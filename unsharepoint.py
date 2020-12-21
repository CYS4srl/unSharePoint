#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2020 CYS4 Srl
See the file 'LICENSE' for copying permission
"""

import sys
import urllib3
from libs.core.database import Database
from libs.core.logger import Logger
from libs.core.request import Request
from libs.core.target import Target
from libs.utils.banner import print_banner
from modules.check_cve import CheckCVE
from modules.check_bruteforce import BruteForce
from modules.check_sharepoint import Sharepoint
from modules.check_soap_api import CheckSoapApi
from modules.check_userenum import UserEnum
from modules.cmdline import gen_cli_args

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def main():
    # print banner
    print_banner()

    # init logger
    logger_instance = Logger()
    logger = logger_instance.get_logger()

    try:

        # init options and parse the arguments
        args = gen_cli_args()

        # set the verbose level if flagged
        if args.verbose:
            logger_instance.enable_debug()

        # init request and their auth if needed
        Request(args.domain, args.username, args.password)

        # init target
        tg = Target(args.url)

        # check if we need to update the database an verify the installation
        db = Database()
        if args.update:
            db.update()

        db.verify_installation()

        # check if the target is online
        sh = Sharepoint()

        # verify if the target is online or not
        response_obj = sh.check_availability()

        # check the headers in order to look into the technology and the server
        sh.check_iis_target(response_obj.headers)

        # check if we have a sharepoint or something else
        sh.check_share_point(response_obj.headers)

        # check cve based on the build number
        if tg.sharepoint:
            check_cve = CheckCVE()
            check_cve.get_cve()

        # verify if we have to to other checks
        if args.type != 'i':

            if args.type == 'a' or args.type == 'ad':
                # Api scan, checking SOAP stuff
                detailed = args.type == 'ad'
                soap_api = CheckSoapApi()
                soap_api.check_soap_api(detailed)


        if args.bruteforce:
            bt = BruteForce(args.domain, args.username_file, args.password_file)
            bt.bruteforce()

        if args.enum_users:
            ue = UserEnum()
            ue.user_enumeration()

        logger.info("Scan completed!")
        logger.info("Results:")
        logger.info(tg.to_string())



    except (KeyboardInterrupt, SystemExit):
        sys.exit(2)
    except Exception as e:
        logger.error(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
