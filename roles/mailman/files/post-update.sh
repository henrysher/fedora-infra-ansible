#!/bin/bash

CONFFILE=/etc/mailman-migration.conf

set -e 

export PATH=$PATH:$(dirname $(realpath $0)) # make yamlget available

BASEDIR=`yamlget basedir $CONFFILE`
CONFDIR=`yamlget confdir $CONFFILE`
INDEXDIR=$BASEDIR/kittystore_search_index

django-admin collectstatic --clear --noinput --pythonpath $CONFDIR --settings settings
django-admin assets build --parse-templates --pythonpath $CONFDIR --settings settings
django-admin syncdb --pythonpath $CONFDIR --settings settings_admin
django-admin migrate hyperkitty --pythonpath $CONFDIR --settings settings_admin
django-admin loaddata /etc/postorius/sites/default/initial-user.json --pythonpath $CONFDIR --settings settings_admin
kittystore-updatedb --pythonpath $CONFDIR --settings settings_admin
chown mailman:mailman -R $INDEXDIR
chmod g+w -R $INDEXDIR

# Give database rights to the non-admin user
$BASEDIR/bin/pg-give-rights.py
