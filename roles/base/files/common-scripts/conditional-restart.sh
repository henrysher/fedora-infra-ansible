#!/bin/bash
#
# We use this to try and restart a service. 
# If it's not running, do nothing. 
# If it is running, restart it.
#

SERVICE=$1
/usr/bin/systemctl try-restart $1
