#!/bin/bash

output=`mktemp`
moutput=`mktemp`
dest=/etc/postfix/package-owner
mdest=/etc/postfix/package-maintainers
/usr/local/bin/owner-email.py >> $output
if [ $? != 0 ]; then
   echo "error creating owner-alias file" >&2
   exit 1
fi

sed -e 's/-owner: /-maintainers: /' $output > $moutput

cp $output $dest
chmod +r $output
mv $output $dest
/usr/sbin/restorecon /etc/postfix/package-owner
/usr/sbin/postalias /etc/postfix/package-owner

cp $moutput $mdest
chmod +r $moutput
mv $moutput $mdest
/usr/sbin/restorecon /etc/postfix/package-maintainers
/usr/sbin/postalias /etc/postfix/package-maintainers
