#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2020 CYS4 Srl
See the file 'LICENSE' for copying permission
"""

import os
import requests

import libs.core.constants as constants
from libs.core.logger import Logger


class Database:
    _instance = None
    logger = None

    def __new__(cls):
        # Creating Logger as a Singleton and init the colored output
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.init_database()
        return cls._instance

    def init_database(self):
        self.logger = Logger().get_logger()

    def verify_installation(self):
        self.logger.debug("Check if the constants.DATABASE_FOLDER exist.")
        if not os.path.exists(constants.DATABASE_FOLDER):
            raise ValueError("Please run the update flag in order to create the folder db.")

        # check if our database exist
        if not os.path.exists('%s%sversions.csv' % (constants.DATABASE_FOLDER, os.path.sep)):
            raise ValueError('Please run the update flag in order to create the version db.')

        # check if our database exist
        if not os.path.exists('%s%scves.csv' % (constants.DATABASE_FOLDER, os.path.sep)):
            raise ValueError('Please run the update flag in order to create the CVE db.')

    def update(self):
        self.logger.info("Running database update.")
        try:
                    r = requests.get(constants.DB_VERSION_URL, timeout=constants.REQUESTS_TIMEOUT)
                    with open('%s%scves.csv' % (constants.DATABASE_FOLDER, os.path.sep), 'wb') as f:
                        f.write(r.content)
        except Exception:
            raise ValueError("Error while retrieving versions file.")

        try:
                    r = requests.get(constants.DB_CVE_URL, timeout=constants.REQUESTS_TIMEOUT)
                    with open('%s%sversions.csv' % (constants.DATABASE_FOLDER, os.path.sep), 'wb') as f:
                        f.write(r.content)
        except Exception:
            raise ValueError("Error while retrieving versions file.")    
        self.logger.info("Database updated.")