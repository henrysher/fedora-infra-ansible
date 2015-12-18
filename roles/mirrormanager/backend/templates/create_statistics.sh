#!/bin/sh

MIRRORLIST_SERVERS="{% for host in groups['mirrorlist2'] %} {{ host }} {% endfor %}"
FRONTENDS="{% for host in groups['mm-frontend'] %} {{ host }} {% endfor %}"

INPUT="/var/log/mirrormanager/mirrorlist.log"

if [ "$1" == "yesterday" ]; then
	DATE=`date +%Y-%m-%d --date='yesterday'`
	STATISTICS="/usr/bin/mirrorlist_statistics -o 1"
	DEST="/var/www/mirrormanager-statistics/data/`date +%Y/%m --date='yesterday'`"
else
	DATE=`date +%Y-%m-%d`
	STATISTICS="/usr/bin/mirrorlist_statistics"
	DEST="/var/www/mirrormanager-statistics/data/`date +%Y/%m`"
fi

INFILE=${INPUT}.${DATE}

OUTPUT=`mktemp -d`

#trap "rm -f ${OUTPUT}/*; rmdir ${OUTPUT}" QUIT TERM INT HUP EXIT

# Fetch compressed log files
for s in ${MIRRORLIST_SERVERS}; do
	ssh $s "( cat $INFILE | gzip -4 )" >> ${OUTPUT}/mirrorlist.log.gz
done

${STATISTICS} -l ${OUTPUT}/mirrorlist.log.gz -d ${OUTPUT}/

for f in ${FRONTENDS}; do
	ssh ${f} mkdir -p ${DEST}
	rsync -aq ${OUTPUT}/{*.png,*.txt} ${f}:${DEST}
done
