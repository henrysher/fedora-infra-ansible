#!/bin/bash
# backup letsencrypt certificate

BACKUPDIR=/backups
# create backup
/usr/bin/tar Pczf /$BACKUPDIR/letsencrypt-$(date +%F).tgz /etc/letsencrypt

# delete the backup three weeks ago.
rm -f /$BACKUPDIR/letsencrypt-$(date --date="3 weeks ago" +%F).tgz

