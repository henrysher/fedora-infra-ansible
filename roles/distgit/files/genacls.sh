#!/bin/sh

TEMPDIR=`mktemp -d -p /var/tmp genacls.XXXXX`
export GL_RC=/etc/gitolite/gitolite.rc
export GL_BINDIR=/usr/bin

cd $TEMPDIR
# Only replace the acls if genacls completes successfully
if /usr/local/bin/genacls.pkgdb > gitolite.conf ; then
    mv gitolite.conf /etc/gitolite/conf/
    /usr/bin/gl-compile-conf
fi
cd /
rm -rf $TEMPDIR
