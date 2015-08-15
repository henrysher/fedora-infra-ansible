#!/bin/bash
outfile=`mktemp`

finalfile=/var/www/cgit.repos
for homedir in /home/fedora/* ; do
  if [ ! -d $homedir/public_git ]; then
    continue
  fi
  for gitdir in $homedir/public_git/* ; do
    if [ ! -f $gitdir/git-daemon-export-ok ]; then
      continue
    fi
    echo $gitdir | sed -e 's;^/home/fedora/;;' >> $outfile
  done
done

cp -f $outfile  $finalfile
chmod 644 $finalfile
