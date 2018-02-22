#!/bin/bash
#
# We use this to try and restart a service. 
# If it's not running, do nothing. 
# If it is running, restart it.
#

SERVICE=$1
# Check if service unit is present before trying to restart it
/usr/bin/systemctl cat $1.service &>/dev/null && /usr/bin/systemctl try-restart $1
