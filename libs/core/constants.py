#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2020 CYS4 Srl
See the file 'LICENSE' for copying permission
"""

import os
import tempfile
import logging
from datetime import datetime
from colorama import init, deinit, Fore, Style


if os.name == 'nt':
  init(convert=True)
else:
  init()

# logging constants
LOG_FILE = datetime.now().strftime("%Y%m%d-%H%M%S-") + "unSharepoint.log"
LOG_NAME = "unSharepoint.logger"
LOG_PATH = tempfile.gettempdir()
CONSOLE_LOGGING = True
FILE_LOGGING = False
# log format constants
FILE_FORMATTER = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
CONSOLE_FORMATTER_INFO = Fore.CYAN + "[+] %(message)s\n"
CONSOLE_FORMATTER_WARNING = Fore.YELLOW + "[!] %(message)s\n"
CONSOLE_FORMATTER_DEBUG = Fore.LIGHTYELLOW_EX + "[*] %(message)s\n"
CONSOLE_FORMATTER_ERROR = Fore.RED + "[!] %(message)s\n"
# banner constants
BANNER_FONTS = ["standard", "alligator", "xbriteb", "cybersmall"]
BANNER_COLORS = [Fore.LIGHTBLACK_EX, Fore.CYAN, Fore.MAGENTA]
BANNER_STYLES = [Style.DIM, Style.BRIGHT, Style.NORMAL]
BANNER_DELIMITER = "#" * 70 + "\n"
# timeout in seconds in order to validate a URL
REQUESTS_TIMEOUT = 30
# url used to build the version number
VERSION_URL = "https://buildnumbers.wordpress.com/sharepoint/"
# urls used to map the securities of the cves
BUILD_URL = "https://portal.msrc.microsoft.com/api/security-guidance/en-us"
CVE_URL = "https://cve.mitre.org/cgi-bin/cvename.cgi?name=%s"
# ua string used for the requests
# database url from github repo
DB_VERSION_URL = "https://raw.githubusercontent.com/WickdDavid/unSharePoint/master/db/versions.csv"
DB_CVE_URL = "https://raw.githubusercontent.com/WickdDavid/unSharePoint/master/db/cves.csv"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko"
# folder database
DATABASE_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + os.path.sep + "db"
# default product ids
PRODUCT_IDS = [
    11099,  # Sharepoint 2013 Enterprise SP1
    10950,  # Sharepoint 2016 Enterprise
    10505,  # Sharepoint 2010 SP1
    10612,  # Sharepoint 2013 Foundation SP1
    10495,  # Sharepoint 2010 SP2
    10607,  # Sharepoint 2013 Server SP1
    10917,  # Sharepoint 2016 Server
    11585  # Sharepoint 2019 Server
]
# default sharepoint service urls
SHAREPOINT_SERVICE_URLS = [
	"/_vti_pvt/service.cnf", 
  "/_vti_pvt/buildversion.cnf",
	"/wss/VirtualDirectories/24017/_vti_pvt/service.cnf"
]
# default sharepoint url (used on bruteforce)
SHAREPOINT_DEFAULT_URL = "/SitePages/Home.aspx"
# default paths for .asmx and .svc files
SHAREPOINT_ASMX_START_PATH = "%s/_vti_bin/%s.asmx?WSDL"
SHAREPOINT_ASMX_PATHS = ["admin", "alerts", "Copy", "Diagniostics", "DspSts", "DWS", "Forms", "Imaging", "Lists",
              "Meetings",
              "People", "Permissions", "PublishedLinksService", "SharedAccess", "Sharepointemailws", "SiteData",
              "Sites", "spsearch", "search", "SocialDataService", "usergroup", "userprofileservice",
              "UserProfileChangeService", "Versions", "Views", "Webpartpages", "Webs"]
SHAREPOINT_SVC_START_PATH = "%s/_vti_bin/%s.svc/mex?wsdl"              
SHAREPOINT_SVC_PATHS = ["Bdcadminservice", "BdcRemoteExecutionService", "BDCResolverPickerService", "bdcservice", "client",
             "CellStorage", "securitytoken", "spclaimproviderwebservice", "topology", "windowstokencache"]
# default sharepoint url for user enumeration
SHAREPOINT_SITEUSER_API_URL = "/_api/web/siteusers"