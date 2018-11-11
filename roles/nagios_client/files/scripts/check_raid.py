#!/usr/bin/env python
#
# very simple python script to parse out /proc/mdstat
# and give results for nagios to monitor
#

import sys
import string

devices = []

try:
    mdstat = string.split(open('/proc/mdstat').read(), '\n')
except IOError:
    # seems we have no software raid on this machines
    sys.exit(0)

error = ""
i = 0
for line in mdstat:
    if line[0:2] == 'md':
        device = string.split(line)[0]
        devices.append(device)
        status = string.split(mdstat[i+1])[-1]
        if string.count(status, "_"):
            # see if we can figure out what's going on
            err = string.split(mdstat[i+2])
            msg = "device=%s status=%s" % (device, status)
            if len(err) > 0:
                msg = msg + " rebuild=%s" % err[0]

            if not error:
                error = msg
            else:
                error = error + ", " + msg
    i = i + 1

if not error:
    print "DEVICES %s OK" % " ".join(devices)
    sys.exit(0)

else:
    print error
    sys.exit(2)

