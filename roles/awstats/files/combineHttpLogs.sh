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

# Because sync-http may not get all logs for 3 days, we only merge
# things after 4 days. 

NUMDAYS=4
YEAR=$(/bin/date -d "-${NUMDAYS} days" +%Y)
MONTH=$(/bin/date -d "-${NUMDAYS} days" +%m)
DAY=$(/bin/date -d "-${NUMDAYS} days" +%d)

LOGDIR=/var/log/hosts
NFSDIR=/mnt/fedora_stats/combined-http
PROXYLOG=${LOGDIR}/proxy*/${YEAR}/${MONTH}/${DAY}/http/
DL_LOG=${LOGDIR}/download*/${YEAR}/${MONTH}/${DAY}/http/
PEOPLE=${LOGDIR}/people*/${YEAR}/${MONTH}/${DAY}/http/

TARGET=${NFSDIR}/${YEAR}/${MONTH}/${DAY}

LOGMERGE=/usr/share/awstats/tools/logresolvemerge.pl

mkdir -p ${TARGET}

##
## Merge the Proxies
FILES=$( ls -1 ${PROXYLOG}/*access.log.xz | awk '{x=split($0,a,"/"); print a[x]}' | sort -u )

for FILE in ${FILES}; do
    TEMP=$(echo ${FILE} | sed 's/\.xz$//')
    perl ${LOGMERGE} ${PROXYLOG}/${FILE} > ${TARGET}/${TEMP}
done

##
## Merge the Downloads
FILES=$( ls -1 ${DL_LOG}/dl*access.log.xz | awk '{x=split($0,a,"/"); print a[x]}' | sort -u )

for FILE in ${FILES}; do
    TEMP=$(echo ${FILE} | sed 's/\.xz$//')
    perl ${LOGMERGE} ${DL_LOG}/${FILE} > ${TARGET}/${TEMP}
done

##
## Merge the People
##
## Merge the Downloads
FILES=$( ls -1 ${PEOPLE}/fedora*access.log.xz | awk '{x=split($0,a,"/"); print a[x]}' | sort -u )

for FILE in ${FILES}; do
    TEMP=$(echo ${FILE} | sed 's/\.xz$//')
    perl ${LOGMERGE} ${PEOPLE}/${FILE} > ${TARGET}/${TEMP}
done

# Now we link up the files into latest directory
# 1. make sure the latest directory exists
# 2. go into it.
# 3. remove the old links
# 4. link up all the files we merged over

if [[ -d ${NFSDIR}/latest ]]; then
    pushd ${NFSDIR}/latest &> /dev/null
    /bin/rm -f *
    for file in ../${YEAR}/${MONTH}/${DAY}/*; do
	ln -s ${file} .
    done
    popd &> /dev/null
fi
