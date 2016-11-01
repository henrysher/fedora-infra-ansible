#!/bin/bash

if [[ $UID != 0 ]]
then
    echo "$0 must be run as root (sudo)"
    exit 1
fi

echo
echo "Updating $1 into $2 for production"
echo

src="$1"
dest="$2"
if [ -d $dest/.git ]; then
   cd $dest
   unset GIT_DIR
   /usr/bin/git pull 2>&1
else
    /usr/bin/git clone $src $dest 2>&1 | sed 's/^/    /'
fi

echo

