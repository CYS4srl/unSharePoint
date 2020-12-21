#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2020 CYS4 Srl
See the file 'LICENSE' for copying permission
"""

import logging
import os
from datetime import datetime
from logging import FileHandler
from sys import stdout
from colorama import init, deinit, Fore

import libs.core.constants as constants



class Logger:
    _instance = None
    _logger = None


    def __new__(cls, logger_name=constants.LOG_NAME, path=constants.LOG_PATH, log_file_name=constants.LOG_FILE, do_console_logging=constants.CONSOLE_LOGGING,
                do_file_logging=constants.FILE_LOGGING):

        # Creating Logger as a Singleton and init the colored output
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.init_logger(logger_name, path, log_file_name, do_console_logging, do_file_logging)
        return cls._instance

    def init_logger(self, logger_name, path, log_file_name, do_console_logging, do_file_logging):

        #init colorama
        if os.name == 'nt':
            init(convert=True)
        else:
            init()

        # First instantiation
        main_logger = logging.getLogger(logger_name)
        main_logger.setLevel(logging.DEBUG)
        if do_console_logging:
            console_handler_debug = logging.StreamHandler(stdout)
            console_handler_debug.setLevel(logging.INFO)
            console_handler_debug.setFormatter(CustomFormatter())
            main_logger.addHandler(console_handler_debug)

        if do_file_logging:
            file_handler = FileHandler(os.path.join(path, log_file_name))
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(CustomFormatter.FILE_FORMATTER)
            main_logger.addHandler(file_handler)

        self._logger = main_logger


    def enable_debug(self):
        for i in range(len(self._logger.handlers)):
            self._logger.handlers[i].setLevel(logging.DEBUG)

    def get_logger(self):
        return self._logger

    # call the del in order to restore the output
    def __del__(self):
        deinit()


class CustomFormatter(logging.Formatter):


    def __init__(self):
        super().__init__(fmt=constants.CONSOLE_FORMATTER_INFO, datefmt=None, style='%')

    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            self._style._fmt = constants.CONSOLE_FORMATTER_DEBUG

        elif record.levelno == logging.INFO:
            self._style._fmt = constants.CONSOLE_FORMATTER_INFO

        elif record.levelno == logging.WARNING:
            self._style._fmt = constants.CONSOLE_FORMATTER_WARNING

        elif record.levelno == logging.ERROR:
            self._style._fmt = constants.CONSOLE_FORMATTER_ERROR

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result
