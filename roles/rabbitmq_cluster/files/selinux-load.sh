#!/bin/sh

set -e
set -x

checkmodule -M -m -o /etc/nagios/nrpe_rabbitmq.mod /etc/nagios/nrpe_rabbitmq.te
semodule_package -o /etc/nagios/nrpe_rabbitmq.pp -m /etc/nagios/nrpe_rabbitmq.mod
semodule -i /etc/nagios/nrpe_rabbitmq.pp
rm /etc/nagios/nrpe_rabbitmq.mod /etc/nagios/nrpe_rabbitmq.pp