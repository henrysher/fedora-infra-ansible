#!/usr/bin/env python
""" Save the staging modules/ pkgdb entries to a local json file.

Use this script to save pkgdb modules/ entries in staging before wiping the db.
"""

import json

import requests

filename = 'old-modules.json'

response = requests.get(
    'https://admin.stg.fedoraproject.org/pkgdb/api/packages/',
    params=dict(namespace='modules'),
)
data = response.json()
with open(filename, 'wb') as f:
    f.write(json.dumps(data).encode('utf-8'))

print "Wrote %s" % filename
