#!/bin/bash

TMPFILE=`mktemp` || exit 1

echo "This is a list of packages in the various infrastructure koji tags" >> $TMPFILE
echo "Please check and make sure there are not any that can be removed/dropped" >> $TMPFILE

for TAG in `koji list-tags | grep infra$`; do
  
  echo -e "\n\t\t\t${TAG}\n" >> $TMPFILE
  koji list-pkgs --tag=${TAG} --noinherit >> $TMPFILE

done

mail -s "Weekly Koji Infra Tag Report" infrastructure@lists.fedoraproject.org < $TMPFILE 

rm -f  $TMPFILE
