#!/usr/bin/env python

import socket
import sys


try:

    unixsocket="/var/run/haproxy-stat"
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect(unixsocket)
    s.send('show stat\n')

    try:

        output = s.recv(16384).strip().split('\n')
	fields = output.pop(0).split(',')
	fields[0]=fields[0].replace('# ','')
	proxies = list()
	for line in output:
	  proxies.append(dict(zip(fields,line.split(','))))

    except Exception, e:
      print str(e)
    finally:
      s.close()

except Exception as e:
  print "MIRRORLIST STATE UNKNOWN: " + str(e)
  sys.exit(3)

total=0
downcount=0
downlist=""
for proxy in proxies:
 if proxy['svname'] == "FRONTEND" or proxy['svname'] == "BACKEND":
   continue
 if proxy['pxname'] == "mirror-lists":
   total+=1
   if proxy['status'] == "DOWN":
     downlist+=proxy["svname"]+" "
     downcount+=1

unavailability = 100 * float(downcount) / float(total)

if unavailability == 0:
  print "MIRRORLIST STATE OK: " + downlist
  sys.exit(0)

if unavailability < 50:
  print "MIRRORLIST STATE WARN: " + downlist
  sys.exit(1)

if unavailability >= 50:
  print "MIRRORLIST STATE CRIT: " + downlist
  sys.exit(2)

print "MIRRORLIST STATE UNKNOWN: " + downlist
sys.exit(3)
