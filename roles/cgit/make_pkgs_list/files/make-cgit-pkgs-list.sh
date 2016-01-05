#!/bin/sh

#
# This simple script lists out the current pkgs git repos to a file. 
# This speeds up cgit as it doesn't have to recurse into all dirs 
# Looking for git repos. 
#
newfile=`mktemp`
target=/srv/git/repositories

for d in `ls $target`; do
  if [ ! -L $target/$d ] && [ -d $target/$d ]; then
    for f in `ls $target/$d/`; do
     echo "$d/$f" >> $newfile;
    done;
  fi;
done;

mv -Z $newfile /srv/git/pkgs-git-repos-list
chown apache:apache /srv/git/pkgs-git-repos-list
chmod 644 /srv/git/pkgs-git-repos-list
