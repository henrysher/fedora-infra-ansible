#!/usr/bin/python

import subprocess
import sys

sp = subprocess.Popen(
    ["osbs", "list-builds"],
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)
sp_out, sp_err = sp.communicate()

if sp_err.split()[0] == 'BUILD':
    print "OK: OSBS is responsive to 'osbs list-builds'"
    sys.exit(0)
else:
    print "CRITICAL: OSBS UNRESPONSIVE"
    sys.exit(2)

