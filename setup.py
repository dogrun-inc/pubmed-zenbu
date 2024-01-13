#!/usr/bin/env python
# The MIT License (MIT)
# https://zenn.dev/sikkim/articles/490f4043230b5a
# python3 setup.py bdist_wheel
# twine upload --skip-existing dist/* で.pypircに記載されているusername(token)とpassword(API-key)情報を入力


from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

DESCRIPTION = 'PubmedZenbu' # Tools description
NAME = 'PubmedZenbu'
AUTHOR = 'Sora Yonezawa, Mitsuo Shintani, Naoya Oec, Takayuki Suzuki'
AUTHOR_EMAIL = 'oec@dogrun.jp' # Suzuki-san's email address
URL = 'https://github.com/dogrun-inc/pubmed-zenbu/tree/2023_dev_suzuki'
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'
LICENSE = 'MIT' # MIT License
DOWNLOAD_URL = URL
VERSION = '0.3.5' # Version number
PYTHON_REQUIRES = '>=3.9'
INSTALL_REQUIRES = [
    'requests>=2.31',
    'openai<=0.28.1',
    'PyYAML>=5.1',
    'Pandas>=2.0.0'
]
KEYWORDS = 'pubmed scraping article dogrun'
CLASSIFIERS=[
    'License :: OSI Approved :: MIT License', # MIT License
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11'
]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type=LONG_DESCRIPTION_CONTENT_TYPE,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=AUTHOR,
    maintainer_email=AUTHOR_EMAIL,
    url=URL,
    download_url=URL,
    classifiers=CLASSIFIERS,
    license=LICENSE,
    keywords=KEYWORDS,
    install_requires=INSTALL_REQUIRES,
    entry_points={
        "console_scripts": [
            "pubmedzenbu=PubmedZenbu.PubmedZenbu:main" #main関数の指定
        ]
    },
    packages=find_packages(include=['PubmedZenbu', 'PubmedZenbu.*'])
)
