#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2020 CYS4 Srl
See the file 'LICENSE' for copying permission
"""

try:
    import setuptools
except ImportError:
    print("[+] Error while importing setuptools")
    exit(1)

requirements = [
    'requests_ntlm2',
    'requests',
    'urllib3',
    'pyfiglet',
    'beautifulsoup4',
    'lxml',
    'zeep',
    'colorama'
]

setuptools.setup(
    name='unSharePoint',
    version='1.0',
    description='A tool created to ease SharePoint security assessments.',
    author='Davide Meacci',
    author_email='davide.meacci@cys4.com',
    maintainer='Davide Meacci',
    maintainer_email='davide.meacci@cys4.com',
    install_requires=requirements,
    license="BSD",
    zip_safe=False,
)