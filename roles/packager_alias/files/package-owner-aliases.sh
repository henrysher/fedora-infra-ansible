#!/bin/bash

output=`mktemp`
dest=/etc/postfix/package-owner
/usr/local/bin/owner-email.py >> $output
if [ $? != 0 ]; then
   echo "error creating owner-alias file" >&2
   exit 1
fi

cp $output $dest
chmod +r $output
mv $output $dest
restorecon /etc/postfix/package-owner
postalias /etc/postfix/package-owner
