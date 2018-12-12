!/bin/bash

openstack overcloud deploy --templates \
  -e /home/stack/templates/node-info.yaml\
  -e /home/stack/templates/overcloud_images.yaml \
  -r /home/stack/templates/roles_data.yaml \
  --ntp-server cloud-noc01.cloud.fedoraproject.org \
  -e /home/stack/templates/custom-storage.yaml \
  --overcloud-ssh-user heat-admin \
  --overcloud-ssh-key ~/.ssh/id_rsa \
  -e /home/stack/templates/custom_domain.yaml \
  --timeout 1800 \
  --validation-errors-nonfatal

#  --config-download \
#  -e /usr/share/openstack-tripleo-heat-templates/environments/config-download-environment.yaml \
#  -e /home/stack/templates/rhel-registration/environment-rhel-registration.yaml \
#  -e /home/stack/templates/rhel-registration/rhel-registration-resource-registry.yaml \
