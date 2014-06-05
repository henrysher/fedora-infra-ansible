#!/bin/bash

##
## This script is used to sync data from main download servers to
## secondary server at ibiblio.
##

RSYNC='/usr/bin/rsync'
RS_OPT="-avSHP  --numeric-ids"
RS_DEADLY="--delete --delete-excluded --delete-delay --delay-updates"
ALT_EXCLUDES="--exclude stage/deltaisos/archive --exclude stage/20-Alpha* --exclude stage/20-Beta*"
EPL_EXCLUDES=""
FED_EXCLUDES=""

SERVER=dl.fedoraproject.org

# http://dl.fedoraproject.org/pub/alt/
${RSYNC} ${RS_OPT} ${RS_DEADLY} ${ALT_EXCLUDES} ${SERVER}::fedora-alt/  /srv/pub/alt/ | tail -n2 | logger -p local0.notice -t rsync_updates_alt
# http://dl.fedoraproject.org/pub/epel/
${RSYNC} ${RS_OPT} ${RS_DEADLY} ${EPL_EXCLUDES} ${SERVER}::fedora-epel/ /srv/pub/epel/ | tail -n2 | logger -p local0.notice -t rsync_updates_epel
# http://dl.fedoraproject.org/pub/fedora/
${RSYNC} ${RS_OPT} ${RS_DEADLY} ${FED_EXCLUDES} ${SERVER}::fedora-enchilada0/ /srv/pub/fedora/ | tail -n2 | logger -p local0.notice -t rsync_updates_fedora

# Let MM know I'm all up to date
#/usr/bin/report_mirror
