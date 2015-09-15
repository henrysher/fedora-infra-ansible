#!/bin/bash
mailto='admin@fedoraproject.org'
source /root/sshagent >>/dev/null
export ANSIBLE_HOST_KEY_CHECKING=False
/srv/web/infra/ansible/scripts/public-db-copy >& /dev/null
