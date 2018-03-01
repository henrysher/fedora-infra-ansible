osbs-secret
===========

This role imports various secrets, such as Pulp or Koji certificates, from
filesystem into OpenShift. See the [OSBS
documentation](https://github.com/projectatomic/osbs-client/blob/master/docs/secret.md)
for more information.

This role is part of
[ansible-osbs](https://github.com/projectatomic/ansible-osbs/) playbook for
deploying OpenShift build service. Please refer to that github repository for
[documentation](https://github.com/projectatomic/ansible-osbs/blob/master/README.md)
and [issue tracker](https://github.com/projectatomic/ansible-osbs/issues).

Role Variables
--------------

The role imports the keys from the machine running ansible. You have to provide
`osbs_secret_files` list, which enumerates what files to import. Elements of
the list are dictionaries with two keys: `source` and `dest`. Source is the
location of the file on the machine where ansible is run. Dest is the filename
of the secret.

    osbs_secret_files:
    - source: /home/user/.pulp/pulp.cer
      dest: pulp.cer
    - source: /home/user/.pulp/pulp.key
      dest: pulp.key

The name of the secret in OpenShift is defined by the `osbs_secret_name`
variable.

    osbs_secret_name: pulpsecret

The secret has to be associated with a service account. This service account
can be set by the `osbs_secret_service_account` variable.

    osbs_secret_service_account: builder

We need a kubeconfig file on the remote machine in order to talk to OpenShift.
Its location is contained in the `pulp_secret_kubeconfig`.

    osbs_kubeconfig_path: /etc/origin/master/admin.kubeconfig

Example Playbook
----------------

Following playbook imports the keys from my home directory on the machine where
ansible is executed. You may need to run something like this after the current
set of keys expires.

    - hosts: builders
      roles:
      - role: osbs-secret
        osbs_secret_name: pulpsecret
        osbs_secret_files:
        - source: /home/mmilata/.pulp/pulp.cer
          dest: pulp.cer
        - source: {{ pulp_secret_local_dir }}/pulp.key
          dest: pulp.key

License
-------

BSD

Author Information
------------------

Martin Milata &lt;mmilata@redhat.com&gt;
