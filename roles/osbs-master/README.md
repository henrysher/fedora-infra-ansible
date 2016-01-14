osbs-master
===========

Main role for deploying OSBS - [OpenShift build
service](https://github.com/projectatomic/osbs-client/), service for building
layered Docker images.

It performs the necessary configuration of Docker and OpenShift and optionally
opens/closes OpenShift firewall port. It also generates self-signed certificate
that can be used by reverse proxy placed in front of the builder.

This role is part of
[ansible-osbs](https://github.com/projectatomic/ansible-osbs/) playbook for
deploying OpenShift build service. Please refer to that github repository for
[documentation](https://github.com/projectatomic/ansible-osbs/blob/master/README.md)
and [issue tracker](https://github.com/projectatomic/ansible-osbs/issues).

Role Variables
--------------

You may need to configure Docker to connect to registries over plain HTTP, or
HTTPS with self-signed certificate (especially when developing OSBS). You can
provide list of such registries in `osbs_docker_insecure_registries` (empty by
default).

    osbs_docker_insecure_registries: []

Expose the OpenShift port to the outside world? Set this to `false` when using
authenticating proxy on the localhost. Has no effect if `osbs_manage_firewalld`
is `false`.

    osbs_master_expose_port: true

Set to false if you don't use firewalld or do not want the playbook to modify
it.

    osbs_manage_firewalld: true

If you are using authenticating proxy, this role can generate a self-signed certificate that the proxy can use to authenticate itself to OpenShift. The proxy needs the certificate and the key concatenated in one file (`osbs_proxy_cert_file`). OpenShift needs to know the CA of the certificate, which is configured in `osbs_proxy_ca_file` and which is the same as the certificate because it is self-signed.

    osbs_proxy_cert_file: /etc/origin/proxy_selfsigned.crt
    osbs_proxy_key_file: /etc/origin/proxy_selfsigned.key
    osbs_proxy_certkey_file: /etc/httpd/openshift_proxy_certkey.crt
    osbs_proxy_ca_file: /etc/origin/proxy_selfsigned.crt

OpenShift authorization policy - which users should be assigned the view
(read-only), osbs-builder (read-write), and cluster-admin (admin) roles. In
default configuration, everyone has read/write access. The authentication is
handled by the proxy - if you are not using it the everyone connecting from the
outside belongs to the `system:unauthenticated` group.

Default setup:

    osbs_readonly_users: []
    osbs_readonly_groups: []
    osbs_readwrite_users: []
    osbs_readwrite_groups:
      - system:authenticated
      - system:unauthenticated
    osbs_admin_users: []
    osbs_admin_groups: []

Development with authenticating proxy:

    osbs_readonly_users: []
    osbs_readonly_groups: []
    osbs_readwrite_users: []
    osbs_readwrite_groups:
      - system:authenticated
    osbs_admin_users: []
    osbs_admin_groups: []

Example production configuration with only one user starting the builds:

    osbs_readonly_users: []
    osbs_readonly_groups:
      - system:authenticated
    osbs_readwrite_groups: []
    osbs_readwrite_users:
      - kojibuilder
    osbs_admin_users:
      - foo@EXAMPLE.COM
      - bar@EXAMPLE.COM
    osbs_admin_groups: []

Limit on the number of running pods.

    osbs_master_max_pods: 3

Dependencies
------------

OpenShift is expected to be installed on the remote host. This can by
accomplished by the
[install-openshift](https://github.com/projectatomic/ansible-role-install-openshift)
role.

Example Playbook
----------------

Simple development deployment:

    - hosts: builders
      roles:
        - install-openshift
        - osbs-master
        - atomic-reactor

Deployment behind authentication proxy that only allows the *kojibuilder* user
to start builds (and everyone to view them). Set docker to trust registry on
localhost:5000 even though it uses HTTP.

    - hosts: builders
      roles:
        - install-openshift
        - role: osbs-master
          osbs_master_expose_port: false
          osbs_docker_insecure_registries: [172.42.17.1:5000]
          osbs_readonly_users: []
          osbs_readonly_groups:
            - system:authenticated
            - system:unauthenticated
          osbs_readwrite_groups: []
          osbs_readwrite_users:
            - kojibuilder
          osbs_admin_users: []
          osbs_admin_groups: []
        - atomic-reactor
        - role: osbs-proxy
          osbs_proxy_type: kerberos
          osbs_proxy_kerberos_keytab_file: /etc/HTTP-FQDN.EXAMPLE.COM.keytab
          osbs_proxy_kerberos_realm: EXAMPLE.COM
          osbs_proxy_ssl_cert_file: /etc/fqdn.example.com.crt
          osbs_proxy_ssl_key_file: /etc/fqdn.example.com.key
          osbs_proxy_ip_whitelist:
            - subnet: 192.168.66.0/24
              user: kojibuilder

License
-------

BSD

Author Information
------------------

Martin Milata &lt;mmilata@redhat.com&gt;
