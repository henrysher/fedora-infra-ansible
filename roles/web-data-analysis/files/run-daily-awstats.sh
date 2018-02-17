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
STORDIR=/mnt/fedora_stats/awstats/storage
OUTDIR=/var/www/html/awstats-reports

TREEDIR=${LOGDIR}/${YEAR}/${MONTH}/${DAY}


AWSTATS=/usr/share/awstats/wwwroot/cgi-bin/awstats.pl
HTMLDOC=/usr/bin/htmldoc

#SITES="apps.fedoraproject.org codecs.fedoraproject.org communityblog.fedoraproject.org docs.fedoraproject.org download.fedoraproject.org fedoramagazine.org fedoraproject.org geoip.fedoraproject.org get.fedoraproject.org getfedora.org labs.fedoraproject.org mirrors.fedoraproject.org spins.fedoraproject.org start.fedoraproject.org"

SITES="admin.fedoraproject.org apps.fedoraproject.org arm.fedoraproject.org ask.fedoraproject.org badges.fedoraproject.org bodhi.fedoraproject.org boot.fedoraproject.org budget.fedoraproject.org bugz.fedoraproject.org cloud.fedoraproject.org codecs.fedoraproject.org communityblog.fedoraproject.org copr.fedoraproject.org darkserver.fedoraproject.org developer.fedoraproject.org developers.fedoraproject.org dl.fedoraproject.org docs.fedoraproject.org docs-old.fedoraproject.org download.fedoraproject.org fas.fedoraproject.org fedora.my fedoracommunity.org fedoramagazine.org fedoraproject.com fedoraproject.org flocktofedora.net flocktofedora.org fonts.fedoraproject.org fpaste.org fudcon.fedoraproject.org geoip.fedoraproject.org get.fedoraproject.org getfedora.org help.fedoraproject.org id.fedoraproject.org it.fedoracommunity.org join.fedoraproject.org k12linux.org kde.fedoraproject.org l10n.fedoraproject.org labs.fedoraproject.org lists.fedorahosted.org lists.fedoraproject.org meetbot-raw.fedoraproject.org meetbot.fedoraproject.org mirrors.fedoraproject.org nightly.fedoraproject.org osbs.fedoraproject.org paste.fedoraproject.org pdc.fedoraproject.org people.fedoraproject.org port389.org qa.fedoraproject.org redirect.fedoraproject.org registry.fedoraproject.org smolts.org spins.fedoraproject.org src.fedoraproject.org start.fedoraproject.org store.fedoraproject.org taskotron.fedoraproject.org translate.fedoraproject.org uk.fedoracommunity.org "

pushd ${CONFDIR}
for SITE in ${SITES}; do
    if [[ -f ${CONFDIR}/${SITE} ]]; then 
	if [[ -d ${STORDIR}/${SITE} ]]; then
	    mkdir -p ${STORDIR}/${SITE}
	fi
	if [[ -d ${OUTDIR}/${YEAR} ]]; then
	    mkdir -p ${OUTDIR}/${YEAR}
	fi
	perl /usr/share/awstats/wwwroot/cgi-bin/awstats.pl -config=${CONFDIR}/${SITE} -update -Logfile=${TREEDIR}/${SITE}-access.log
	perl /mnt/fedora_stats/awstats/conf/awstats_buildstaticpages.pl -awstatsprog=${AWSTATS} -config=${SITE} -month=all -year=${YEAR} -dir=${OUTDIR}/${YEAR} ;
    else
	echo "Site ${SITE} does not have config file"
    fi
done
popd
