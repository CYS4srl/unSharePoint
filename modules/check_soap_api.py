#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2020 CYS4 Srl
See the file 'LICENSE' for copying permission
"""

from zeep import Client
from zeep import xsd
from zeep.transports import Transport

from libs.core.logger import Logger
from libs.core.request import Request
from libs.core.target import Target
import libs.core.constants as constants


class CheckSoapApi:
    
    _instance = None
    logger = None
    target = None
    request = None

    def __new__(cls):
        # Creating Logger as a Singleton and init the colored output
        if cls._instance is None:
            cls._instance = super(CheckSoapApi, cls).__new__(cls)
            cls._instance.init_soap_api()
        return cls._instance

    def init_soap_api(self):
        self.logger = Logger().get_logger()
        self.target = Target()
        self.request = Request()

    def check_soap_api(self, detailed):
        self.logger.debug("starting check_soap_api")
        url = self.target.url
        # TODO check more https://docs.microsoft.com/en-us/previous-versions/office/developer/sharepoint-2010/ms467069
        for path in constants.SHAREPOINT_ASMX_PATHS:
            self.check_soap_availability(constants.SHAREPOINT_ASMX_START_PATH % (url, path), detailed)
        for path in constants.SHAREPOINT_SVC_PATHS:
            self.check_soap_availability(constants.SHAREPOINT_SVC_START_PATH % (url, path), detailed)

    def check_soap_availability(self, url, detailed):
        self.logger.debug("starting check_soap_availability")
        try:
            # request the url and save the data into the session variable
            r = self.request.request_get(url)

            if r.status_code == 200:
                self.logger.info("%s is reachable :)." % url)
            elif r.status_code == 401:
                self.logger.warning("%s unauthorized :(." % url)
                return False
        except Exception:
            raise ValueError("Unhandled error check_soap_availability().")

        if detailed:
            client = Client(url, transport=Transport(session=self.request.session))
            for service in client.wsdl.services.values():
                for port in service.ports.values():
                    for operation in port.binding._operations.values():
                        parameters = {}
                        if operation.input.body:
                            for parameter in operation.input.body.type.elements:
                                parameters[parameter[0]] = xsd.SkipValue
                            with client.settings(raw_response=True):
                                response = client.service[operation.name](**parameters)
                                if str(response.status_code)[0] == "2":
                                    self.logger.info("--- Available method: %s" % operation.name)
                                if str(response.status_code)[0] == "5":
                                    self.logger.info("--- Maybe available (double check) method: %s" % operation.name)
