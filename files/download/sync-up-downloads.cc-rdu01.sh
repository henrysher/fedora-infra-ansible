#!/bin/bash

##
## This script is used to sync data from main download servers to
## secondary server at RDU community cage.
##

RSYNC='/usr/bin/rsync'
RS_OPT="-avSHP  --numeric-ids"
RS_DEADLY="--delete --delete-excluded --delete-delay --delay-updates"
EPL_EXCLUDES=""
FED_EXCLUDES=""

SERVER=dl.fedoraproject.org

# http://dl.fedoraproject.org/pub/epel/
${RSYNC} ${RS_OPT} ${RS_DEADLY} ${EPL_EXCLUDES} ${SERVER}::fedora-epel/ /srv/pub/epel/ | tail -n2 | logger -p local0.notice -t rsync_updates_epel
# http://dl.fedoraproject.org/pub/fedora/
${RSYNC} ${RS_OPT} ${RS_DEADLY} ${FED_EXCLUDES} ${SERVER}::fedora-enchilada0/ /srv/pub/fedora/ | tail -n2 | logger -p local0.notice -t rsync_updates_fedora
# http://dl.fedoraproject.org/pub/fedora-secondary/
${RSYNC} ${RS_OPT} ${RS_DEADLY} ${FED_EXCLUDES} ${SERVER}::fedora-secondary0/ /srv/pub/fedora-secondary/ | tail -n2 | logger -p local0.notice -t rsync_updates_fedora_2nd

# Let MM know I'm all up to date
#/usr/bin/report_mirror
