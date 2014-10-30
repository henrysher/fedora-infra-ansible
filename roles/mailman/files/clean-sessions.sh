#!/bin/bash

CONFFILE=/etc/mailman-migration.conf

set -e 
export PATH=$PATH:$(dirname $(realpath $0)) # make yamlget available

CONFDIR=`yamlget confdir $CONFFILE`
django-admin clearsessions --pythonpath $CONFDIR --settings settings
