#!/bin/bash

# backup.sh will run FROM backup03 TO the various GNOME boxes on the set. (there's two set
# of machines, one being the ones with a public IP and the others being the IP-less ones that
# will forward their agent through bastion.gnome.org)

export PATH=$PATH:/bin:/usr/bin:/usr/local/bin

MACHINES='signal.gnome.org webapps2.gnome.org clutter.gnome.org blogs.gnome.org chooser.gnome.org git.gnome.org webapps.gnome.org socket.gnome.org bugzilla-web.gnome.org progress.gnome.org clipboard.gnome.org drawable.gnome.org vbox.gnome.org cloud-ssh.gnome.org bastion.gnome.org spinner.gnome.org master.gnome.org combobox.gnome.org restaurant.gnome.org expander.gnome.org'

IPLESS_MACHINES='live.gnome.org extensions.gnome.org view.gnome.org puppet.gnome.org'


BACKUP_DIR='/fedora_backups/gnome/'
LOGS_DIR='/fedora_backups/gnome/logs'
BACKUP_USER='root'

OPTS='-avz -e "ssh -i /usr/local/etc/gnome_backup_id.rsa" --bwlimit=2000'
IPLESS_OPTS='-avz -e "ssh -A -i /usr/local/etc/gnome_backup_id.rsa bastion.gnome.org" --bwlimit=2000'

for MACHINE in "$MACHINES"; do
      rsync $BACKUP_USER@$MACHINE:/etc/rsyncd/backup.exclude $BACKUP_DIR/excludes/$MACHINE.exclude
      cd $BACKUP_DIR/$MACHINE
      rsync $OPTS --exclude-from=$BACKUP_DIR/excludes/$MACHINE.exclude --log-file=$LOGS_DIR/$MACHINE.log $BACKUP_USER@$MACHINE_NAME:/ .
done

for MACHINE in "$IPLESS_MACHINES"; do
      rsync $BACKUP_USER@$MACHINE:/etc/rsyncd/backup.exclude $BACKUP_DIR/excludes/$MACHINE.exclude
      cd $BACKUP_DIR/$MACHINE
      rsync $IPLESS_OPTS --exclude-from=$BACKUP_DIR/excludes/$MACHINE.exclude --log-file=$LOGS_DIR/$MACHINE.log $BACKUP_USER@$MACHINE_NAME:/ .
done

# Dailyreport needs the logs to generate the data we need.
cd $LOGS_DIR && scp -i /fedora_backups/gnome/backup_id.rsa * $BACKUP_USER@combobox.gnome.org:/home/admin/backup-logs
