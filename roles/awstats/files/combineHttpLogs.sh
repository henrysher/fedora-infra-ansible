#!/bin/bash

#
# The object of this script is to combine multiple http logs from the
# proxy servers and put them into an NFS directory where they can be
# analyzed by other software on other systems.
#

# Because sync-http may not get all logs for 3 days, we only merge
# things after 4 days. 
NUMDAYS=4
YEAR=$(/bin/date -d "-${NUMDAYS} days" +%Y)
MONTH=$(/bin/date -d "-${NUMDAYS} days" +%m)
DAY=$(/bin/date -d "-${NUMDAYS} days" +%d)

LOGDIR=/var/log/hosts
HTTPLOG=${LOGDIR}/proxy*/${YEAR}/${MONTH}/${DAY}/http/

TARGET=/mnt/fedora_stats/combined-http/${YEAR}/${MONTH}/${DAY}

AWSTATS=/usr/share/awstats/tools/logresolvemerge.pl

FILES=$( ls -1 ${HTTPLOG}/*access.log.xz | awk '{x=split($0,a,"/"); print a[x]}' | sort -u )

for FILE in ${FILES}; do
    TEMP=$(echo ${FILE} | sed 's/\.xz$//')
    perl ${AWSTATS} ${HTTPLOG}/${FILE} > ${TARGET}/${TEMP}
done
