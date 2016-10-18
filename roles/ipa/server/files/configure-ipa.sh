#!/bin/bash
ADMIN_PASSWORD="$1"
DM_PASSWORD="$2"

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

# Allow sync user to update passwords
ldapmodify -x -H ldapi://%2fvar%2frun%2fslapd-FEDORAPROJECT-ORG.socket <<EOF
dn: cn=ipa_pwd_extop,cn=plugins,cn=config
changetype: modify
add: passSyncManagersDNs
passSyncManagersDNs: uid=fas_sync,cn=users,cn=accounts,dc=fedoraproject,dc=org
EOF
exit 0
