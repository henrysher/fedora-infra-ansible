#! /bin/bash

# Once we have snapshot (builder image) in OpenStack, we need to make it public,
# protected, and setup hw_rng_model attribute.  This script simplifies the task.
# See https://docs.pagure.org/copr.copr/how_to_upgrade_builders.html

. /home/copr/cloud/keystonerc_proper_tenant

set +x

openstack image set \
	--public \
	--protected \
	--property hw_rng_model=virtio \
	"$1"
