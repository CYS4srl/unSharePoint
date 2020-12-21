#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2020 CYS4 Srl
See the file 'LICENSE' for copying permission
"""

class Target:
    _instance = None
    # instance target var
    server = None
    sharepoint = None
    technology = None
    cves = None
    url = None
    credentials = None
    found_users = None

    def __new__(cls, url=None):
        if cls._instance is None:
            cls._instance = super(Target, cls).__new__(cls)
            cls._instance.init_target(url)

        return cls._instance

    def init_target(self, url):
        self.url = url
        self.cves = []
        self.credentials = []
        self.found_users = []


    def to_string(self):

        final_string = "\n" * 2

        final_string += "Server type:"
        final_string += "-- %s" % self.server
        final_string += "\n" * 2

        final_string += "Server technology:"
        final_string += "-- %s" % self.technology
        final_string += "\n" * 2

        final_string += "Sharepoint detected information"
        final_string += "\n"
        final_string += "-- Version: %s" % self.sharepoint["version"]
        final_string += "\n"
        final_string += "-- Date: %s" % self.sharepoint["date"].strftime("%m/%d/%Y, %H:%M:%S")

        final_string += "\n"
        final_string += "-- Vulnerabilites found: %d" % len(self.cves) 
        final_string += "\n"

        for cve in self.cves:
            final_string += "--- %s" % cve
            final_string += "\n"
            final_string += "----- Severity:%s" % self.cves[cve]["severity"]
            final_string += "\n"
            final_string += "----- Impact:%s" % self.cves[cve]["impact"]
            final_string += "\n"
            if("link" in self.cves[cve]):
                final_string += "----- PoC link:%s" % self.cves[cve]["link"]
                final_string += "\n"

        final_string += "\n"*2
        final_string += "-- Found credentials: %d" % len(self.credentials)
        final_string += "\n"

        for credential in self.credentials:
            final_string += "--- Username:%s" % credential["username"]
            final_string += "\n"
            final_string += "--- Password:%s" % credential["password"]
            final_string += "\n"

        final_string += "\n"*2
        final_string += "-- Found users: %d" % len(self.found_users)
        final_string += "\n"

        for user in self.found_users:
            for user_attr in user:
                final_string += "---- %s:%s" % (user_attr,user[user_attr])
                final_string += "\n"

        return final_string