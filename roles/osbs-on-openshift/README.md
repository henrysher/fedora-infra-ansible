osbs-on-openshift
=================

Role for deploying OSBS on top of a pre-existing [OpenShift](https://openshift.org)
cluster where we do not have cluster admin.

- [OpenShift build service](https://github.com/projectatomic/osbs-client/),
service for building layered Docker images.

This role is based on
[ansible-role-osbs-common](https://github.com/projectatomic/ansible-role-osbs-common)
upstream but the `osbs-common` role in Fedora Infra was pre-existing and used as
a location for common tasks required of all nodes in an osbs cluster.

This role is part of
[ansible-osbs](https://github.com/projectatomic/ansible-osbs/)
playbook for deploying OpenShift build service. Please refer to that github
repository for [documentation](https://github.com/projectatomic/ansible-osbs/blob/master/README.md)
and [issue tracker](https://github.com/projectatomic/ansible-osbs/issues).
