#!/bin/bash

BASELOCATION=/srv/web/meetbot/teams
cd $BASELOCATION
cd ..

for f in `find -type f -mtime -30 | grep -v "fedora-meeting\."`
do
    teamname=$(basename $f | awk -F. '{ print $1 }' )
    mkdir -p $BASELOCATION/$teamname
    ln -f -s $PWD/$f $BASELOCATION/$teamname/
done

