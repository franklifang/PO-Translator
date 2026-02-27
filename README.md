# PO Translator (PO翻译器)

[![License: GPL v2](https://img.shields.io/badge/License-GPL%20v2-blue.svg)](https://www.gnu.org/licenses/old-licenses/gpl-2.0.en.html)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](https://github.com/franklifang/po-translator)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)

**PO Translator** is an for translating .PO (Portable Object) files using cloud-based AI language models. It provides a user-friendly interface for batch translation with support for multiple AI providers.

**PO翻译器**是一个用于翻译.PO文件的Windows应用程序，使用云端AI大语言模型进行翻译。提供友好的用户界面，支持批量翻译和多个AI提供商。

## ✨ Features (特性)

- 🌐 **Multi-Language Support**: Supports 20+ languages including English, Chinese, Spanish, French, German, Japanese, Korean, etc.
- 🤖 **Multiple AI Providers**: OpenAI, DeepSeek, Zhipu AI, Moonshot, Alibaba Qwen, Huawei Cloud MaaS, and custom APIs
- ⚡ **Batch Translation**: Translates multiple entries in batches for improved performance
- 📝 **PO File Support**: Full support for .PO file format with automatic quote handling
- 🎯 **Smart Processing**: Skips already translated and fuzzy entries
- 🔄 **Error Recovery**: Automatic retry mechanism with user interaction on API failures
- 📊 **Progress Tracking**: Real-time progress display with detailed logging
- 💾 **Configuration Persistence**: Saves API keys and settings locally
- 🆓 **Free & Open Source**: Built with tkinter (no paid dependencies)

## 📋 Requirements (系统要求)

- Windows 7/8/10/11
- Python 3.7 or higher
- Internet connection

## 🚀 Installation (安装)

### 1. Clone the Repository (克隆仓库)

```bash
git clone https://github.com/franklifang/po-translator.git
cd po-translator
```

### 2. Install Dependencies (安装依赖)

```bash
pip install -r requirements.txt
```

### 3. Run the Application (运行程序)

```bash
python src/main.py
```

## 📖 Usage (使用方法)

### Basic Workflow (基本流程)

1. **Select Input File**: Choose the .PO file to translate
2. **Select Output File**: Specify where to save the translated file
3. **Choose Languages**: Select source and target languages
4. **Configure API**: 
   - Select API provider
   - Enter API key
   - Choose AI model
   - Set batch size (10/20/50/100)
5. **Start Translation**: Click "Start Translation" and monitor progress

### API Configuration (API配置)

#### OpenAI
- **Models**: GPT-3.5-Turbo, GPT-4, GPT-4-Turbo, GPT-4o
- **Get API Key**: https://platform.openai.com/api-keys

#### DeepSeek
- **Models**: DeepSeek-Chat, DeepSeek-Coder
- **Get API Key**: https://platform.deepseek.com/

#### Zhipu AI (ChatGLM)
- **Models**: ChatGLM-Pro, ChatGLM-Std, ChatGLM-Lite
- **Get API Key**: https://open.bigmodel.cn/

#### Moonshot (Kimi)
- **Models**: Moonshot-V1-8K, Moonshot-V1-32K, Moonshot-V1-128K
- **Get API Key**: https://platform.moonshot.cn/

#### Alibaba Qwen
- **Models**: Qwen-Turbo, Qwen-Plus, Qwen-Max
- **Get API Key**: https://dashscope.aliyun.com/

#### Huawei Cloud MaaS
- **Models**: DeepSeek-V3.2, and other models
- **Get API Key**: https://www.huaweicloud.com/product/modelarts.html

### Batch Size Selection (批量大小选择)

- **10 items/batch**: For unstable networks or strict API limits
- **20 items/batch**: Balanced performance (recommended)
- **50 items/batch**: For stable networks
- **100 items/batch**: For large-scale translation with stable connection

## 🛠️ Technical Details (技术细节)

### Project Structure (项目结构)

```
po-translator/
├── LICENSE                 # GPL v2 License
├── README.md              # This file
├── requirements.txt       # Python dependencies
├── src/
│   ├── main.py           # GUI application (tkinter)
│   └── po_translator.py  # Core translation engine
├── docs/
│   ├── USER_GUIDE.md     # User guide
│   └── API_PROVIDERS.md  # API provider documentation
└── .github/
    ├── ISSUE_TEMPLATE.md  # Issue template
    └── PULL_REQUEST_TEMPLATE.md  # PR template
```

### Key Features (关键特性)

#### Batch Translation (批量翻译)
Translates multiple PO entries in a single API call for improved performance:
- Reduces API calls by up to 90%
- Significantly faster than single-item translation
- Maintains translation quality

#### Multiline msgid Preservation (多行msgid保留)
Preserves original msgid formatting without line wrapping:
```po
# Original (preserved)
msgid "Display the latest updates of the post author (when used into a page or post), of the displayed user (when viewing their profile) or of your community."

# Not wrapped to multiple lines
```

#### Error Recovery (错误恢复)
Automatic detection and recovery from:
- API timeouts (computer sleep/hibernation)
- Network connection issues
- API rate limits
- User can choose to retry, skip, or stop

## 🤝 Acknowledgments (致谢)

This project uses services from:

- **Huawei Cloud ModelArts** - For providing accessible AI model services
  华为云ModelArts - 提供便捷的AI模型服务

- **Zhipu AI** - For providing advanced language model capabilities
  智谱AI - 提供先进的语言模型能力

We thank these organizations for their contributions to the AI community.

## 📝 License (许可证)

This project is licensed under the GNU General Public License v2.0 - see the [LICENSE](LICENSE) file for details.

本项目采用GNU通用公共许可证v2.0 - 详见[LICENSE](LICENSE)文件。

## 👤 Author (作者)

**LI, Fang (黎昉)**
- Organization: Zokin Design, LLC. (上海左晶多媒体设计有限公司)
- GitHub: [@franklifang](https://github.com/franklifang)

## 🐛 Bug Reports (问题报告)

If you find a bug, please open an issue on GitHub:
[Issues](https://github.com/franklifang/po-translator/issues)

## 📧 Contact (联系方式)

For questions and support, please open an issue or contact:
- Email: support@zokin.com
- Website: https://www.zokin.com

## 🌟 Star History (星标历史)

If you find this project useful, please consider giving it a star ⭐

---

**Version**: 1.0.0  
**Release Date**: 2026  
**License**: GPL v2  
**Copyright**: © 2026 LI, Fang (黎昉)
               © 2026 Zokin Design, LLC.
