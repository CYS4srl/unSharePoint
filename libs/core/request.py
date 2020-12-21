#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2020 CYS4 Srl
See the file 'LICENSE' for copying permission
"""

import requests
from requests_ntlm2 import HttpNtlmAuth

from libs.core import constants
from libs.core.logger import Logger


class Request:
    _instance = None
    session = None
    logger = None

    def __new__(cls, domain=None, username=None, password=None):
        # Creating Logger as a Singleton and init the colored output
        if cls._instance is None:
            cls._instance = super(Request, cls).__new__(cls)
            cls._instance.init_requests(domain, username, password)
        return cls._instance

    def init_requests(self, domain, username, password):
        self.logger = Logger().get_logger()
        # create the sessions object for the requests
        self.session = requests.Session()
        self.session.verify = False

        # update the ua flag
        self.session.headers.update({'User-Agent': constants.USER_AGENT})

        # check if we have to add the auth to our requests
        if username and password:
            if domain:
                username = '%s\\%s' % (domain, username)
            self.session.auth = HttpNtlmAuth(username, password)

    def request_get(self, url):
        self.logger.debug("request_get")
        try:
            r = self.session.get(url, timeout=constants.REQUESTS_TIMEOUT)

            # close the connection
            r.close()
        except requests.exceptions.Timeout:
            raise ValueError("Request timed out, server is unreachable.")

        return r

    def request_post(self, url, json):
        self.logger.debug("request_post")
        try:
            r = self.session.post(url, timeout=constants.REQUESTS_TIMEOUT, json=json)

            # close the connection
            r.close()
        except requests.exceptions.Timeout:
            raise ValueError("Request timed out, server is unreachable.")

        return r
