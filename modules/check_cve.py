#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2020 CYS4 Srl
See the file 'LICENSE' for copying permission
"""

import os
from datetime import datetime

from libs.core.logger import Logger
from libs.core.database import Database
from libs.core.target import Target
import libs.core.constants as constants


class CheckCVE:

    _instance = None
    logger = None
    target = None
    db = None

    def __new__(cls):
        # Creating Logger as a Singleton and init the colored output
        if cls._instance is None:
            cls._instance = super(CheckCVE, cls).__new__(cls)
            cls._instance.init_checkcve()
        return cls._instance

    def init_checkcve(self):

        self.logger = Logger().get_logger()
        self.target = Target()
        self.db = Database()


    def get_cve(self):

        _version_tokens = self.target.sharepoint["version"].split(".")
        _version_date = self.target.sharepoint["date"]
        _version_major = int(_version_tokens[0])
        _version_minor = int(_version_tokens[1])
        _version_build = int(_version_tokens[2])
        _product_ids = constants.PRODUCT_IDS
        cve_list = {}

        #### setting _product_id ids parameters based on version (that is how Microsoft assigns CVEs to Sharepoint versions)

        if(_version_major == 16):
            if(_version_build < 10337):
                _product_ids.remove(11585) 
        if(_version_major < 16):
            _product_ids.remove(11585)
            _product_ids.remove(10917)
            _product_ids.remove(10950)
        if(_version_major < 15):
            _product_ids.remove(11099)
            _product_ids.remove(10612)
            _product_ids.remove(10607)

        ##### recovering CVE list 

        with open('%s%scves.csv' % (constants.DATABASE_FOLDER, os.path.sep),"r") as _file_cves:

            for line in _file_cves:

                _cve_details = line.split(",")

                #### If there are not enough details in this entry, we skip it

                if(len(_cve_details) < 5):

                    continue

                #### set up cve details

                _product_id = int(_cve_details[0])
                _cve_id = _cve_details[1]
                _cve_publication_date = datetime.strptime(_cve_details[2].split("T")[0], "%Y-%m-%d")
                _cve_poc_link = _cve_details[-1].rstrip()
                _cve_severity = _cve_details[4].rstrip()
                _cve_impact = _cve_details[5].rstrip()

                #### if the vulnerability has been published after a patch release, we add it

                if(_cve_publication_date > _version_date and _product_id in _product_ids):

                    cve_list[_cve_id] = {
                        "severity":_cve_severity,
                        "impact":_cve_impact
                    }

                    #### check if any poc link may be available
                    if(_cve_poc_link != "N/A"):

                        cve_list[_cve_id]["link"] = _cve_poc_link


        self.target.cves = cve_list
