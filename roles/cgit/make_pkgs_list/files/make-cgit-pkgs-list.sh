#!/bin/sh

#
# This simple script lists out the current pkgs git repos to a file. 
# This speeds up cgit as it doesn't have to recurse into all dirs 
# Looking for git repos. 
#
newfile=`mktemp`
target=/srv/git/repositories

# These are the pagure folders that we don't want to bother showing in cgit (it
# makes things too slow...)
blacklist='forks tickets docs requests'

for d in `ls $target`; do
  # If it's not a link, it is a directory, and it's not in the blacklist..
  if [ ! -L $target/$d ] && [ -d $target/$d ] && [[ ! $blacklist == *"$d"* ]]; then
    # Then take every file inside and stuff it into our tmpfile.
    for f in `ls $target/$d/`; do
     echo "$d/$f" >> $newfile;
    done;
  fi;
done;

# When we're done with everything in $target, make that avail to cgit.
mv -Z $newfile /srv/git/pkgs-git-repos-list
chown apache:apache /srv/git/pkgs-git-repos-list
chmod 644 /srv/git/pkgs-git-repos-list
