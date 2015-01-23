#!/bin/bash

URL=https://admin.fedoraproject.org/ca/crl.pem
OLD=/etc/pki/tls/crl.pem
NEW=/var/tmp/crl.pem

wget $URL -O $NEW
OLDUPDATE=`openssl crl -in $OLD -noout -lastupdate`
NEWUPDATE=`openssl crl -in $NEW -noout -lastupdate`

if [ "$OLDUPDATE" != "$NEWUPDATE" ]; then
    cp -f $NEW $OLD
    /sbin/restorecon $OLD
    /etc/init.d/httpd graceful
    echo "updated to $NEWUPDATE"
fi

