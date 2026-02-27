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

    def test_escaping_matches_expected_output(self):
        """Translated PO file should match the expected fixture entry-by-entry"""
        input_path = os.path.join(FIXTURES_DIR, 'escaping_input.po')
        expected_path = os.path.join(FIXTURES_DIR, 'escaping_expected.po')

        # Read expected translations to use as mock API responses
        expected_po = polib.pofile(expected_path)
        fake_translations = [entry.msgstr for entry in expected_po if entry.msgid]

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

            for expected_entry, output_entry in zip(expected_po, output_po):
                if not expected_entry.msgid:
                    continue
                self.assertEqual(
                    output_entry.msgstr,
                    expected_entry.msgstr,
                    f"Mismatch for msgid: {expected_entry.msgid!r}",
                )
        finally:
            os.unlink(output_path)


if __name__ == "__main__":
    unittest.main()
