"""
PO Translator (PO翻译器) - Setup Configuration
An application for translating .PO files using cloud AI APIs

Copyright (C) 2026 LI, Fang (黎昉)
Copyright (C) 2026 Zokin Design, LLC. (上海左晶多媒体设计有限公司)

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="po-translator",
    version="1.0.0",
    author="LI, Fang (黎昉)",
    author_email="support@zokin.com",
    description="An application for translating .PO files using cloud AI APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/franklifang/po-translator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Software Development :: Localization",
        "Topic :: Text Processing :: Linguistic",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Microsoft :: Windows :: Windows 7",
        "Operating System :: Microsoft :: Windows :: Windows 8",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "polib==1.2.0",
        "requests==2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "po-translator=src.main:main",
        ],
    },
    keywords="po translation localization i18n l10n ai openai deepseek",
    project_urls={
        "Bug Reports": "https://github.com/franklifang/po-translator/issues",
        "Source": "https://github.com/franklifang/po-translator",
        "Documentation": "https://github.com/franklifang/po-translator/blob/main/docs/USER_GUIDE.md",
    },
)
