#!/usr/bin/python

import requests
import sys

r =  requests.get("https://localhost:8443/", verify=False)

if 'paths' in r.json().keys():
    print "OK: OSBS API endpoint is responding with path data"
    sys.exit(0)
else:
    print "CRITICAL: OSBS API not responding properly"
    sys.exit(2)

