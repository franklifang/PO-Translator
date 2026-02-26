# Contributing to PO Translator

Thank you for your interest in contributing to PO Translator! This document provides guidelines and instructions for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

This project and everyone participating in it is governed by the principles of open-source collaboration. By participating, you are expected to uphold this code. Please be respectful, inclusive, and constructive in all interactions.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:
- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, PO Translator version)
- Log output if applicable

### Suggesting Enhancements

We welcome suggestions for improvements! Please open an issue with:
- Clear description of the enhancement
- Use case and benefits
- Possible implementation approach

### Pull Requests

We actively welcome pull requests! Please follow the process below.

## Development Setup

### Prerequisites

- Python 3.7 or higher
- Git
- A code editor (VS Code, PyCharm, etc.)

### Setup Steps

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR_USERNAME/po-translator.git
   cd po-translator
   ```

3. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/macOS
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Follow coding standards
   - Add tests if applicable
   - Update documentation

3. **Test your changes**
   ```bash
   # Run the application
   python src/main.py
   
   # Test with different scenarios
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: Brief description of your changes"
   ```

5. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Open a Pull Request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Fill in the PR template
   - Submit the PR

### Commit Message Format

Use clear, descriptive commit messages:

- `Add: New feature`
- `Fix: Bug fix`
- `Update: Update existing feature`
- `Refactor: Code refactoring`
- `Docs: Documentation changes`
- `Test: Adding tests`

## Coding Standards

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use meaningful variable and function names
- Add docstrings to functions and classes

### Code Organization

```
po-translator/
├── src/
│   ├── main.py           # GUI application
│   └── po_translator.py  # Core translation engine
├── docs/                 # Documentation
├── .github/              # GitHub templates
├── requirements.txt      # Dependencies
├── README.md            # Project README
├── CHANGELOG.md         # Version history
└── CONTRIBUTING.md      # This file
```

### Best Practices

1. **Keep functions small and focused**
2. **Add comments for complex logic**
3. **Handle errors gracefully**
4. **Use type hints where appropriate**
5. **Follow DRY (Don't Repeat Yourself) principle**

## Testing

### Manual Testing

Before submitting a PR, test your changes with:

1. **Different PO files**
   - Small files (< 10 entries)
   - Medium files (10-100 entries)
   - Large files (> 100 entries)

2. **Different API providers**
   - OpenAI
   - DeepSeek
   - Other providers

3. **Edge cases**
   - Empty PO files
   - Files with syntax errors
   - Network issues
   - API errors

### Test Scenarios

- [ ] Translation completes successfully
- [ ] Progress updates correctly
- [ ] Error handling works
- [ ] Configuration saves/loads correctly
- [ ] GUI is responsive during translation
- [ ] Stop button works correctly

## Documentation

### When to Update Documentation

- Adding new features
- Changing existing behavior
- Fixing bugs that affect user experience
- Adding new API providers

### Documentation Files

- **README.md**: Project overview, installation, basic usage
- **docs/USER_GUIDE.md**: Detailed user guide
- **CHANGELOG.md**: Version history
- **Code comments**: Inline documentation

### Documentation Style

- Use clear, simple language
- Include code examples
- Add screenshots for UI features
- Keep it up-to-date

## Getting Help

If you need help or have questions:

- Open an issue on GitHub
- Email: support@zokin.com
- Check existing documentation

## License

By contributing to PO Translator, you agree that your contributions will be licensed under the GPL v2 License.

---

Thank you for contributing to PO Translator! 🎉

**Author**: LI, Fang (黎昉)  
**Organization**: Zokin Design, LLC. (上海左晶多媒体设计有限公司)
