#!/bin/bash

HKCONFDIR="/etc/hyperkitty/sites/default"
MMDIR=$1
DOMAIN=$2

if [ -z "$MMDIR" ]; then
    echo  "Usage: $0 <mailman-lib-directory>"
    exit 2
fi

[ -z "$DOMAIN" ] && DOMAIN=lists.fedoraproject.org

existinglists=`mktemp`
trap "rm -f $existinglists" EXIT
sudo -u mailman mailman3 lists -q > $existinglists

for listname in `ls $MMDIR/lists`; do
    listaddr="$listname@$DOMAIN"
    if ! grep -qs $listaddr $existinglists; then
        echo "sudo -u mailman mailman3 create -d $listaddr"
        echo "sudo -u mailman PYTHONPATH=/usr/lib/mailman mailman3 import21 $listaddr $MMDIR/lists/$listname/config.pck"
    fi
    echo "sudo kittystore-import -p $HKCONFDIR -s settings_admin -l $listaddr --continue $MMDIR/archives/private/${listname}.mbox/${listname}.mbox"
done
