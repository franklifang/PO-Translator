"""
PO Translator (PO翻译器) - Core Translation Engine
An application for translating .PO files using cloud AI APIs

Copyright (C) 2026 LI, Fang (黎昉)
Copyright (C) 2026 Zokin Design, LLC. (上海左晶多媒体设计有限公司)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

Version: 1.0.0
Author: LI, Fang (黎昉)
Organization: Zokin Design, LLC. (上海左晶多媒体设计有限公司)
"""

import polib
import requests
import json
import os
import re
import urllib3
from typing import List, Dict, Optional, Callable
from urllib.parse import quote, unquote

# Disable SSL warnings for Huawei Cloud MaaS
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

__version__ = "1.0.0"
__author__ = "LI, Fang (黎昉)"
__organization__ = "Zokin Design, LLC. (上海左晶多媒体设计有限公司)"


class POTranslator:
    """Handles PO file translation using cloud AI APIs"""

    def __init__(self, api_provider: str = "openai", api_key: str = "", api_base: str = ""):
        """
        Initialize the PO Translator

        Args:
            api_provider: API provider ("openai", "deepseek", "zhipu", "moonshot", "qwen", "huawei_maas", "custom")
            api_key: API key for the provider
            api_base: Custom API base URL (optional)
        """
        self.api_provider = api_provider
        self.api_key = api_key
        self.api_base = api_base
        self.model = None
        self.batch_size = 10  # Default batch size
        self.should_stop = False  # Flag to stop translation

        # Default API endpoints for different providers
        self.api_endpoints = {
            "openai": "https://api.openai.com/v1/chat/completions",
            "deepseek": "https://api.deepseek.com/v1/chat/completions",
            "zhipu": "https://open.bigmodel.cn/api/paas/v3/model-api/chatglm_pro/invoke",
            "moonshot": "https://api.moonshot.cn/v1/chat/completions",
            "qwen": "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation",
            "huawei_maas": "https://api.modelarts-maas.com/v2/chat/completions",
            "custom": api_base
        }

    def set_model(self, model_name: str):
        """
        Set the AI model to use for translation

        Args:
            model_name: Name of the model
        """
        self.model = model_name

    def set_batch_size(self, batch_size: int):
        """
        Set the batch size for translation

        Args:
            batch_size: Number of texts to translate per batch (10, 20, 50, or 100)
        """
        self.batch_size = batch_size

    def stop_translation(self):
        """Stop the translation process"""
        self.should_stop = True

    def get_default_models(self):
        """Get default models for each provider"""
        default_models = {
            "openai": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini"],
            "deepseek": ["deepseek-chat", "deepseek-coder"],
            "zhipu": ["chatglm_pro", "chatglm_std", "chatglm_lite"],
            "moonshot": ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"],
            "qwen": ["qwen-turbo", "qwen-plus", "qwen-max", "qwen-max-longcontext"],
            "huawei_maas": ["deepseek-v3.2"],
            "custom": ["custom-model"]
        }
        return default_models.get(self.api_provider, ["unknown"])

    def translate_batch_openai_compatible(self, texts: List[str], source_lang: str, target_lang: str) -> tuple:
        """
        Translate multiple texts in a single API call

        Args:
            texts: List of texts to translate
            source_lang: Source language code
            target_lang: Target language code

        Returns:
            Tuple of (translations list, success boolean, error message)
        """
        endpoint = self.api_endpoints.get(self.api_provider, self.api_base)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

        # Create a numbered list of texts for translation
        numbered_texts = "\n".join([f"{i+1}. {text}" for i, text in enumerate(texts)])

        prompt = f"""You are a professional translator. Translate the following numbered texts from {source_lang} to {target_lang}.
Provide ONLY the translations in the same numbered format, one per line.
Do not add any explanations or additional text.

Texts to translate:
{numbered_texts}

Translations:"""

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are a professional translator. Provide accurate and natural translations."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3,
            "max_tokens": 4000
        }

        try:
            verify_ssl = self.api_provider != "huawei_maas"
            response = requests.post(endpoint, headers=headers, json=payload, timeout=120, verify=verify_ssl)
            response.raise_for_status()

            result = response.json()
            translated_text = result["choices"][0]["message"]["content"].strip()

            # Parse the numbered translations
            translations = []
            lines = translated_text.split('\n')
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                # Remove number prefix (e.g., "1. ", "2. ", etc.)
                match = re.match(r'^\d+\.\s*(.+)$', line)
                if match:
                    translations.append(match.group(1).strip())
                elif line:
                    translations.append(line)

            # Ensure we have the same number of translations as inputs
            while len(translations) < len(texts):
                translations.append(texts[len(translations)])  # Use original if missing

            return translations[:len(texts)], True, None

        except requests.exceptions.Timeout:
            return texts, False, "API request timed out (possible sleep/hibernation)"
        except requests.exceptions.ConnectionError as e:
            return texts, False, f"Connection error: {str(e)}"
        except requests.exceptions.RequestException as e:
            return texts, False, f"API request failed: {str(e)}"
        except Exception as e:
            return texts, False, f"Unexpected error: {str(e)}"

    def translate_batch(self, texts: List[str], source_lang: str, target_lang: str) -> tuple:
        """
        Translate multiple texts

        Args:
            texts: List of texts to translate
            source_lang: Source language code
            target_lang: Target language code

        Returns:
            Tuple of (translations list, success boolean, error message)
        """
        if not texts:
            return [], True, None

        if self.api_provider in ["openai", "deepseek", "moonshot", "huawei_maas", "custom"]:
            return self.translate_batch_openai_compatible(texts, source_lang, target_lang)
        else:
            # For other providers, translate one by one
            translations = []
            for text in texts:
                result, success, error = self.translate_batch_openai_compatible([text], source_lang, target_lang)
                if not success:
                    return texts, False, error
                translations.append(result[0])
            return translations, True, None

    def translate_po_file(
        self,
        input_file: str,
        output_file: str,
        source_lang: str,
        target_lang: str,
        progress_callback: Optional[Callable] = None,
        error_callback: Optional[Callable] = None
    ) -> Dict:
        """
        Translate a PO file with batch processing and error recovery

        Args:
            input_file: Path to input PO file
            output_file: Path to output PO file
            source_lang: Source language code
            target_lang: Target language code
            progress_callback: Optional callback function for progress updates
            error_callback: Optional callback function for error handling (returns 'retry', 'skip', or 'stop')

        Returns:
            Dictionary with translation statistics
        """
        self.should_stop = False
        
        # Load the PO file
        po = polib.pofile(input_file)

        stats = {
            "total": len(po),
            "translated": 0,
            "fuzzy": 0,
            "untranslated": 0,
            "errors": 0
        }

        # Collect texts to translate
        texts_to_translate = []
        entry_indices = []

        for i, entry in enumerate(po):
            # Skip entries that are already translated
            if entry.msgstr and not entry.obsolete:
                stats["translated"] += 1
                continue

            # Skip fuzzy translations
            if "fuzzy" in entry.flags:
                stats["fuzzy"] += 1
                continue

            # Skip empty msgid
            if not entry.msgid or not entry.msgid.strip():
                continue

            # Add to batch
            texts_to_translate.append(entry.msgid)
            entry_indices.append(i)

        stats["untranslated"] = len(texts_to_translate)

        if texts_to_translate:
            if progress_callback:
                progress_callback(0, len(texts_to_translate), "Starting batch translation...")

            # Translate in batches
            total_batches = (len(texts_to_translate) + self.batch_size - 1) // self.batch_size

            for batch_num in range(total_batches):
                if self.should_stop:
                    if progress_callback:
                        progress_callback(0, len(texts_to_translate), "Translation stopped by user")
                    break

                start_idx = batch_num * self.batch_size
                end_idx = min(start_idx + self.batch_size, len(texts_to_translate))

                batch_texts = texts_to_translate[start_idx:end_idx]
                batch_indices = entry_indices[start_idx:end_idx]

                # Try to translate batch
                max_retries = 3
                retry_count = 0
                success = False

                while retry_count < max_retries and not success:
                    if self.should_stop:
                        break

                    try:
                        if progress_callback:
                            progress_callback(
                                start_idx,
                                len(texts_to_translate),
                                f"Translating batch {batch_num + 1}/{total_batches} ({len(batch_texts)} items)..."
                            )

                        # Translate batch
                        translations, success, error_msg = self.translate_batch(batch_texts, source_lang, target_lang)

                        if not success:
                            # API call failed
                            if error_callback:
                                action = error_callback(error_msg, batch_num + 1, total_batches)
                                if action == 'stop':
                                    self.should_stop = True
                                    break
                                elif action == 'skip':
                                    # Use original texts
                                    translations = batch_texts
                                    success = True
                                elif action == 'retry':
                                    retry_count += 1
                                    if retry_count < max_retries:
                                        if progress_callback:
                                            progress_callback(
                                                start_idx,
                                                len(texts_to_translate),
                                                f"Retrying batch {batch_num + 1} (attempt {retry_count + 1}/{max_retries})..."
                                            )
                                        continue
                                    else:
                                        # Max retries reached, skip this batch
                                        translations = batch_texts
                                        success = True
                            else:
                                # No error callback, use original texts
                                translations = batch_texts
                                success = True

                        if success:
                            # Apply translations
                            for idx, translation in zip(batch_indices, translations):
                                entry = po[idx]
                                entry.msgstr = translation

                    except Exception as e:
                        stats["errors"] += len(batch_texts)
                        print(f"Error in batch {batch_num + 1}: {e}")
                        if error_callback:
                            action = error_callback(str(e), batch_num + 1, total_batches)
                            if action == 'stop':
                                self.should_stop = True
                                break
                        break

                if progress_callback:
                    progress_callback(end_idx, len(texts_to_translate), f"Completed batch {batch_num + 1}/{total_batches}")

        # Update language in metadata
        if po.metadata:
            po.metadata["Language"] = target_lang

        # Save the translated PO file with wrap width set to 0 to prevent line wrapping
        po.wrapwidth = 0  # Disable line wrapping
        po.save(output_file)

        return stats

    def get_language_name(self, lang_code: str) -> str:
        """
        Get full language name from language code

        Args:
            lang_code: Language code (e.g., "en", "zh", "es")

        Returns:
            Full language name
        """
        language_map = {
            "en": "English",
            "zh": "Chinese (Simplified)",
            "zh-CN": "Chinese (Simplified)",
            "zh-TW": "Chinese (Traditional)",
            "es": "Spanish",
            "fr": "French",
            "de": "German",
            "ja": "Japanese",
            "ko": "Korean",
            "ru": "Russian",
            "it": "Italian",
            "pt": "Portuguese",
            "pt-BR": "Portuguese (Brazil)",
            "ar": "Arabic",
            "hi": "Hindi",
            "th": "Thai",
            "vi": "Vietnamese",
            "id": "Indonesian",
            "nl": "Dutch",
            "pl": "Polish",
            "tr": "Turkish",
            "uk": "Ukrainian"
        }
        return language_map.get(lang_code, lang_code)
