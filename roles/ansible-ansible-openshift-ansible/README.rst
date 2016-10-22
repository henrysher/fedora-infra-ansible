ansible-ansible-openshift-ansible
#################################

Ansible role to run ansible on a remote "openshift control" what will run
`openshift-ansible`_ to deploy a cluster.

This is a Fedora Infrastructure specific adaptation into a role of the original
prototype located in pagure:

    https://pagure.io/ansible-ansible-openshift-ansible/tree/master

What? Why?
----------

The `openshift-ansible`_ playbooks require that various tasks be run on
``localhost`` in order to build their internal abstracted representation of the
inventory list. Running potentially arbitrary code from external sources on a
bastion host (which is what ``localhost`` would be as the ansible control
machine) is often frowned upon. The goal here is to allow for the deployment of
`openshift-ansible`_ via an intermediate host.

.. note::
    There is a requirement to setup the SSH keys such that the bastion host
    can passwordless ssh into the openshift control host and such that the
    openshift control host can passwordless ssh into each of the hosts in
    the openshift cluster. This is outside the scope of this document.


::

    +---------------+                   +-------------------+
    |               |                   |                   |
    | bastion host  +----[ansible]----->| openshift control |
    |               |                   |                   |
    +---------------+                   +---------+---------+
                                                  |
                                                  |
                                              [ansible]
                                                  |
                                                  |
                                                  V
    +--------------------------------------------------------------------------+
    |                                                                          |
    |  openshift cluster                                                       |
    |                                                                          |
    |  +-----------+               +-----------+   +-----------+               |
    |  |           |               |           |   |           |               |
    |  | openshift |  ...[masters] | openshift |   | openshift |   ...[nodes]  |
    |  |  master   |               |   node    |   |   node    |               |
    |  |           |               |           |   |           |               |
    |  +-----------+               +-----------+   +-----------+               |
    |                                                                          |
    +--------------------------------------------------------------------------+

