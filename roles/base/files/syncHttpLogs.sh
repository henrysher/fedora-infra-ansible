#!/bin/bash

RSYNC_FLAGS='-az --no-motd'

function syncHttpLogs {

    # in case we missed a run or two.. try to catch up the last 3 days.
    for d in 1 2 3
    do
        HOST=$1
	# some machines store stuff in old format. some new.
        if [ "$2" = "old" ]; then
            YESTERDAY=$(/bin/date -d "-$d days" +%Y-%m-%d)
        else
            YESTERDAY=$(/bin/date -d "-$d days" +%Y%m%d)
        fi
        YEAR=$(/bin/date -d "-$d days" +%Y)
        MONTH=$(/bin/date -d "-$d days" +%m)
        DAY=$(/bin/date -d "-$d days" +%d)
        /bin/mkdir -p /var/log/hosts/$HOST/$YEAR/$MONTH/$DAY/http
        cd /var/log/hosts/$HOST/$YEAR/$MONTH/$DAY/http/

        for f in $(/usr/bin/rsync $RSYNC_FLAGS --list-only $HOST::log/httpd/*$YESTERDAY* | awk '{ print $5 }')
        do
            DEST=$(echo $f | /bin/sed s/-$YESTERDAY//)
            /usr/bin/rsync $RSYNC_FLAGS $HOST::log/httpd/$f ./$DEST
        done
    done
}

syncHttpLogs proxy01.phx2.fedoraproject.org
syncHttpLogs proxy02.vpn.fedoraproject.org
syncHttpLogs proxy03.vpn.fedoraproject.org
syncHttpLogs proxy04.vpn.fedoraproject.org
syncHttpLogs proxy05.vpn.fedoraproject.org
syncHttpLogs proxy06.vpn.fedoraproject.org
syncHttpLogs proxy07.vpn.fedoraproject.org
syncHttpLogs proxy08.vpn.fedoraproject.org
syncHttpLogs proxy09.vpn.fedoraproject.org
syncHttpLogs proxy10.phx2.fedoraproject.org
syncHttpLogs proxy11.vpn.fedoraproject.org
syncHttpLogs proxy12.vpn.fedoraproject.org
syncHttpLogs proxy13.vpn.fedoraproject.org
syncHttpLogs proxy14.vpn.fedoraproject.org
syncHttpLogs proxy01.stg.phx2.fedoraproject.org
syncHttpLogs fas01.phx2.fedoraproject.org
syncHttpLogs fas02.phx2.fedoraproject.org
syncHttpLogs fas03.phx2.fedoraproject.org
syncHttpLogs fas01.stg.phx2.fedoraproject.org
syncHttpLogs fedocal01.phx2.fedoraproject.org
syncHttpLogs fedocal02.phx2.fedoraproject.org
syncHttpLogs fedocal01.stg.phx2.fedoraproject.org
syncHttpLogs paste01.phx2.fedoraproject.org
syncHttpLogs paste02.phx2.fedoraproject.org
syncHttpLogs paste01.stg.phx2.fedoraproject.org
syncHttpLogs datagrepper01.phx2.fedoraproject.org
syncHttpLogs datagrepper02.phx2.fedoraproject.org
syncHttpLogs datagrepper01.stg.phx2.fedoraproject.org
syncHttpLogs ipsilon01.phx2.fedoraproject.org
syncHttpLogs ipsilon02.phx2.fedoraproject.org
syncHttpLogs ask01.phx2.fedoraproject.org
syncHttpLogs ask02.phx2.fedoraproject.org
syncHttpLogs ask01.stg.phx2.fedoraproject.org
syncHttpLogs badges-web01.phx2.fedoraproject.org
syncHttpLogs badges-web02.phx2.fedoraproject.org
syncHttpLogs badges-web01.stg.phx2.fedoraproject.org
syncHttpLogs elections01.phx2.fedoraproject.org
syncHttpLogs elections02.phx2.fedoraproject.org
syncHttpLogs elections01.stg.phx2.fedoraproject.org
syncHttpLogs tagger01.phx2.fedoraproject.org
syncHttpLogs tagger02.phx2.fedoraproject.org
syncHttpLogs tagger01.stg.phx2.fedoraproject.org
syncHttpLogs bodhi03.phx2.fedoraproject.org
syncHttpLogs bodhi04.phx2.fedoraproject.org
syncHttpLogs bodhi01.stg.phx2.fedoraproject.org
syncHttpLogs packages03.phx2.fedoraproject.org
syncHttpLogs packages04.phx2.fedoraproject.org
syncHttpLogs packages03.stg.phx2.fedoraproject.org
syncHttpLogs blockerbugs01.phx2.fedoraproject.org
syncHttpLogs blockerbugs02.phx2.fedoraproject.org
syncHttpLogs blockerbugs01.stg.phx2.fedoraproject.org
syncHttpLogs value01.phx2.fedoraproject.org
syncHttpLogs secondary01
syncHttpLogs hosted03.vpn.fedoraproject.org old
syncHttpLogs people02.vpn.fedoraproject.org old
syncHttpLogs noc01.phx2.fedoraproject.org
syncHttpLogs download01.phx2.fedoraproject.org
syncHttpLogs download02.phx2.fedoraproject.org
syncHttpLogs download03.phx2.fedoraproject.org
syncHttpLogs download04.phx2.fedoraproject.org
syncHttpLogs download05.phx2.fedoraproject.org
syncHttpLogs download-rdu01.vpn.fedoraproject.org
syncHttpLogs sundries01.phx2.fedoraproject.org
syncHttpLogs sundries02.phx2.fedoraproject.org
syncHttpLogs sundries01.stg.phx2.fedoraproject.org
## eof
