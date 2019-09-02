#! /bin/bash

# Helper script to delete (protected) OpenStack image in one step.
# See: https://docs.pagure.org/copr.copr/how_to_upgrade_builders.html

. /home/copr/cloud/keystonerc_proper_tenant

set +x

openstack image set \
	--unprotected \
	"$1"

openstack image delete "$1"
