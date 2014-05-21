#!/usr/bin/python -tt

import yum
import sys
import time
import fnmatch

result = 0
now = time.time()
uptime = float(open('/proc/uptime', 'r').read().split()[0])

rebootcausers = ('glibc', 'kernel*')

my = yum.YumBase()
my.preconf.init_plugins=False
my.preconf.debuglevel=1
my.preconf.errorlevel=1
pkgs = my.rpmdb.returnPackages(patterns=rebootcausers)

does='no'
for pkg in pkgs:
    if (now - pkg.installtime) < uptime:
        does='yes'
        break

if len(sys.argv) > 1 and sys.argv[1] == 'after-updates':
    for (n, a, e, v, r) in my.up.getUpdatesList():
        for i in rebootcausers:
            if fnmatch.fnmatch(n, i):
                does='yes'


print does
sys.exit(0)


