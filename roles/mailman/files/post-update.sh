#!/bin/bash

CONFFILE=/etc/mailman-migration.conf

set -e 

export PATH=$PATH:$(dirname $(realpath $0)) # make yamlget available

BASEDIR=`yamlget basedir $CONFFILE`
CONFDIR=`yamlget confdir $CONFFILE`
INDEXDIR=$BASEDIR/fulltext_index

django-admin collectstatic --clear --noinput --verbosity 0 --pythonpath $CONFDIR --settings settings
django-admin compress --pythonpath $CONFDIR --settings settings
django-admin syncdb --pythonpath $CONFDIR --settings settings_admin --noinput --migrate
django-admin loaddata /etc/postorius/sites/default/initial-user.json --pythonpath $CONFDIR --settings settings_admin
mkdir -p $INDEXDIR
chown apache:apache -R $INDEXDIR

# Give database rights to the non-admin user
sleep $[ ( $RANDOM % 10 )  + 1 ]s # avoid simultaneous lockups on parallel servers. Yes, this is dirty.
$BASEDIR/bin/pg-give-rights.py > /dev/null

# SELinux contexts
restorecon -r "$BASEDIR"

# Run unit tests
django-admin test --pythonpath $CONFDIR --settings settings_test hyperkitty

# Reload Apache to flush the python cache
systemctl reload httpd

# Clean the cache
systemctl restart memcached
