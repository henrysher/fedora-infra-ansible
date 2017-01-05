#!/bin/sh
# Puppet notes -- script is file
# mkdir /srv/git_seed
# cron job to invoke file daily
# Need to setup OUTPUT_DIR to be served by apache

# Where the git repos live.  These are bare repos
ORIGIN_DIR=/srv/git/repositories

# Where we'll create the repos to tar up
WORK_DIR=/srv/git_seed

# Subdirectory makes cleanup easier
SEED_DIR=$WORK_DIR/git-checkout

# subdirectory to collect rpm speciles
SPEC_DIR=$WORK_DIR/rpm-specs

# Where to store the seed tarball for download
OUTPUT_DIR=/srv/cache/lookaside/

# Instead of starting fresh each time, we'll try to use git pull to keep things synced
#rm -rf $WORK_DIR/*
mkdir -p $SEED_DIR
mkdir -p $SPEC_DIR

# Give people an indication of when this checkout was last synced
TIMESTAMP=`date --rfc-3339=seconds`
DATE=`date +'%Y%m%d'`
echo "$TIMESTAMP" > $SEED_DIR/TIMESTAMP


for repo in $ORIGIN_DIR/*.git ; do
  bname=$(basename $repo .git)
  working_tree=$SEED_DIR/$bname
# uncomment to skip processing dead.package repos
#  if [ -e $working_tree/dead.package ]; then
#  continue
#  fi
  if [ -d $working_tree ] ; then
    pushd $working_tree &> /dev/null
    sed -i "s@url = .*@url = $repo@" $working_tree/.git/config
    git pull --all &> /dev/null
    sed -i "s@url = .*@url = git://pkgs.fedoraproject.org/$bname@" $working_tree/.git/config
    popd &>/dev/null
    if [ -e $working_tree/dead.package ]; then
      rm -f $working_tree/$bname.spec
      rm -f $SPEC_DIR/$bname.spec
    elif [ -e $working_tree/$bname.spec ]; then
      cp -p $working_tree/$bname.spec $SPEC_DIR/
    fi
  else
    pushd $SEED_DIR &>/dev/null
    git clone $repo &> /dev/null
    popd &>/dev/null
    sed -i "s@url = .*@url = git://pkgs.fedoraproject.org/$bname@" $working_tree/.git/config
    if [ -e $working_tree/dead.package ]; then
      rm -f $working_tree/$bname.spec
      rm -f $SPEC_DIR/$bname.spec
    elif [ -e $working_tree/$bname.spec ]; then
      cp -p $working_tree/$bname.spec $SPEC_DIR/
    fi
  fi
done

tar -cf - -C$WORK_DIR $(basename $SEED_DIR)|xz -2 > $OUTPUT_DIR/.git-seed-$DATE.tar.xz
tar -cf - -C$WORK_DIR $(basename $SPEC_DIR)|xz -2 > $OUTPUT_DIR/.rpm-specs-$DATE.tar.xz
rm $OUTPUT_DIR/git-seed*tar.xz
rm $OUTPUT_DIR/rpm-specs*tar.xz
mv $OUTPUT_DIR/.git-seed-$DATE.tar.xz $OUTPUT_DIR/git-seed-$DATE.tar.xz
mv $OUTPUT_DIR/.rpm-specs-$DATE.tar.xz $OUTPUT_DIR/rpm-specs-$DATE.tar.xz
ln -s git-seed-$DATE.tar.xz $OUTPUT_DIR/git-seed-latest.tar.xz
ln -s rpm-specs-$DATE.tar.xz $OUTPUT_DIR/rpm-specs-latest.tar.xz

python2 /usr/local/bin/alternative_arch_report.py /srv/git_seed/rpm-specs/ | \
    mail -s "[Report] Packages Restricting Arches" pingou@fedoraproject.org
