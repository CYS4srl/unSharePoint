#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2020 CYS4 Srl
See the file 'LICENSE' for copying permission
"""

import os
from datetime import datetime

from libs.core.logger import Logger
from libs.core.request import Request
from libs.core.target import Target
import libs.core.constants as constants

class Sharepoint:
    _instance = None
    logger = None
    target = None
    request = None

    def __new__(cls):
        # Creating Logger as a Singleton and init the colored output
        if cls._instance is None:
            cls._instance = super(Sharepoint, cls).__new__(cls)
            cls._instance.init_sharepoint()
        return cls._instance

    def init_sharepoint(self):
        self.logger = Logger().get_logger()
        self.target = Target()
        self.request = Request()

    def check_availability(self):
        self.logger.debug("check_availability")
        try:
            r = self.request.request_get(self.target.url)

            if r.status_code != 200:
                self.logger.warning("Please take attention, the target answered with %i code." % r.status_code)

        except Exception:
            raise ValueError("Unhandled error on check_availability().")

        return r

    def check_iis_target(self, headers):
        self.logger.debug("check_iis_target")
        # Detection by header parse
        detected_version_iis = detect_server_by_headers(headers)
        if detected_version_iis:
            self.target.server = detected_version_iis
            self.logger.debug("Server version Detected (headers parse): {}".format(detected_version_iis))

        # detect the technology if present
        detected_tec = detect_tec_by_headers(headers)
        if detected_tec:
            self.target.technology = detected_tec
            self.logger.debug("Technology detected (headers parse): {}".format(detected_tec))

    def check_share_point(self, headers):
        self.logger.debug("check_share_point")
        # Detection by header parse
        detected_version_share_point = self.detect_sharepoint_by_headers(headers)
        if detected_version_share_point:
            self.logger.debug("SharePoint version Detected (headers parse): {}".format(detected_version_share_point))

        # Detection by conf file parse #
        if not detected_version_share_point:
            detected_version_share_point = self.detect_sharepoint_by_servicefile()
            if detected_version_share_point:
                self.logger.debug(
                    "SharePoint version Detected (service.cnf parse): {}".format(detected_version_share_point))

        self.get_version(detected_version_share_point)



    def detect_sharepoint_by_headers(self, headers):
        self.logger.debug("detect_sharepoint_by_headers")
        useful_headers = [header for header in headers if "sharepoint" in header.lower()]
        if "MicrosoftSharePointTeamServices" in headers.keys():
            version = headers["MicrosoftSharePointTeamServices"].split(";")[0].split(":")[0]
            return version
        elif len(useful_headers) > 0:
            self.logger.warning(
                "Header %s was found, it may not bring the exact version." % headers[useful_headers[0]].replace("\r\n",
                                                                                                                ""))
        return None

    def detect_sharepoint_by_servicefile(self):
        self.logger.debug("detect_sharepoint_by_servicefile")
        version = None
        for service_url in constants.SHAREPOINT_SERVICE_URLS:
            try:

                # request the url and save the data into the session variable
                r = self.request.request_get(self.target.url + service_url)

                if r.status_code == 200:
                    if "vti_extenderversion" in r.text:
                        version = r.text.split("vti_extenderversion:SR|")[1].replace("\n", "")
                        break
                    if "vti_buildversion" in r.text:
                        version = r.text.split("vti_extenderversion:SR|")[1].replace("\n", "")
                        break

            except Exception:
                raise ValueError("Unhandled error detect_sharepoint_by_servicefile().")

        return version

    def get_version(self,patch_number):


        _patch_tokens = patch_number.split(".")
        _major_version = int(_patch_tokens[0])
        _minor_version = int(_patch_tokens[1])
        _build_version = int(_patch_tokens[3])
        _patch_number = "%s.%s.%s" % (_major_version,_minor_version,_build_version)
        _last_version = ""
        _last_date = ""
        db_version = {
            "version": "",
            "date": ""
        }



        with open('%s%sversions.csv' % (constants.DATABASE_FOLDER, os.path.sep),"r") as file_versions:

            for line in file_versions:

                _line_tokens = line.split(",")
                _checked_version = _line_tokens[0].split(".")
                _checked_version_date = _line_tokens[2]

                #### if there are not enough tokens, we skip it #######

                if(len(_checked_version)<4):
                    continue

                #### Extract major, minor and build version #######

                _checked_version_major = int(_checked_version[0])
                _checked_version_minor = int(_checked_version[1])
                _checked_version_build = int(_checked_version[2])

                #### reformat checked version date #######

                if(_checked_version_date!="N/A"):
                    _checked_version_date = datetime.strptime(_checked_version_date, "%Y %B %d")

                #### reformat checked version structure #######

                _checked_version = "%s.%s.%s" % (_checked_version_major,_checked_version_minor,_checked_version_build)

                #### check if we found a version #######

                if(_checked_version == _patch_number):
                    db_version["version"] = _checked_version
                    db_version["date"] = _checked_version_date
                    self.logger.info("Version details found.")
                    break

                #### if not a suitable version is found, we return the closer one (since they are ordered) #######

                if((_major_version > _checked_version_major) or (_major_version == _checked_version_major and _build_version > _checked_version_build)):

                    db_version["version"] = _checked_version
                    db_version["date"] = _checked_version_date
                    self.logger.info("Version could not be found, performing best guess.")
                    break

        self.target.sharepoint = db_version


def detect_server_by_headers(headers):
    if "Server" in headers.keys():
        return headers["Server"]
    return None


def detect_tec_by_headers(headers):
    if "X-Powered-By" in headers.keys():
        return headers["X-Powered-By"]
    return None



