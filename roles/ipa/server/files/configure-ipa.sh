#!/bin/bash -xe
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

# Create fas_sync user
ipa user-add fas_sync --first=FAS --last=Sync

# Allow sync user to create and edit users
ipa group-add-member admins --users=fas_sync

# Disable password expiration
ipa pwpolicy-mod global_policy --maxlife=0 --minlife=0 --history=0 --minclasses=0 --minlength=0 --maxfail=0
