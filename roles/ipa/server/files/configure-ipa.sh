#!/bin/bash -x
ADMIN_PASSWORD="$1"

function cleanup {
    kdestroy -A
}
trap cleanup EXIT

echo $ADMIN_PASSWORD | kinit admin

# Disallow all users to change their own settings
ipa selfservice-find | grep "Self-service name:" | sed -e "s/  Self-service name: //" | \
while read line
do
    echo "Removing $line"
    ipa selfservice-del "$line"
done

# Disable default permissions so we don't break our privacy policy
ipa permission-mod "System: Read User Addressbook Attributes" --bindtype=permission

# TODO: Add custom permissions to grant specific access to user attributes
