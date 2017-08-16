#!/bin/bash
# reload SERVICE only if PACKAGE is installed.
# We use this throughout handlers/restart_services.yml

SERVICE=$1
PACKAGE=$2

rpm -q $PACKAGE

INSTALLED=$?

if [ $INSTALLED -eq 0 ]; then
    echo "Checking if $SERVICE is running"
    /sbin/service $SERVICE status >& /dev/null
    if [ $? == 0 ]; then
      echo "Package $PACKAGE installed and running.  Attempting reload of $SERVICE."
      /sbin/service $SERVICE reload
      exit $?  # Exit with the /sbin/service status code
    fi
    echo "Package $PACKAGE is install, but $SERVICE is not running, skipping..."
    exit 0
fi

# If the package wasn't installed, then pretend everything is fine.
echo "Package $PACKAGE not installed.  Skipping reload of $SERVICE."
exit 0
