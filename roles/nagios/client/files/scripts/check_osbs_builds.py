#!/usr/bin/python

import subprocess
import sys

sp = subprocess.Popen(
    ["osbs", "list-builds"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    stdin=subprocess.PIPE
)
sp_out, sp_err = sp.communicate()
sp_err = sp_err.split('\n')

if 'not attached to terminal' in sp_err[0]:
    sp_err = sp_err[1:]

if sp_err[0].split()[0] == 'BUILD':
    print "OK: OSBS is responsive to 'osbs list-builds'"
    sys.exit(0)
else:
    print "CRITICAL: OSBS UNRESPONSIVE"
    sys.exit(2)
