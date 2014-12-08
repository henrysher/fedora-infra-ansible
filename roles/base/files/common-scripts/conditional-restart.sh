#!/bin/bash
# Restart SERVICE only if PACKAGE is installed.
# We use this throughout handlers/restart_services.yml

SERVICE=$1
PACKAGE=$2

rpm -q $PACKAGE

INSTALLED=$?

if [ $INSTALLED -eq 0 ]; then
    echo "Package $PACKAGE installed.  Attempting restart of $SERVICE."
    /sbin/service $SERVICE restart
    exit $?  # Exit with the /sbin/service status code
fi

# If the package wasn't installed, then pretend everything is fine.
echo "Package $PACKAGE not installed.  Skipping restart of $SERVICE."
exit 0
