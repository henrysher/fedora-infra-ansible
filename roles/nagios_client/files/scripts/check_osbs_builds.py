#!/usr/bin/python

import subprocess
import sys

sp = subprocess.Popen(
    ["oc", "-n", "osbs-fedora", "get", "builds"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    stdin=subprocess.PIPE
)
sp_out, sp_err = sp.communicate()
sp_out = sp_out.split('\n')

if sp_out[0].split()[0] == 'NAME':
    print "OK: OSBS is responsive to 'oc get builds'"
    sys.exit(0)
else:
    print "CRITICAL: OSBS UNRESPONSIVE"
    sys.exit(2)
