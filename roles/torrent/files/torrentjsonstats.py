#!/usr/bin/python -tt

import sys
import simplejson


whitelist='/srv/torrent/btholding/whitelist'


if len(sys.argv) < 2:
    print "Usage: torrentstats.py /path/to/torrent/stats/file"
    sys.exit(1)
    
torrents = {}
for line in open(whitelist,'r').readlines():
    line = line.strip()
    csum, torrent = line.split('-', 1)
    torrents[csum.strip()] = torrent.replace('.torrent','')


tlist = []
for line in open(sys.argv[1],'r').readlines():
    line = line.strip()
    if not line:
        continue
    tdict = {}
    csum,total,active = line.split(':')
    if csum not in torrents:
        continue
    tdict['name'] = torrents[csum].strip()
    tdict['completed'] = int(total)
    tdict['downloaders'] = int(active)
    tdict['size'] = 0
    tdict['seeds'] = 1
    tlist.append(tdict)

print simplejson.dumps(tlist)
