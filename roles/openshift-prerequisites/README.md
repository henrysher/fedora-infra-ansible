OpenShift prerequisites Role
============================

An Ansible role to manage prerequisites for OSE installation.
It performs the following operations:

* Sets necessary sebools for GlusterFS and NFS.
  https://docs.openshift.com/container-platform/3.3/install_config/install/prerequisites.html#prereq-selinux
* Installs python-six package
  https://github.com/openshift/openshift-ansible/issues/3020


Role Variables Example
----------------------

    # Set up sebools
    openshift_sebools:
    - name: virt_sandbox_use_fusefs
      state: yes
      persistent: yes


Example Playbook
----------------

    - hosts: all
      roles:
      - openshift-prerequisites


Dependencies
------------

None.
