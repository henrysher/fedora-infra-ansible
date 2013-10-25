#!/bin/bash

CONFFILE=/etc/mailman-migration.conf
BASEDIR=`yamlget basedir $CONFFILE`
CONFDIR=`yamlget confdir $CONFFILE`

set -e 

django-admin collectstatic --clear --noinput --pythonpath $CONFDIR --settings settings
django-admin assets build --parse-templates --pythonpath $CONFDIR --settings settings
django-admin syncdb --pythonpath $CONFDIR --settings settings_admin
django-admin migrate hyperkitty --pythonpath $CONFDIR --settings settings_admin
django-admin loaddata /etc/postorius/sites/default/initial-user.json --pythonpath $CONFDIR --settings settings_admin
kittystore-updatedb --pythonpath $CONFDIR --settings settings_admin

# Give database rights to the non-admin user
$BASEDIR/bin/pg-give-rights.py
