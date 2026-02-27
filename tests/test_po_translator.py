"""Tests for PO Translator core translation engine"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch

import polib

# Add src to path so we can import po_translator
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from po_translator import POTranslator, sanitize_po_file

FIXTURES_DIR = os.path.join(os.path.dirname(__file__), 'fixtures')


class TestQuoteEscaping(unittest.TestCase):
    """Test that quotes and backslashes in translations are not double-escaped"""

    def test_special_characters_not_doubled(self):
        """The number of quotes and backslashes should be preserved, not doubled by extra escaping"""
        input_path = os.path.join(FIXTURES_DIR, 'escaping_input.po')

        # Simulate translations that contain special characters
        fake_translations = [
            '她说"你好"',        # 2 quotes
            '路径\\到\\文件',     # 2 backslashes
            '点击"确定"或按\\n',  # 2 quotes + 1 backslash
            '你好世界',           # no special characters
        ]

        translator = POTranslator(api_provider="openai", api_key="fake")
        translator.set_model("gpt-4o")

        fd, output_path = tempfile.mkstemp(suffix=".po")
        os.close(fd)

        try:
            with patch.object(
                translator,
                "translate_batch",
                return_value=(fake_translations, True, None),
            ):
                translator.translate_po_file(input_path, output_path, "en", "zh")

            output_po = polib.pofile(output_path)
            output_entries = [e for e in output_po if e.msgid]

            for fake, entry in zip(fake_translations, output_entries):
                expected_quotes = fake.count('"')
                expected_backslashes = fake.count('\\')
                actual_quotes = entry.msgstr.count('"')
                actual_backslashes = entry.msgstr.count('\\')

                self.assertEqual(
                    actual_quotes,
                    expected_quotes,
                    f'Quote count mismatch for msgid {entry.msgid!r}: '
                    f'expected {expected_quotes}, got {actual_quotes} in {entry.msgstr!r}',
                )
                self.assertEqual(
                    actual_backslashes,
                    expected_backslashes,
                    f'Backslash count mismatch for msgid {entry.msgid!r}: '
                    f'expected {expected_backslashes}, got {actual_backslashes} in {entry.msgstr!r}',
                )
        finally:
            os.unlink(output_path)


class TestSanitizePOFile(unittest.TestCase):
    """Test that malformed PO files with unescaped quotes are sanitized correctly"""

    def test_malformed_file_can_be_loaded_after_sanitize(self):
        """A PO file with unescaped inner quotes should be loadable after sanitization"""
        malformed_path = os.path.join(FIXTURES_DIR, 'malformed_quotes.po')

        # Verify the malformed file cannot be loaded directly
        with self.assertRaises(Exception):
            polib.pofile(malformed_path)

        # Sanitize and verify it can now be loaded
        fd, sanitized_path = tempfile.mkstemp(suffix=".po")
        os.close(fd)

        try:
            sanitize_po_file(malformed_path, sanitized_path)
            po = polib.pofile(sanitized_path)

            entries = [e for e in po if e.msgid]
            self.assertEqual(len(entries), 3)
        finally:
            os.unlink(sanitized_path)

    def test_already_escaped_quotes_not_doubled(self):
        """Quotes that are already escaped should not be escaped again"""
        malformed_path = os.path.join(FIXTURES_DIR, 'malformed_quotes.po')

        fd, sanitized_path = tempfile.mkstemp(suffix=".po")
        os.close(fd)

        try:
            sanitize_po_file(malformed_path, sanitized_path)
            po = polib.pofile(sanitized_path)

            # The first entry has properly escaped quotes in the original:
            # msgid "Built with %1$s by <a href=\"%2$s\">%3$d volunteers</a>."
            # polib unescapes \" to " when reading, so we expect exactly 2 quotes
            # (the ones around %2$s in the href). If sanitize doubled them,
            # we'd see extra backslashes instead.
            first = [e for e in po if e.msgid][0]
            self.assertEqual(
                first.msgid.count('"'), 2,
                f'Already-escaped quotes were corrupted: {first.msgid!r}',
            )
        finally:
            os.unlink(sanitized_path)

    def test_unescaped_quotes_get_escaped(self):
        """Unescaped inner quotes should be properly escaped after sanitization"""
        malformed_path = os.path.join(FIXTURES_DIR, 'malformed_quotes.po')

        fd, sanitized_path = tempfile.mkstemp(suffix=".po")
        os.close(fd)

        try:
            sanitize_po_file(malformed_path, sanitized_path)
            po = polib.pofile(sanitized_path)

            # The entry with msgctxt had unescaped quotes:
            # msgctxt "Colloquial alternative to "learn about BuddyPress""
            # After sanitize, msgctxt should contain the quotes as literal characters
            entry_with_ctx = [e for e in po if e.msgctxt][0]
            self.assertIn('"', entry_with_ctx.msgctxt,
                          f'Inner quotes should be preserved in msgctxt: {entry_with_ctx.msgctxt!r}')
        finally:
            os.unlink(sanitized_path)

    def test_translate_po_file_handles_malformed_input(self):
        """translate_po_file should handle malformed PO files via built-in sanitization"""
        malformed_path = os.path.join(FIXTURES_DIR, 'malformed_quotes.po')

        fake_translations = ['用 %1$s 构建', '你好，BuddyPress！', '你好世界']

        translator = POTranslator(api_provider="openai", api_key="fake")
        translator.set_model("gpt-4o")

        fd, output_path = tempfile.mkstemp(suffix=".po")
        os.close(fd)

        try:
            with patch.object(
                translator,
                "translate_batch",
                return_value=(fake_translations, True, None),
            ):
                stats = translator.translate_po_file(
                    malformed_path, output_path, "en", "zh"
                )

            self.assertEqual(stats["untranslated"], 3)
            output_po = polib.pofile(output_path)
            translated = [e for e in output_po if e.msgstr and e.msgid]
            self.assertEqual(len(translated), 3)
        finally:
            os.unlink(output_path)


if __name__ == "__main__":
    unittest.main()
