osbs-namespace
==============

Setup an OpenShift namespace as required by OSBS:
- Create namespace, also referred to as project (`osbs_namespace`)
- Create service accounts (`osbs_service_accounts`)

If user is cluster admin (`osbs_is_admin`), the following is also performed:
- Create policy binding
- Create osbs-custom-build role to allow custom builds
- Sets up rolebindings for specified users, groups and service accounts

For orchestrator namespaces (`osbs_orchestrator`):
- reactor-config-secret is generated and stored in `osbs_generated_config_path`
  use osbs-secret to import it
- client-config-secret is generated and stored in `osbs_generated_config_path`
  use osbs-secret to import it

Requirements
------------

A running instance of OpenShift.

Role Variables
--------------

    # Namespace name to be used
    osbs_namespace: 'my-namespace'
    # Is user running playbook as cluster admin?
    osbs_is_admin: true
    # Will the namespace be used for orchestrator builds?
    osbs_orchestrator: true

    # Worker clusters to be used for generating reactor and client config secrets
    # in orchestrator workspace
    osbs_worker_clusters:
      x86_64:
        - name: prod-first-x86_64
          max_concurrent_builds: 6
          openshift_url: https://my-first-x86_64-cluster.fedoraproject.org:8443
        - name: prod-second-x86_64
          max_concurrent_builds: 16
          openshift_url: https://my-second-x86_64-cluster.fedoraproject.org
          # optional params, and their defaults:
          enabled: true # yaml boolean
          namespace: worker
          use_auth: 'true' # yaml string
          verify_ssl: 'true' # yaml string

      ppc64le:
        - name: prod-ppc64le
          max_concurrent_builds: 6
          openshift_url: https://my-ppc64le-cluster.fedoraproject.org:8443

    # Reactor config maps to be created in orchestrator namespace
    osbs_reactor_config_maps:
    - name: reactor-config-map
      # See config.json schema in atomic-reactor project for details:
      # https://github.com/projectatomic/atomic-reactor/blob/master/atomic_reactor/schemas/config.json
      data:
        clusters:
            x86_64:
            -   enabled: true
                max_concurrent_builds: 10
                name: x86_64-on-premise
        version: 1

    # Service accounts to be created - these accounts will also be bound to
    # edit clusterrole and osbs-custom-build role in specified namespace
    osbs_service_accounts:
    - bot
    - ci

    # Users and groups to be assigned view clusterrole in specified namespace
    osbs_readonly_groups:
    - group1
    - group2
    osbs_readonly_users:
    - user1
    - user2

    # Users and groups to be assigned edit clusterrole and osbs-custom-build
    # role in specified namespace
    osbs_readwrite_groups:
    - group1
    - group2
    osbs_readwrite_users:
    - user1
    - user2

    # Users and groups to be assigned admin clusterrole and osbs-custom-build
    # role in specified namespace
    osbs_admin_groups:
    - group1
    - group2
    osbs_admin_users:
    - user1
    - user2

    # Users and groups to be assigned cluster-reader clusterrole cluster wide
    osbs_cluster_reader_groups:
    - group1
    - group2
    osbs_cluster_reader_users:
    - user1
    - user2

    # Koji integration
    osbs_koji_secret_name: kojisecret
    osbs_koji_hub: https://koji.fedoraproject.org  # Empty default value
    osbs_koji_root: https://koji.fedoraproject.org/kojihub  # Empty default value

    # Pulp integration
    osbs_pulp_secret_name: pulpsecret
    osbs_pulp_registry_name: brew-qa  # Empty default value

    # Distribution registry integration
    osbs_registry_secret_name: v2-registry-dockercfg
    osbs_registry_api_version:
    - v1
    - v2
    osbs_registry_uri: https://distribution.registry.fedoraproject.org/v2  # Empty default value

    # Dist-git integration
    osbs_sources_command: fedpkg sources
    osbs_source_registry_uri: https://source.registry.fedoraproject.org  # Empty default value

    # Pruning
    osbs_prune: false
    osbs_prune_schedule: '0 0 */8 * *'
    osbs_prune_secret: ''
    osbs_prune_image: ''
    osbs_prune_commands: ["/prune.sh"]

For a full list, see defaults/main.yml

Dependencies
------------

None.

Example Playbook
----------------

    - name: setup worker namespace
      hosts: master
      roles:
         - role: osbs-namespace
           osbs_namespace: worker

    - name: setup orchestrator namespace
      hosts: master
      roles:
         - role: osbs-namespace
           osbs_namespace: orchestrator
           osbs_orchestrator: true

License
-------

BSD

Author Information
------------------

Luiz Carvalho <lui@redhat.com>
