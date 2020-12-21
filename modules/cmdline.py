#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Copyright (C) 2020 CYS4 Srl
See the file 'LICENSE' for copying permission
"""

import sys

from libs.core.wrapperargs import WrapperArgs
from libs.utils import validate_input


def validate(args):

    if not args.url:
        raise ValueError("The target is not specified.")

    if args.url[-1] == "/":
        args.url = args.url[:-1]

    if not args.type:
        args.type = "i"

    auth_check = validate_input.check_auth(args.username, args.password)
    if args.domain and not auth_check:
        raise ValueError("Domain, Username or Password were not set correctly.")

    if args.bruteforce:
        if not args.username_file or not args.password_file:
            raise ValueError("If you specify the bruteforce param please give an username and password file")


def gen_cli_args(argv=None):
    """
    This function parses the command line parameters and arguments
    """

    if not argv:
        argv = sys.argv

    parser = WrapperArgs()

    parser.add_argument(
        '--url', type=validate_input.check_url, help='target URL to analyze', required=False)
    parser.add_argument(
        '-t', '--type', type=validate_input.check_scan_type,
        help='scan type (\'i\': info / \'a\': api / \'ad\': api-detailed)', required=False)
    parser.add_argument(
        '-d', '--domain', type=validate_input.check_domain, help='username to perform login (NTLM auth).',
        required=False)
    parser.add_argument(
        '-u', '--username', type=validate_input.check_username, help='username to perform login (NTLM auth).',
        required=False)
    parser.add_argument(
        '-p', '--password', type=validate_input.check_password, help='password to perform login (NTLM auth).',
        required=False)

    # Brute force options
    brute = parser.add_argument_group("Brute force", "These options can be used to run brute force checks.")

    brute.add_argument("--bruteforce", dest="bruteforce", action="store_true",
                       help="Check existence of valid combination of username and passwords from file.")
    brute.add_argument("--enum-users", dest="enum_users", action="store_true",
                       help="Check existence of common users from the api, if exposed.")
    brute.add_argument("--username-file", dest="username_file",
                       help="Username's file")
    brute.add_argument("--password-file", dest="password_file",
                       help="Password's file")

    parser.add_argument(
        '-o', '--output', action='store_true', help='output logs in temp folder.', required=False)
    parser.add_argument(
        '--update', action='store_true', help='Update the CVE e Build database.', required=False)
    parser.add_argument(
        "--verbose", action="store_true", help="increase output verbosity", required=False)

    if len(argv) == 1:
        parser.print_help()
        sys.exit(2)

    args = parser.parse_args()

    validate(args)

    return args
