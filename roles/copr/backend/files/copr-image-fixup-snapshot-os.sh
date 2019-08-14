#! /bin/bash

. /home/copr/cloud/keystonerc_proper_tenant

set +x

openstack image set \
	--public \
	--protected \
	--property hw_rng_model=virtio \
	"$1"
