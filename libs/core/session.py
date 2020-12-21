#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2020 CYS4 Srl
See the file 'LICENSE' for copying permission
"""

import requests

class SessionSingleton:
    class __SessionSingleton:
        def __init__(self, session, url):
            if(session and url):
                self.session = session
                self.url = self.url
            else:
                self.session = requests.Session()
                self.url = url
        def __str__(self):
            return repr(self) + self.session
    instance = None
    def __init__(self,session=None,url=None):
        if not SessionSingleton.instance:
            SessionSingleton.instance = SessionSingleton.__SessionSingleton(session, url)
        elif(session and url):
            SessionSingleton.instance.session = session
            SessionSingleton.instance.url = url
    def __getattr__(self, session):
        return getattr(self.instance, session)
    def getSessionSingleton(self):
        return self.instance.session
    def getUrlSingleton(self):
    	return self.instance.url