# PO Translator User Guide (用户指南)

## Table of Contents (目录)

1. [Getting Started (快速开始)](#getting-started)
2. [Installation (安装)](#installation)
3. [Configuration (配置)](#configuration)
4. [Using PO Translator (使用PO翻译器)](#using-po-translator)
5. [API Providers (API提供商)](#api-providers)
6. [Troubleshooting (故障排除)](#troubleshooting)
7. [FAQ (常见问题)](#faq)

## Getting Started (快速开始)

PO Translator is a application for translating .PO (Portable Object) files using cloud-based AI language models. This guide will help you get started quickly.

PO翻译器是一个用于翻译.PO文件的Windows应用程序，使用云端AI大语言模型进行翻译。本指南将帮助您快速上手。

### Prerequisites (前提条件)

- Windows 7/8/10/11
- Python 3.7 or higher
- Internet connection
- API key from a supported provider

## Installation (安装)

### Step 1: Download (下载)

Clone the repository:
```bash
git clone https://github.com/franklifang/po-translator.git
cd po-translator
```

### Step 2: Install Dependencies (安装依赖)

```bash
pip install -r requirements.txt
```

### Step 3: Run (运行)

```bash
python src/main.py
```

## Configuration (配置)

### API Key Setup (API密钥设置)

1. Select your API provider from the dropdown
2. Enter your API key in the "API Key" field
3. Click "Save Key" to store it locally

**Note**: API keys are stored locally in `config.json`. Keep this file secure!

**注意**：API密钥本地存储在`config.json`文件中。请妥善保管此文件！

### Batch Size Configuration (批量大小配置)

Choose the appropriate batch size based on your network stability:

- **10 items**: Unstable network or strict API limits
- **20 items**: Balanced performance (recommended)
- **50 items**: Stable network
- **100 items**: Large-scale translation with very stable connection

## Using PO Translator (使用PO翻译器)

### Basic Workflow (基本流程)

1. **Select Input File**
   - Click "Browse" next to "Input PO File"
   - Select the .PO file you want to translate

2. **Select Output File**
   - Click "Browse" next to "Output PO File"
   - Choose where to save the translated file

3. **Choose Languages**
   - Source Language: The language of the original PO file
   - Target Language: The language to translate to

4. **Configure API**
   - Select API Provider
   - Enter API Key
   - Choose AI Model
   - Set Batch Size

5. **Start Translation**
   - Click "Start Translation"
   - Monitor progress in the log window
   - Wait for completion

### Understanding the Log (理解日志)

The log window shows:
- Translation progress
- Batch information
- Any errors or warnings
- Final statistics

### Error Handling (错误处理)

If an API error occurs, you'll see a dialog with three options:

1. **Retry**: Try the current batch again
2. **Skip This Batch**: Skip and use original text
3. **Stop Translation**: Stop the entire process

## API Providers (API提供商)

### OpenAI

**Models**: GPT-3.5-Turbo, GPT-4, GPT-4-Turbo, GPT-4o

**Get API Key**: https://platform.openai.com/api-keys

**Pricing**: Pay-per-use

**Best for**: General translation, high quality

### DeepSeek

**Models**: DeepSeek-Chat, DeepSeek-Coder

**Get API Key**: https://platform.deepseek.com/

**Pricing**: Very competitive

**Best for**: Chinese-English translation, technical content

### Zhipu AI (ChatGLM)

**Models**: ChatGLM-Pro, ChatGLM-Std, ChatGLM-Lite

**Get API Key**: https://open.bigmodel.cn/

**Pricing**: Competitive

**Best for**: Chinese language support

### Moonshot (Kimi)

**Models**: Moonshot-V1-8K, Moonshot-V1-32K, Moonshot-V1-128K

**Get API Key**: https://platform.moonshot.cn/

**Pricing**: Competitive

**Best for**: Long-context translation

### Alibaba Qwen

**Models**: Qwen-Turbo, Qwen-Plus, Qwen-Max

**Get API Key**: https://dashscope.aliyun.com/

**Pricing**: Enterprise-grade

**Best for**: Asian languages

### Huawei Cloud MaaS

**Models**: DeepSeek-V3.2, and others

**Get API Key**: https://www.huaweicloud.com/product/modelarts.html

**Pricing**: Pay-per-use

**Best for**: Enterprise users, Chinese market

## Troubleshooting (故障排除)

### Common Issues (常见问题)

#### 1. "Input file does not exist"

**Solution**: Check the file path and ensure the file exists.

#### 2. "API request timed out"

**Possible causes**:
- Computer went to sleep/hibernate
- Network connection issue
- API server overload

**Solutions**:
- Wake up computer and retry
- Check network connection
- Try a smaller batch size

#### 3. "Connection error"

**Solution**: Check your internet connection and firewall settings.

#### 4. "Invalid API key"

**Solution**: Verify your API key is correct and has sufficient credits.

#### 5. PO file syntax errors

**Solution**: Use a PO file editor (like Poedit) to fix syntax errors before translation.

### Performance Tips (性能建议)

1. **Use appropriate batch size**: Smaller batches for unstable networks
2. **Choose the right model**: Balance quality and speed
3. **Check API limits**: Stay within rate limits
4. **Monitor progress**: Watch for errors and retry if needed

## FAQ (常见问题)

### Q: Is PO Translator free?

A: Yes, PO Translator is free and open-source under GPL v2 license. However, you need to pay for API usage from providers.

### Q: Which API provider should I use?

A: It depends on your needs:
- **Best quality**: OpenAI GPT-4 or higher
- **Best value**: DeepSeek
- **Best for Chinese**: Zhipu AI or Alibaba Qwen
- **Enterprise**: Huawei Cloud MaaS

### Q: How long does translation take?

A: It depends on:
- Number of entries
- Batch size
- API response time
- Network speed

Example: 100 entries with batch size 20 typically takes 1-2 minutes.

### Q: Can I translate multiple PO files at once?

A: Currently, you need to translate files one by one. Batch file processing may be added in future versions.

### Q: Are my API keys safe?

A: API keys are stored locally in `config.json`. Never share this file or commit it to version control.

### Q: Can I use a custom API endpoint?

A: Yes! Select "Custom API" as the provider and enter your custom API URL.

### Q: What if my PO file has syntax errors?

A: Use a PO file editor like Poedit to fix syntax errors before translation.

### Q: Can I contribute to this project?

A: Yes! We welcome contributions. Please see our GitHub repository for guidelines.

## Support (支持)

For questions and support:
- GitHub Issues: https://github.com/franklifang/po-translator/issues
- Email: support@zokin.com
- Website: https://www.zokin.com

---

**Version**: 1.0.0  
**Last Updated**: 2026  
**Author**: LI, Fang (黎昉)  
**Organization**: Zokin Design, LLC. (上海左晶多媒体设计有限公司)
