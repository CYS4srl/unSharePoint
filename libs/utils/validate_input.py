#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2020 CYS4 Srl
See the file 'LICENSE' for copying permission
"""

import argparse
import re


# Module to check errors in parsed parameters
def check_url(url):
    regex = re.compile(
        r'^(?:http)s?:/\/'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[(([0-9a-fA-F]{1,4}:){7,7}[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,7}:|([0-9a-fA-F]{1,4}:){1,6}:[0-9a-fA-F]{1,4}|([0-9a-fA-F]{1,4}:){1,5}' \
        r'(:[0-9a-fA-F]{1,4}){1,2}|([0-9a-fA-F]{1,4}:){1,4}(:[0-9a-fA-F]{1,4}){1,3}|([0-9a-fA-F]{1,4}:){1,3}(:[0-9a-fA-F]{1,4}){1,4}|([0-9a-fA-F]{1,4}:)' \
        r'{1,2}(:[0-9a-fA-F]{1,4}){1,5}|[0-9a-fA-F]{1,4}:((:[0-9a-fA-F]{1,4}){1,6})|:((:[0-9a-fA-F]{1,4}){1,7}|:)|fe80:(:[0-9a-fA-F]{0,4}){0,4}%[0-9a-zA-Z]' \
        r'{1,}|::(ffff(:0{1,4}){0,1}:){0,1}((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])|([0-9a-fA-F]{1,4}:){1,4}'\
        r':((25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9])\.){3,3}(25[0-5]|(2[0-4]|1{0,1}[0-9]){0,1}[0-9]))\])' # ... or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

    if not isinstance(url, str) or re.match(regex, url) is None:
        raise argparse.ArgumentTypeError("{} is not a valid URL.".format(url))

    return url


def check_domain(domain):
    regex = re.compile(
        r'^[A-Za-z0-9\\\._-]{1,}$', re.IGNORECASE)

    if not isinstance(domain, str) or re.match(regex, domain) is None:
        raise argparse.ArgumentTypeError("{} is not a valid domain.".format(domain))

    return domain


def check_port(port):
    try:
        port = int(port)
        if not isinstance(port, int) or port not in range(1, 65536):
            raise argparse.ArgumentTypeError("{} is not a valid port.".format(port))
    except ValueError:
        raise argparse.ArgumentTypeError(
            "{} is not a valid port (must be an integer between 1 and 65535).".format(port))
    return port


def check_scan_type(scan_type):
    allowed_scans = ["i", "a", "ad", "f"]
    if not isinstance(scan_type, str) or scan_type.lower() not in allowed_scans:
        raise argparse.ArgumentTypeError(
            ("{} is not a valid scan type (must be %s )." % ",".join(allowed_scans)).format(scan_type))
    return scan_type


def check_username(username):
    if not isinstance(username, str) or len(username) not in range(1, 32):
        raise argparse.ArgumentTypeError(
            "{} is not a valid username (must be a string of max 32 and minimum 1 characters).".format(username))
    return username


def check_password(password):
    if not isinstance(password, str) or len(password) not in range(1, 64):
        raise argparse.ArgumentTypeError(
            "{} is not a valid password (must be a string of max 64 and minimum 1 characters).".format(password))
    return password


def check_auth(username, password):
    if not username and not password:
        return False
    elif not username:
        raise argparse.ArgumentTypeError("Username is needed if you provide credentials.")
    elif not password:
        raise argparse.ArgumentTypeError("Password is needed if you provide credentials.")
    return True
