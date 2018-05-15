#!/usr/bin/env python
"""
GDPR SAR script for HyperKitty.

Extract all emails from a selected address and prints them in JSON to the
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


ENV_EMAIL = "SAR_EMAIL"
HYPERKITTY_INSTANCE = "http://localhost/archives/"

log = logging.getLogger()


def get_emails(address):
    url = urljoin(HYPERKITTY_INSTANCE, "api/sender/{}/emails/".format(address))
    result = {"next": url}
    count = None
    email_urls = []
    while result.get("next"):
        url = result["next"]
        response = requests.get(url)
        if response.status_code >= 300:
            log.error("Could not get URL %s: %d %s",
                      url, response.status_code, response.reason)
            break
        result = response.json()
        if count is None:
            count = result["count"]
        email_urls.extend([e["url"] for e in result["results"]])
    if count != len(email_urls):
        log.error("Mismatch in the number of emails: got %s but there are "
                  "%s in total.", len(email_urls), count)
        raise ValueError
    emails = []
    for url in email_urls:
        response = requests.get(url)
        result = response.json()
        emails.append(result)
    return emails


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true")
    return parser.parse_args()


def main():
    args = parse_args()
    try:
        email = os.environ[ENV_EMAIL]
    except KeyError as e:
        print("Missing environment variable. {}".format(e), file=sys.stderr)
        sys.exit(1)
    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.WARNING,
        stream=sys.stderr,
    )
    emails = get_emails(email)
    print(json.dumps(dict(
        emails=emails, count=len(emails),
    ), indent=2))


if __name__ == "__main__":
    main()
