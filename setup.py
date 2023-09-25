#!/usr/bin/env python
# The MIT License (MIT)
# https://zenn.dev/sikkim/articles/490f4043230b5a


from setuptools import setup

DESCRIPTION = '' # Tools description
NAME = 'pubmed_zenbu'
AUTHOR = 'Takayuki Suzuki'
AUTHOR_EMAIL = '' # Suzuki-san's email address
URL = 'https://github.com/dogrun-inc/pubmed-zenbu'
LICENSE = '' # MIT License ? 
DOWNLOAD_URL = URL
VERSION = '' # Version number
PYTHON_REQUIRES = '>=3.9' 
INSTALL_REQUIRES = [
    'pytz>=' # This is Timezone library
]
PACKAGES = [
    'pubmed_zenbu'
]
KEYWORDS = 'pubmed scraping article dogrun'
CLASSIFIERS=[
    'License :: OSI Approved :: MIT License', # MIT License ?
    'Programming Language :: Python :: 3.9' 
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