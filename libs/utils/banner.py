#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2020 CYS4 Srl
See the file 'LICENSE' for copying permission
"""

import random
import pyfiglet
from colorama import init, deinit, Fore, Style

import libs.core.constants as constants


def print_banner():
    # colorama
    init()

    print("\n")
    ascii_banner = pyfiglet.figlet_format("unSharePoint", font=random.choice(constants.BANNER_FONTS))
    print(random.choice(constants.BANNER_COLORS) + random.choice(constants.BANNER_STYLES) + constants.BANNER_DELIMITER + ascii_banner + constants.BANNER_DELIMITER)
    print("unSharePoint - A tool to ease SharePoint security assessments.")
    print("Authors: Davide Meacci (@WickdDavid) - Alessio Dalla Piazza(@alessiodallapiazza)\n")

    # colorama
    print(Style.RESET_ALL)
    deinit()
