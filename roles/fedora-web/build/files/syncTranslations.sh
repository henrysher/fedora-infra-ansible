#!/bin/bash
# this script pull all translations from the zanata Websites project.
# It pulls every resources.

PO_DIR=/var/tmp/po_dir
SITES="alt.fedoraproject.org \
       boot.fedoraproject.org \
       fedoracommunity.org \
       fedorahosted.org \
       fedoraproject.org \
       getfedora.org \
       flocktofedora.org \
       spins.fedoraproject.org \
       labs.fedoraproject.org \
       budget.fedoraproject.org \
       arm.fedoraproject.org \
       start.fedoraproject.org"

# hack for zanata-client, since it currently only is able to find
# config file in ~/.config/zanata.ini and apache's $HOME isn't a good location
export HOME=/var/lib/zanata

[ -d $PO_DIR ] || mkdir $PO_DIR

for site in $SITES
do
  [ -d $PO_DIR/$site ] || mkdir -p $PO_DIR/$site
  cp $HOME/sample.xml $PO_DIR/$site/zanata.xml
  sed -i "s/@VERSION@/$site/" $PO_DIR/$site/zanata.xml
  cd $PO_DIR/$site
  zanata pull
done

