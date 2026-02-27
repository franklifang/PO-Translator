"""
PO Translator (PO翻译器) - Windows GUI Application
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

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import os
import threading
import json
from po_translator import POTranslator, __version__, __author__, __organization__

__app_name__ = "PO Translator"
__app_name_cn__ = "PO翻译器"


# Language options
LANGUAGES = [
    "English (en)",
    "Chinese Simplified (zh)",
    "Chinese Traditional (zh-TW)",
    "Spanish (es)",
    "French (fr)",
    "German (de)",
    "Japanese (ja)",
    "Korean (ko)",
    "Russian (ru)",
    "Italian (it)",
    "Portuguese (pt)",
    "Portuguese Brazil (pt-BR)",
    "Arabic (ar)",
    "Hindi (hi)",
    "Thai (th)",
    "Vietnamese (vi)",
    "Indonesian (id)",
    "Dutch (nl)",
    "Polish (pl)",
    "Turkish (tr)",
    "Ukrainian (uk)"
]

# API Providers
API_PROVIDERS = [
    "OpenAI",
    "DeepSeek",
    "Zhipu AI (ChatGLM)",
    "Moonshot (Kimi)",
    "Alibaba Qwen",
    "Huawei Cloud MaaS",
    "Custom API"
]

# Provider mapping
PROVIDER_MAP = {
    "OpenAI": "openai",
    "DeepSeek": "deepseek",
    "Zhipu AI (ChatGLM)": "zhipu",
    "Moonshot (Kimi)": "moonshot",
    "Alibaba Qwen": "qwen",
    "Huawei Cloud MaaS": "huawei_maas",
    "Custom API": "custom"
}

# Default models for each provider
DEFAULT_MODELS = {
    "OpenAI": ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo", "gpt-4o", "gpt-4o-mini"],
    "DeepSeek": ["deepseek-chat", "deepseek-coder"],
    "Zhipu AI (ChatGLM)": ["chatglm_pro", "chatglm_std", "chatglm_lite"],
    "Moonshot (Kimi)": ["moonshot-v1-8k", "moonshot-v1-32k", "moonshot-v1-128k"],
    "Alibaba Qwen": ["qwen-turbo", "qwen-plus", "qwen-max", "qwen-max-longcontext"],
    "Huawei Cloud MaaS": ["deepseek-v3.2"],
    "Custom API": ["custom-model"]
}

# Config file path
CONFIG_FILE = "config.json"


class POTranslatorGUI:
    """Main GUI application for PO file translation"""

    def __init__(self, root):
        self.root = root
        self.root.title(f"{__app_name__} v{__version__}")
        self.root.geometry("800x750")
        
        self.translator = None
        self.translation_running = False
        self.config = self.load_config()
        
        self.create_widgets()
        self.load_saved_settings()

    def load_config(self):
        """Load configuration from file"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {
            "api_keys": {},
            "last_provider": "OpenAI",
            "last_model": "gpt-3.5-turbo",
            "custom_api_url": "",
            "batch_size": "10"
        }

    def save_config(self):
        """Save configuration to file"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")

    def create_widgets(self):
        """Create all GUI widgets"""
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(main_frame, text=f"{__app_name__} ({__app_name_cn__})", 
                               font=("Helvetica", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 5))

        subtitle_label = ttk.Label(main_frame, 
                                  text=f"Translates .PO files using cloud AI APIs | v{__version__}", 
                                  foreground="gray")
        subtitle_label.grid(row=1, column=0, columnspan=3, pady=(0, 10))

        # File selection
        ttk.Label(main_frame, text="Input PO File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.input_file_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.input_file_var, width=50).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_input_file).grid(row=2, column=2, padx=5, pady=5)

        ttk.Label(main_frame, text="Output PO File:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.output_file_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.output_file_var, width=50).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output_file).grid(row=3, column=2, padx=5, pady=5)

        # Language selection
        ttk.Label(main_frame, text="Source Language:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.source_lang_var = tk.StringVar(value="English (en)")
        source_lang_combo = ttk.Combobox(main_frame, textvariable=self.source_lang_var, values=LANGUAGES, width=47, state="readonly")
        source_lang_combo.grid(row=4, column=1, sticky=tk.W, pady=5)

        ttk.Label(main_frame, text="Target Language:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.target_lang_var = tk.StringVar(value="Chinese Simplified (zh)")
        target_lang_combo = ttk.Combobox(main_frame, textvariable=self.target_lang_var, values=LANGUAGES, width=47, state="readonly")
        target_lang_combo.grid(row=5, column=1, sticky=tk.W, pady=5)

        # API Provider
        ttk.Label(main_frame, text="API Provider:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.provider_var = tk.StringVar(value=self.config.get("last_provider", "OpenAI"))
        provider_combo = ttk.Combobox(main_frame, textvariable=self.provider_var, values=API_PROVIDERS, width=47, state="readonly")
        provider_combo.grid(row=6, column=1, sticky=tk.W, pady=5)
        provider_combo.bind("<<ComboboxSelected>>", self.on_provider_change)

        # API Key
        ttk.Label(main_frame, text="API Key:").grid(row=7, column=0, sticky=tk.W, pady=5)
        self.api_key_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.api_key_var, width=50, show="*").grid(row=7, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="Save Key", command=self.save_api_key).grid(row=7, column=2, padx=5, pady=5)

        # Model
        ttk.Label(main_frame, text="AI Model:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.model_var = tk.StringVar(value=self.config.get("last_model", "gpt-3.5-turbo"))
        self.model_combo = ttk.Combobox(main_frame, textvariable=self.model_var, width=47)
        self.model_combo.grid(row=8, column=1, sticky=tk.W, pady=5)

        # Batch size
        ttk.Label(main_frame, text="Batch Size:").grid(row=9, column=0, sticky=tk.W, pady=5)
        self.batch_size_var = tk.StringVar(value=str(self.config.get("batch_size", "10")))
        batch_size_combo = ttk.Combobox(main_frame, textvariable=self.batch_size_var, values=["10", "20", "50", "100"], width=47, state="readonly")
        batch_size_combo.grid(row=9, column=1, sticky=tk.W, pady=5)

        # Custom API URL
        ttk.Label(main_frame, text="Custom API URL:").grid(row=10, column=0, sticky=tk.W, pady=5)
        self.custom_url_var = tk.StringVar(value=self.config.get("custom_api_url", ""))
        self.custom_url_entry = ttk.Entry(main_frame, textvariable=self.custom_url_var, width=50)
        self.custom_url_entry.grid(row=10, column=1, sticky=(tk.W, tk.E), pady=5)

        # Log area
        ttk.Label(main_frame, text="Log:").grid(row=11, column=0, sticky=tk.W, pady=(10, 5))
        self.log_text = scrolledtext.ScrolledText(main_frame, width=70, height=15, font=("Consolas", 9))
        self.log_text.grid(row=12, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100, length=500)
        self.progress_bar.grid(row=13, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)

        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, foreground="blue")
        self.status_label.grid(row=14, column=0, columnspan=3, sticky=tk.W, pady=5)

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=15, column=0, columnspan=3, pady=10)

        self.start_button = ttk.Button(button_frame, text="Start Translation", command=self.start_translation)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_translation, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5)

        ttk.Button(button_frame, text="Clear Log", command=self.clear_log).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="About", command=self.show_about).grid(row=0, column=3, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.exit_application).grid(row=0, column=4, padx=5)

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(12, weight=1)

    def load_saved_settings(self):
        """Load saved settings"""
        provider = self.config.get("last_provider", "OpenAI")
        if provider in self.config.get("api_keys", {}):
            self.api_key_var.set(self.config["api_keys"][provider])
        
        # Update model list
        self.on_provider_change(None)

    def on_provider_change(self, event):
        """Handle provider change"""
        provider = self.provider_var.get()
        models = DEFAULT_MODELS.get(provider, [])
        self.model_combo['values'] = models
        if models:
            self.model_var.set(models[0])
        
        # Load saved API key
        if provider in self.config.get("api_keys", {}):
            self.api_key_var.set(self.config["api_keys"][provider])
        else:
            self.api_key_var.set("")
        
        # Show/hide custom URL
        if provider == "Custom API":
            self.custom_url_entry.grid()
        else:
            self.custom_url_entry.grid_remove()

    def browse_input_file(self):
        """Browse for input PO file"""
        filename = filedialog.askopenfilename(filetypes=[("PO Files", "*.po"), ("All Files", "*.*")])
        if filename:
            self.input_file_var.set(filename)

    def browse_output_file(self):
        """Browse for output PO file"""
        filename = filedialog.asksaveasfilename(filetypes=[("PO Files", "*.po"), ("All Files", "*.*")])
        if filename:
            self.output_file_var.set(filename)

    def save_api_key(self):
        """Save API key"""
        provider = self.provider_var.get()
        api_key = self.api_key_var.get()
        if api_key:
            if "api_keys" not in self.config:
                self.config["api_keys"] = {}
            self.config["api_keys"][provider] = api_key
            self.save_config()
            self.log_message(f"API key saved for {provider}")
        else:
            messagebox.showwarning("Warning", "Please enter an API key first")

    def log_message(self, message):
        """Add message to log"""
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

    def clear_log(self):
        """Clear log"""
        self.log_text.delete(1.0, tk.END)

    def extract_lang_code(self, lang_string):
        """Extract language code from language string"""
        for lang in LANGUAGES:
            if lang_string in lang:
                start = lang.find("(") + 1
                end = lang.find(")")
                return lang[start:end]
        return lang_string

    def error_callback(self, error_msg, batch_num, total_batches):
        """
        Handle API errors with user interaction
        
        Returns:
            'retry', 'skip', or 'stop'
        """
        # This will be called from background thread, so we need to use root.after
        result = [None]
        
        def show_dialog():
            message = f"API Error in batch {batch_num}/{total_batches}:\n\n{error_msg}\n\n"
            message += "This might be due to:\n"
            message += "- Computer sleep/hibernation\n"
            message += "- Network connection issue\n"
            message += "- API rate limit\n\n"
            message += "What would you like to do?"
            
            dialog = tk.Toplevel(self.root)
            dialog.title("API Error")
            dialog.geometry("500x300")
            dialog.transient(self.root)
            dialog.grab_set()
            
            ttk.Label(dialog, text=message, wraplength=450, justify=tk.LEFT).pack(pady=20, padx=20)
            
            button_frame = ttk.Frame(dialog)
            button_frame.pack(pady=10)
            
            def on_retry():
                result[0] = 'retry'
                dialog.destroy()
            
            def on_skip():
                result[0] = 'skip'
                dialog.destroy()
            
            def on_stop():
                result[0] = 'stop'
                dialog.destroy()
            
            ttk.Button(button_frame, text="Retry", command=on_retry).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Skip This Batch", command=on_skip).pack(side=tk.LEFT, padx=5)
            ttk.Button(button_frame, text="Stop Translation", command=on_stop).pack(side=tk.LEFT, padx=5)
            
            dialog.wait_window()
        
        # Show dialog in main thread
        self.root.after(0, show_dialog)
        
        # Wait for result
        while result[0] is None:
            import time
            time.sleep(0.1)
        
        return result[0]

    def start_translation(self):
        """Start translation"""
        if self.translation_running:
            messagebox.showinfo("Info", "Translation is already running!")
            return

        # Validate inputs
        input_file = self.input_file_var.get()
        output_file = self.output_file_var.get()
        api_key = self.api_key_var.get()

        if not input_file or not os.path.exists(input_file):
            messagebox.showerror("Error", "Input file does not exist!")
            return

        if not output_file:
            messagebox.showerror("Error", "Please specify output file!")
            return

        if not api_key:
            messagebox.showerror("Error", "Please enter API key!")
            return

        # Start translation in separate thread
        self.translation_running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_var.set("Translation in progress...")
        self.status_label.config(foreground="blue")

        thread = threading.Thread(target=self.run_translation, daemon=True)
        thread.start()

    def run_translation(self):
        """Run translation in background"""
        try:
            input_file = self.input_file_var.get()
            output_file = self.output_file_var.get()
            source_lang = self.extract_lang_code(self.source_lang_var.get())
            target_lang = self.extract_lang_code(self.target_lang_var.get())
            provider_name = self.provider_var.get()
            api_key = self.api_key_var.get()
            model = self.model_var.get()
            custom_url = self.custom_url_var.get()

            provider_code = PROVIDER_MAP.get(provider_name, "openai")

            self.translator = POTranslator(
                api_provider=provider_code,
                api_key=api_key,
                api_base=custom_url
            )
            self.translator.set_model(model)
            
            # Set batch size
            try:
                batch_size = int(self.batch_size_var.get())
                self.translator.set_batch_size(batch_size)
            except:
                self.translator.set_batch_size(10)

            self.log_message("Starting translation...")
            self.log_message(f"Input: {input_file}")
            self.log_message(f"Output: {output_file}")
            self.log_message(f"Source Language: {source_lang}")
            self.log_message(f"Target Language: {target_lang}")
            self.log_message(f"API Provider: {provider_name}")
            self.log_message(f"Model: {model}")
            self.log_message(f"Batch Size: {self.translator.batch_size}")

            # Progress callback
            def progress_callback(current, total, message):
                if not self.translation_running:
                    self.translator.stop_translation()
                    return
                progress = (current / total) * 100 if total > 0 else 0
                self.root.after(0, lambda: self.update_progress(progress, message))

            # Run translation
            stats = self.translator.translate_po_file(
                input_file, output_file, source_lang, target_lang, 
                progress_callback, self.error_callback
            )

            # Show results
            self.root.after(0, lambda: self.show_results(stats, output_file))

        except Exception as e:
            self.root.after(0, lambda: self.show_error(str(e)))

        finally:
            self.translation_running = False
            self.root.after(0, self.translation_finished)

    def update_progress(self, progress, message):
        """Update progress bar and status"""
        self.progress_var.set(progress)
        self.status_var.set(f"{message} ({progress:.1f}%)")
        self.log_message(f"[{progress:.0f}%] {message}")

    def show_results(self, stats, output_file):
        """Show translation results"""
        self.log_message("\n" + "="*50)
        self.log_message("Translation Complete!")
        self.log_message(f"Total entries: {stats['total']}")
        self.log_message(f"Already translated: {stats['translated']}")
        self.log_message(f"Fuzzy entries: {stats['fuzzy']}")
        self.log_message(f"Untranslated: {stats['untranslated']}")
        self.log_message(f"Errors: {stats['errors']}")
        self.log_message(f"Output saved to: {output_file}")
        self.log_message("="*50)

        self.status_var.set("Translation completed successfully!")
        self.status_label.config(foreground="green")
        messagebox.showinfo("Success", f"Translation completed!\nOutput saved to: {output_file}")

    def show_error(self, error):
        """Show error message"""
        self.log_message(f"Error during translation: {error}")
        self.status_var.set(f"Error: {error}")
        self.status_label.config(foreground="red")
        messagebox.showerror("Error", f"Translation failed:\n{error}")

    def translation_finished(self):
        """Called when translation finishes"""
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def stop_translation(self):
        """Stop translation"""
        self.translation_running = False
        if self.translator:
            self.translator.stop_translation()
        self.log_message("Stopping translation...")
        self.stop_button.config(state=tk.DISABLED)

    def show_about(self):
        """Show about dialog"""
        about_text = f"""{__app_name__} ({__app_name_cn__})
Version {__version__}

{__organization__}

Copyright (C) 2026 {__author__}

This program is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

Acknowledgments:
- Huawei Cloud ModelArts
- Zhipu AI

Website: https://www.zokin.com
GitHub: https://github.com/franklifang/po-translator"""
        
        messagebox.showinfo("About", about_text)

    def exit_application(self):
        """Exit application"""
        # Save config
        self.config["last_provider"] = self.provider_var.get()
        self.config["last_model"] = self.model_var.get()
        self.config["custom_api_url"] = self.custom_url_var.get()
        self.config["batch_size"] = self.batch_size_var.get()
        self.save_config()
        
        self.root.quit()
        self.root.destroy()


def main():
    """Main entry point"""
    root = tk.Tk()
    app = POTranslatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
