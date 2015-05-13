#/bin/bash

if [ $# -ne 1 ]; then
        exit 0
fi

NUMBER_OF_CRAWLERS=$1
HOST=`hostname -s`
MAX_HOST=`/usr/local/bin/mm2_get-highest-active-host-id`

# make MAX_HOST a multiple of NUMBER_OF_CRAWLERS
let FIX=${MAX_HOST}%${NUMBER_OF_CRAWLERS}

if [ "${FIX}" -ne "0" ]; then
        let MAX_HOST=${MAX_HOST}+${NUMBER_OF_CRAWLERS}-${FIX}
fi

let PART=${MAX_HOST}/${NUMBER_OF_CRAWLERS}

STARTID=0
STOPID=${PART}

for i in `seq 1 ${NUMBER_OF_CRAWLERS}`; do
        if [ "${HOST}" == "mm-crawler0${i}" ]; then
                echo "--startid=${STARTID} --stopid=${STOPID}"
        fi
        let STARTID=${STARTID}+${PART}
        let STOPID=${STOPID}+${PART}
	if [ "${STOPID}" -eq "${MAX_HOST}" ]; then
		let STOPID=${STOPID}+1
	fi
done
