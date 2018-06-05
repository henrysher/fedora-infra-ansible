ansible-role-osbs-namespace/operations
======================================

Collection of common maintenance operations for an OpenShift cluster.
By default, all tasks in this sub-roles are disabled. Use the control
booleans to enable the desired operations:

Requirements
------------

A running instance of OpenShift.

Role Variables
--------------


    # Update docker daemon on each OpenShift node.
    # It's highly recommended to use `serial: 1` in your playbook.
    osbs_upgrade_docker: false
    # Docker version to update to.
    osbs_docker_version: <default not set>

    # Update OpenShift node labels.
    osbs_update_node_labels: false
    # A list of labels to be applied to each OpenShift node.
    osbs_node_labels: []
    # A list of all predefined node selector labels
    osbs_managed_node_labels:
        - "auto_build=true"

    # Disable a node to make it safe to perform
    # operations such as restarting docker daemon
    # or any other risky maintenance
    osbs_disable_node: true
    # Then to re-enable node:
    osbs_enable_node: true

    # Override default systemd unit files
    osbs_systemd_override: true

See `operations/defaults/main.yml` for a comprehensive list of all
available variables.

Dependencies
------------

None.

Example Playbook
----------------

    - name: update docker
      hosts: nodes
      roles:
         - role: ansible-role-osbs-namespace/operations
           osbs_upgrade_docker: true
           osbs_docker_version: docker-1.12.6-61.git85d7426.el7

    - name: node maintenance
      hosts: nodes
      roles:
          - role: ansible-role-osbs-namespace/operations
            osbs_disable_node: true
          - role: my-maintenance-role
          - role: ansible-role-osbs-namespace/operations
            osbs_enable_node: true

License
-------

BSD

Author Information
------------------

Luiz Carvalho <lui@redhat.com>
