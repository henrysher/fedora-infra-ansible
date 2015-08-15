#/bin/bash

if [ $# -ne 1 ]; then
        exit 0
fi

NUMBER_OF_CRAWLERS=$1
HOST=`hostname -s`
START_STOP="/usr/local/bin/mm2_get-mirrors-to-crawl"


for i in `seq 1 ${NUMBER_OF_CRAWLERS}`; do
        if [ "${HOST}" == "mm-crawler0${i}" ]; then
		${START_STOP} -f ${i}:${NUMBER_OF_CRAWLERS}
        fi
done
