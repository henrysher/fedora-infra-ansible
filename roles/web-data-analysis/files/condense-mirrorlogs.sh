#!/bin/bash

# This file is part of Fedora Project Infrastructure Ansible
# Repository.
#
# Fedora Project Infrastructure Ansible Repository is free software:
# you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later
# version.
#
# Fedora Project Infrastructure Ansible Repository is distributed in
# the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with Fedora Project Infrastructure Ansible Repository.  If
# not, see <http://www.gnu.org/licenses/>.

# There is a multiday delay involved in processing the logs. It
# may take up to 4 days to get the logs to the main-server. It may
# take a day to combine all the logs onto combined-httpd. So we assume 
# we are 5 days behind.

let NUMDAYS=5
let OLDDAYS=$(( $NUMDAYS+1 ))

PROJECT=mirrors
WEBLOG=${PROJECT}.fedoraproject.org

# This is the year/month/day for a N days ago.
YEAR=$(/bin/date -d "-${NUMDAYS} days" +%Y)
MONTH=$(/bin/date -d "-${NUMDAYS} days" +%m)
DAY=$(/bin/date -d "-${NUMDAYS} days" +%d)

# And we have have to deal with year/month/day boundaries for our later grep.
OLDDATE=$(/bin/date -d "-${OLDDAYS} days" +%Y-%m-%d)
OLDYEAR=$(/bin/date -d "-${OLDDAYS} days" +%Y)

NFSDIR=/mnt/fedora_stats/combined-http
TARGET=${NFSDIR}/${YEAR}/${MONTH}/${DAY}

LOGFILE=${TARGET}/${WEBLOG}-access.log

WORKDIR=/mnt/fedora_stats/data/${PROJECT}
WORKFILE=${WORKDIR}/${YEAR}/${MONTH}/worked-${DAY}

WEBDIR=/var/www/html/csv-reports/${PROJECT}

TEMPDIR=$( mktemp -d /tmp/web-data-analysis.XXXXXXXXX )

LBIN=/usr/local/bin/
LSHARE=/usr/local/share/web-data-analysis

mkdir -p ${WORKDIR}/${YEAR}/${MONTH}
if [[ ! -f ${WORKDIR}/${YEAR}/out-${YEAR}-${MONTH} ]]; then
    touch ${WORKDIR}/${YEAR}/out-${YEAR}-${MONTH}
fi

if [[ ! -f ${WORKDIR}/out-${YEAR} ]]; then
    touch ${WORKDIR}/out-${YEAR}
fi


if [[ ! -f ${LOGFILE} ]]; then
    echo "No logfile found for ${YEAR}/${MONTH}/${DAY}. Please fix."
elif [[ -f ${WORKFILE} ]]; then 
    echo "The workfile for ${YEAR}/${MONTH}/${DAY} already existed."
else
    ${LBIN}/mirrorlist.py -o ${WORKFILE} ${LOGFILE}; 
fi

# So the data isn't strictly across month boundries due to the end of
# the logfiles being at 04:00 versus 23:59. Also log files might get
# stuck and you end up with days or weeks of data in a single
# file. Doing a continual sort clears up that.

sort -o ${WORKFILE} -u ${WORKFILE}
sort -o ${WORKDIR}/${YEAR}/out-${YEAR}-${MONTH} -S 8G -T /srv/tmp -u ${WORKDIR}/${YEAR}/out-${YEAR}-${MONTH} ${WORKFILE}
sort -o ${WORKDIR}/out-${YEAR} -S 8G -T /srv/tmp -u ${WORKDIR}/out-${YEAR} ${WORKFILE}

# Because the logs stop at 04:00 we can only get 24 hours from 6 days before. 
###
### FIXME: This breaks around the new year.
egrep "${OLDDATE}" ${WORKDIR}/out-${OLDYEAR} > ${TEMPDIR}/watched-day

# Grab the data and put it in the two files. This makes it a lot
# faster to process as a whole year may take an hour to go through.

for i in ${OLDYEAR} all; do
    awk -f ${LSHARE}/${PROJECT}-data.awk ${TEMPDIR}/watched-day >> ${WEBDIR}/${PROJECT}data-${i}.csv
    sort -o ${WEBDIR}/${PROJECT}data-${i}.csv -u ${WEBDIR}/${PROJECT}data-${i}.csv
done

gnuplot ${LSHARE}/${PROJECT}-data.gp

# Make the seven day moving average file
/usr/local/bin/mirrors-moving_avg.py > ${WEBDIR}/${PROJECT}data-all-7day-ma.csv

gnuplot  ${LSHARE}/${PROJECT}-moving.gp

# cleanup the temp data
rm -rf ${TEMPDIR}
