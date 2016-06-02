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
# we are 6 days behind.

let NUMDAYS=6

# This is the year/month/day for a N days ago.
YEAR=$(/bin/date -d "-${NUMDAYS} days" +%Y)
MONTH=$(/bin/date -d "-${NUMDAYS} days" +%m)
DAY=$(/bin/date -d "-${NUMDAYS} days" +%d)

LOGDIR=/mnt/fedora_stats/combined-http/
CONFDIR=/mnt/fedora_stats/awstats/conf
OUTDIR=/var/www/html/awstats-reports

TREEDIR=${LOGDIR}/${YEAR}/${MONTH}/${DAY}


AWSTATS=/usr/share/awstats/wwwroot/cgi-bin/awstats.pl
HTMLDOC=/usr/bin/htmldoc

SITES="apps.fedoraproject.org codecs.fedoraproject.org communityblog.fedoraproject.org docs.fedoraproject.org download.fedoraproject.org fedoramagazine.org fedoraproject.org geoip.fedoraproject.org get.fedoraproject.org getfedora.org labs.fedoraproject.org mirrors.fedoraproject.org spins.fedoraproject.org start.fedoraproject.org"


for SITE in ${SITES}; do
    perl /usr/share/awstats/wwwroot/cgi-bin/awstats.pl -config=${CONFDIR}/${SITE} -update -Logfile=${TREEDIR}/${SITE}-access.log
done

