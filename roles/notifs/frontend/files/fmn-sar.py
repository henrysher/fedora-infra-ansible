#!/usr/bin/env python
"""
GDPR SAR script for FMN.

Extract all preferences from a selected username and prints them in JSON to the
standard output.
"""

from __future__ import absolute_import, unicode_literals, print_function

import argparse
import json
import logging
import os
import sys

import requests
from six.moves.urllib.parse import urljoin


ENV_USERNAME = "SAR_USERNAME"
FMN_INSTANCE = "http://localhost/notifications/"
FMN_CONTEXTS = ["email", "irc"]

log = logging.getLogger()


def get_prefs(username, context):
    url = urljoin(
        FMN_INSTANCE,
        "api/{username}.id.fedoraproject.org/{context}/".format(
            username=username, context=context
        )
    )
    response = requests.get(url)
    if response.status_code >= 300:
        log.error("Could not get URL %s: %d %s",
                  url, response.status_code, response.reason)
        return {}
    result = response.json()
    return result


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        username = os.environ[ENV_USERNAME]
    except KeyError as e:
        print("Missing environment variable. {}".format(e), file=sys.stderr)
        sys.exit(1)
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.WARNING,
        stream=sys.stderr,
    )
    result = {}
    for context in FMN_CONTEXTS:
        result[context] = get_prefs(username, context)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
