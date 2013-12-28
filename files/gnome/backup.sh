#!/bin/bash
# backup.sh will run FROM backup03 TO the various GNOME boxes on the set. (there's two set
# of machines, one being the ones with a public IP and the others being the IP-less ones that
# will forward their agent through bastion.gnome.org)

export PATH=$PATH:/bin:/usr/bin:/usr/local/bin

MACHINES='signal.gnome.org
          webapps2.gnome.org
          clutter.gnome.org
          blogs.gnome.org
          chooser.gnome.org
          git.gnome.org
          webapps.gnome.org
          socket.gnome.org
          bugzilla-web.gnome.org
          progress.gnome.org
          clipboard.gnome.org
          drawable.gnome.org
          vbox.gnome.org
          cloud-ssh.gnome.org
          bastion.gnome.org
          spinner.gnome.org
          master.gnome.org
          combobox.gnome.org
          restaurant.gnome.org
          expander.gnome.org
          live.gnome.org
          extensions.gnome.org
          view.gnome.org
          puppet.gnome.org'

BACKUP_DIR='/fedora_backups/gnome/'
LOGS_DIR='/fedora_backups/gnome/logs'

for MACHINE in $MACHINES; do
      rsync -avz -e 'ssh -F /usr/local/etc/gnome_ssh_config' --bwlimit=2000 $MACHINE:/etc/rsyncd/backup.exclude $BACKUP_DIR/excludes/$MACHINE.exclude
      rdiff-backup --force --remote-schema 'ssh -F /usr/local/etc/gnome_ssh_config %s rdiff-backup --server' --print-statistics --exclude-device-files --exclude-filelist $BACKUP_DIR/excludes/$MACHINE.exclude $MACHINE::/ $BACKUP_DIR/$MACHINE/ | mail -s 'Daily backup: $MACHINE' backups@gnome.org
done
