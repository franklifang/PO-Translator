# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-XX-XX

### Added
- Initial release of PO Translator
- Support for multiple AI providers (OpenAI, DeepSeek, Zhipu AI, Moonshot, Alibaba Qwen, Huawei Cloud MaaS)
- Batch translation for improved performance
- Configurable batch size (10/20/50/100 items)
- Multi-language support (20+ languages)
- Automatic quote handling in PO files
- Error recovery with retry mechanism
- Progress tracking with detailed logging
- API key management and local storage
- Configuration persistence
- User-friendly GUI with tkinter
- Multiline msgid preservation
- GPL v2 license

### Features
- **Batch Translation**: Translates multiple entries in a single API call
- **Error Recovery**: Automatic detection and recovery from API failures
- **Smart Processing**: Skips already translated and fuzzy entries
- **Progress Tracking**: Real-time progress display with detailed logging
- **Configuration Persistence**: Saves API keys and settings locally
- **Free & Open Source**: Built with tkinter (no paid dependencies)

### Supported Languages
- English
- Chinese (Simplified & Traditional)
- Spanish
- French
- German
- Japanese
- Korean
- Russian
- Italian
- Portuguese
- Arabic
- Hindi
- Thai
- Vietnamese
- Indonesian
- Dutch
- Polish
- Turkish
- Ukrainian

### Supported API Providers
- OpenAI (GPT-3.5, GPT-4, GPT-4o)
- DeepSeek
- Zhipu AI (ChatGLM)
- Moonshot (Kimi)
- Alibaba Qwen
- Huawei Cloud MaaS
- Custom API endpoints

### Technical Details
- Python 3.7+ support
- Windows 7/8/10/11 compatibility
- No external GUI dependencies (uses tkinter)
- Minimal dependencies (polib, requests)

### Acknowledgments
- Huawei Cloud ModelArts for accessible AI model services
- Zhipu AI for advanced language model capabilities

---

## Future Plans

### [1.1.0] - Planned
- Batch file processing
- Translation memory support
- Custom glossary support
- Export/import settings
- Command-line interface
- Linux and macOS support

### [1.2.0] - Planned
- Translation quality scoring
- Auto-detect source language
- Support for more PO file features
- Performance optimizations
- Plugin system for custom providers

---

**Note**: This project follows [Semantic Versioning](https://semver.org/). 
- Major version (X.0.0): Incompatible API changes
- Minor version (1.X.0): New features, backward compatible
- Patch version (1.0.X): Bug fixes, backward compatible
