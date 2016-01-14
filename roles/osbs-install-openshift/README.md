install-openshift
=================

Installs OpenShift v3 from various sources. Currently supports installing RPM
from COPR and building and installing the RPM from source code.

This role is part of
[ansible-osbs](https://github.com/projectatomic/ansible-osbs/) playbook for
deploying OpenShift build service. Please refer to that github repository for
[documentation](https://github.com/projectatomic/ansible-osbs/blob/master/README.md)
and [issue tracker](https://github.com/projectatomic/ansible-osbs/issues).

Role Variables
--------------

You need to specify which method of installation you want to use. Valid options
are `copr` (default) and `source`.

    install_openshift_method: copr

You must specify particular version that should be installed from the COPR.
Can be in either `version` or `version-release` format.

    install_openshift_copr_version: 1.0.5

When building from source, you need to specify the version of the built package.

    install_openshift_source_version: 1.0.5

Git commit to build packages from.

    install_openshift_source_commit: c66613fded194b10ce4e4e1c473fbfc0a511405b

File name of the tarball to be downloaded from github.

    install_openshift_source_archive: openshift-{{ install_openshift_source_commit }}.tar.gz

Directory for rpmbuild.

    install_openshift_source_rpmbuild_dir: "{{ ansible_env.HOME }}/rpmbuild"

Example Playbook
----------------

    - hosts: builders
      roles:
         - role: install-openshift
           install_openshift_method: copr

License
-------

BSD

Author Information
------------------

Martin Milata &lt;mmilata@redhat.com&gt;
