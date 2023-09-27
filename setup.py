#!/usr/bin/env python
# The MIT License (MIT)
# https://zenn.dev/sikkim/articles/490f4043230b5a


from setuptools import setup

DESCRIPTION = '- This tool extracts metadata from PubMed articles using ChatGPT. Inputs as a `search query for PubMed` and `prompt for ChatGPT`, output as a csv file including the extracted results. Positional arguments: arguments.csv (csv file including openai_api_key, ncbi_api_key, search_query, and prompt),oldest_year (oldest year to search for PubMed)' # Tools description
NAME = 'PubmedZenbu'
AUTHOR = 'Sora Yonezawa, Mitsuo Shintani, Naoya Oec, Takayuki Suzuki'
AUTHOR_EMAIL = 'oec@dogrun.jp' # Suzuki-san's email address
URL = 'https://github.com/dogrun-inc/pubmed-zenbu'
LICENSE = 'MIT' # MIT License
DOWNLOAD_URL = URL
VERSION = '0.1.0' # Version number
PYTHON_REQUIRES = '>=3.9'
INSTALL_REQUIRES = [
    'requests>=2.31.0',
    'openai>=0.28.1',
    'PyYAML>=6.0.1',
    'Pandas>=2.1.1'
]
PACKAGES = [
    'PubmedZenbu'
]
KEYWORDS = 'pubmed scraping article dogrun'
CLASSIFIERS=[
    'License :: OSI Approved :: MIT License', # MIT License
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11'
]
with open('README.md', 'r', encoding='utf-8') as fp:
    readme = fp.read()
LONG_DESCRIPTION = readme
LONG_DESCRIPTION_CONTENT_TYPE = 'text/markdown'

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
    packages=PACKAGES,
    classifiers=CLASSIFIERS,
    license=LICENSE,
    keywords=KEYWORDS,
    install_requires=INSTALL_REQUIRES
)
