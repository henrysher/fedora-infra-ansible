#!/bin/bash
# backup and renew letsencrypt certificate. it checks if cert need renewal. if not nginx will not stop

BACKUPDIR=/backups
# create backup
/usr/bin/tar Pczf /$BACKUPDIR/letsencrypt-$(date +%F).tgz /etc/letsencrypt

# check and renew if required. if so do it in standalone mode
/usr/bin/certbot renew -q --pre-hook "/usr/bin/systemctl stop nginx" --post-hook "/usr/bin/systemctl start nginx"

# delete the backup three weeks ago.
rm -f /$BACKUPDIR/letsencrypt-$(date --date="3 weeks ago" +%F).tgz

