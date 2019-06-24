#!/bin/bash
TYPE=$1
NAME=$2
STATE=$3

#
# We are becoming master node
#
if [ $STATE == "MASTER" ]; then
	systemctl stop kojira
	rm -f /etc/cron.d/koji-directory-cleanup
	rm -f /etc/cron.d/koji-gc
	rm -f /etc/cron.d/koji-prune-signed-copies
	logger "just became keepalived master"

fi
#
# We are becoming the backup node
#
if [ $STATE == "BACKUP" ]; then
	systemctl start kojira
        cp -a /usr/local/etc/koji-directory-cleanup /etc/cron.d/koji-directory-cleanup
        cp -a /usr/local/etc/koji-gc /etc/cron.d/koji-gc
        cp -a /usr/local/etc/koji-prune-signed-copies /etc/cron.d/koji-prune-signed-copies
	logger "just became keepalived backup"
fi
#
# something horrible has gone wrong
#
if [ $STATE == "FAULT" ]; then
	logger "just had a keepalived fault"
fi
