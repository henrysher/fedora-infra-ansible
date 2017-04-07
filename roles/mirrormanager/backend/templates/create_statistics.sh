#!/bin/sh

MIRRORLIST_SERVERS="{% for host in groups['mirrorlist2'] %} {{ host }} {% endfor %}"
MIRRORLIST_PROXIES="{% for host in groups['mirrorlist-proxies'] %} {{ host }} {% endfor %}"
FRONTENDS="{% for host in groups['mm-frontend'] %} {{ host }} {% endfor %}"

INPUT="/var/log/mirrormanager/mirrorlist.log"
CONTAINER1="/var/log/mirrormanager/mirrorlist1.service.log"
CONTAINER2="/var/log/mirrormanager/mirrorlist2.service.log"

if [ "$1" == "yesterday" ]; then
	DATE=`date +%Y%m%d --date='yesterday'`
	STATISTICS="/usr/bin/mirrorlist_statistics -o 1"
	DEST="/var/www/mirrormanager-statistics/data/`date +%Y/%m --date='yesterday'`"
else
	DATE=`date +%Y%m%d`
	STATISTICS="/usr/bin/mirrorlist_statistics"
	DEST="/var/www/mirrormanager-statistics/data/`date +%Y/%m`"
fi

INFILE=${INPUT}-${DATE}.xz

OUTPUT=`mktemp -d`

trap "rm -f ${OUTPUT}/*; rmdir ${OUTPUT}" QUIT TERM INT HUP EXIT

# Fetch compressed log files
for s in ${MIRRORLIST_SERVERS}; do
	ssh $s "( xzcat $INFILE | gzip -4 )" >> ${OUTPUT}/mirrorlist.log.gz
done
for s in ${MIRRORLIST_PROXIES}; do
	ssh $s "( cat $CONTAINER1 | gzip -4 )" >> ${OUTPUT}/mirrorlist.log.gz
	ssh $s "( cat $CONTAINER2 | gzip -4 )" >> ${OUTPUT}/mirrorlist.log.gz
	if [ "$1" == "yesterday" ]; then
		ssh $s "( xzcat $CONTAINER1-${DATE}.xz | gzip -4 )" >> ${OUTPUT}/mirrorlist.log.gz
		ssh $s "( xzcat $CONTAINER2-${DATE}.xz | gzip -4 )" >> ${OUTPUT}/mirrorlist.log.gz
	fi
done

${STATISTICS} -l ${OUTPUT}/mirrorlist.log.gz -d ${OUTPUT}/

for f in ${FRONTENDS}; do
	ssh ${f} mkdir -p ${DEST}
	rsync -aq ${OUTPUT}/{*.png,*.txt} ${f}:${DEST}
done
