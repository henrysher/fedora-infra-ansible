#!/bin/sh
# Puppet notes -- script is file
# mkdir /srv/git_seed
# cron job to invoke file daily
# Need to setup OUTPUT_DIR to be served by apache

# Where the git repos live.  These are bare repos
ORIGIN_DIR=/srv/git/rpms

# Where we'll create the repos to tar up
WORK_DIR=/srv/git_seed
# Subdirectory makes cleanup easier
SEED_DIR=$WORK_DIR/git-checkout

# Where to store the seed tarball for download
OUTPUT_DIR=/srv/cache/lookaside/

# Instead of starting fresh each time, we'll try to use git pull to keep things synced
#rm -rf $WORK_DIR/*
mkdir -p $SEED_DIR

# Give people an indication of when this checkout was last synced
TIMESTAMP=`date --rfc-3339=seconds`
DATE=`date +'%Y%m%d'`
echo "$TIMESTAMP" > $SEED_DIR/TIMESTAMP


for repo in $ORIGIN_DIR/*.git ; do 
  working_tree=$SEED_DIR/$(basename $repo .git)
  if [ -d $working_tree ] ; then
    pushd $working_tree &> /dev/null
    sed -i "s@url = .*@url = $repo@" $working_tree/.git/config 
    git pull --all &> /dev/null
    sed -i "s@url = .*@url = git://pkgs.fedoraproject.org/$(basename $repo .git)@" $working_tree/.git/config 
    popd &>/dev/null
  else
    pushd $SEED_DIR &>/dev/null
    git clone $repo &> /dev/null
    popd &>/dev/null
    sed -i "s@url = .*@url = git://pkgs.fedoraproject.org/$(basename $repo .git)@" $working_tree/.git/config 
    fi
done

tar -cf - -C$WORK_DIR $(basename $SEED_DIR)|xz -2 > $OUTPUT_DIR/.git-seed-$DATE.tar.xz
rm $OUTPUT_DIR/git-seed*tar.xz
mv $OUTPUT_DIR/.git-seed-$DATE.tar.xz $OUTPUT_DIR/git-seed-$DATE.tar.xz
ln -s git-seed-$DATE.tar.xz $OUTPUT_DIR/git-seed-latest.tar.xz
