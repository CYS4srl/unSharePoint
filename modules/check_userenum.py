#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2020 CYS4 Srl
See the file 'LICENSE' for copying permission
"""

from bs4 import BeautifulSoup

from libs.core.logger import Logger
from libs.core.request import Request
from libs.core.target import Target

import libs.core.constants as constants


class UserEnum:
    
    _instance = None
    logger = None
    target = None
    request = None

    def __new__(cls):
        # Creating Logger as a Singleton and init the colored output
        if cls._instance is None:
            cls._instance = super(UserEnum, cls).__new__(cls)
            cls._instance.init_userenum()
        return cls._instance

    def init_userenum(self):
        self.logger = Logger().get_logger()
        self.target = Target()
        self.request = Request()

    def user_enumeration(self):
        self.logger.debug("user_enumeration")
        url = "%s%s" % (self.target.url,constants.SHAREPOINT_SITEUSER_API_URL)

        # Starting User Enumeration
        try:
            r = self.request.request_get(url)
            if r.status_code != '200':
                self.logger.warning("User enumeration API is unreachable or current account is not authorized :(")
            else:
                xml = BeautifulSoup(r.text.encode("utf-8"), "lxml")
                for child in xml.find_all("m:properties"):

                    info_sid_issuer = child.find("d:userid")
                    found_user = {}
                    found_user["login name"] = child.find("d:loginname").text
                    found_user["title"] = child.find("d:title").text
                    found_user["isSiteAdmin"] = child.find("d:issiteadmin").text
                    if [t_child for t_child in info_sid_issuer.children]:
                        found_user["sid"] = info_sid_issuer.find("d:nameid").text
                        found_user["issuer"] = info_sid_issuer.find("d:nameidissuer").text
                    self.target.found_users.append(found_user)
                    self.logger.info("#################")
                    for key in found_user:
                        logger.info("%s : %s" (key,found_user[key]))
                    self.logger.info("#################")

        except Exception:
            raise ValueError("Unhandled exception in user_enumeration.")
