#!/usr/bin/python3

import os
import sys

from mailman.core.initialize import initialize
from mailman.config import config
from mailman.interfaces.pending import IPendings
from mailman.interfaces.requests import IListRequests, RequestType
from zope.component import getUtility


def clean_pended():
    getUtility(IPendings).evict()


if __name__ == '__main__':
    if os.getuid() == 0:
        print("This script must be run as the mailman user", file=sys.stderr)
        sys.exit(1)
    initialize(config_path="/etc/mailman.cfg")
    clean_pended()
    config.db.commit()
