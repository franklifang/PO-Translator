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


class TestQuoteEscaping(unittest.TestCase):
    """Test that quotes and backslashes in translations are not double-escaped"""

    def _create_po_file(self, entries):
        """Helper to create a temporary PO file with the given msgid entries."""
        po = polib.POFile()
        po.metadata = {"Content-Type": "text/plain; charset=UTF-8"}
        for msgid in entries:
            po.append(polib.POEntry(msgid=msgid, msgstr=""))
        fd, path = tempfile.mkstemp(suffix=".po")
        os.close(fd)
        po.save(path)
        return path

    def _run_translation(self, input_path, fake_translations):
        """Run translate_po_file with mocked API responses."""
        translator = POTranslator(api_provider="openai", api_key="fake")
        translator.set_model("gpt-4o")

        fd, output_path = tempfile.mkstemp(suffix=".po")
        os.close(fd)

        with patch.object(
            translator,
            "translate_batch",
            return_value=(fake_translations, True, None),
        ):
            translator.translate_po_file(input_path, output_path, "en", "zh")

        return output_path

    def test_quotes_not_double_escaped(self):
        """Quotes in translations should appear as \" in the PO file, not \\\""""
        input_path = self._create_po_file(['She said "hello"'])
        output_path = self._run_translation(input_path, ['她说"你好"'])

        try:
            po = polib.pofile(output_path)
            self.assertEqual(po[0].msgstr, '她说"你好"')
        finally:
            os.unlink(input_path)
            os.unlink(output_path)

    def test_backslashes_not_double_escaped(self):
        """Backslashes in translations should appear as \\\\ in PO, not \\\\\\\\"""
        input_path = self._create_po_file(["path\\to\\file"])
        output_path = self._run_translation(input_path, ["路径\\到\\文件"])

        try:
            po = polib.pofile(output_path)
            self.assertEqual(po[0].msgstr, "路径\\到\\文件")
        finally:
            os.unlink(input_path)
            os.unlink(output_path)

    def test_mixed_special_characters(self):
        """Translations with both quotes and backslashes should be escaped correctly"""
        input_path = self._create_po_file(['Click "OK" or press \\n'])
        output_path = self._run_translation(input_path, ['点击"确定"或按\\n'])

        try:
            po = polib.pofile(output_path)
            self.assertEqual(po[0].msgstr, '点击"确定"或按\\n')
        finally:
            os.unlink(input_path)
            os.unlink(output_path)

    def test_plain_text_unchanged(self):
        """Translations without special characters should pass through unchanged"""
        input_path = self._create_po_file(["Hello world"])
        output_path = self._run_translation(input_path, ["你好世界"])

        try:
            po = polib.pofile(output_path)
            self.assertEqual(po[0].msgstr, "你好世界")
        finally:
            os.unlink(input_path)
            os.unlink(output_path)


if __name__ == "__main__":
    unittest.main()
