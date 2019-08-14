#! /bin/bash

. /home/copr/cloud/keystonerc_proper_tenant

set +x

openstack image set \
	--unprotected \
	"$1"

openstack image delete "$1"
