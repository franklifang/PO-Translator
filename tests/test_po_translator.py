"""Tests for PO Translator core translation engine"""

import os
import sys
import tempfile
import unittest
from unittest.mock import patch

import polib

# Add src to path so we can import po_translator
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from po_translator import POTranslator

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


if __name__ == "__main__":
    unittest.main()
