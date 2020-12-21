#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2020 CYS4 Srl
See the file 'LICENSE' for copying permission
"""

import argparse


# This class wrap the error message and print again the help message
class WrapperArgs(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)
