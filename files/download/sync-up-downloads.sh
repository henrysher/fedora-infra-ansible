#!/bin/bash

##
## This script is used to sync data from main download servers to
## secondary server at ibiblio.
##

RSYNC='/usr/bin/rsync'
RS_OPT="-avSHP  --numeric-ids"
RS_DEADLY="--delete --delete-excluded --delete-delay --delay-updates"
ALT_EXCLUDES="--exclude deltaisos/archive --exclude 22_Alpha* --exclude 22_Beta*"
EPL_EXCLUDES=""
FED_EXCLUDES=""

SERVER=dl.fedoraproject.org

# http://dl.fedoraproject.org/pub/alt/stage/
${RSYNC} ${RS_OPT} ${RS_DEADLY} ${ALT_EXCLUDES} ${SERVER}::fedora-alt/stage/  /srv/pub/alt/stage/ | tail -n2 | logger -p local0.notice -t rsync_updates_alt_stg
# http://dl.fedoraproject.org/pub/alt/bfo/
${RSYNC} ${RS_OPT} ${RS_DEADLY} ${ALT_EXCLUDES} ${SERVER}::fedora-alt/bfo/  /srv/pub/alt/bfo/ | tail -n2 | logger -p local0.notice -t rsync_updates_alt_bfo
# http://dl.fedoraproject.org/pub/epel/
${RSYNC} ${RS_OPT} ${RS_DEADLY} ${EPL_EXCLUDES} ${SERVER}::fedora-epel/ /srv/pub/epel/ | tail -n2 | logger -p local0.notice -t rsync_updates_epel
# http://dl.fedoraproject.org/pub/fedora/
${RSYNC} ${RS_OPT} ${RS_DEADLY} ${FED_EXCLUDES} ${SERVER}::fedora-enchilada0/ /srv/pub/fedora/ | tail -n2 | logger -p local0.notice -t rsync_updates_fedora

# Let MM know I'm all up to date
#/usr/bin/report_mirror
