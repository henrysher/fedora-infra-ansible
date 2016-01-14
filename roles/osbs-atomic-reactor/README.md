atomic-reactor
==============

This role obtains
[atomic-reactor](https://github.com/projectatomic/atomic-reactor) docker image
to be used in [OSBS (OpenShift build
service)](https://github.com/projectatomic/osbs-client).

This role is part of
[ansible-osbs](https://github.com/projectatomic/ansible-osbs/) playbook for
deploying OpenShift build service. Please refer to that github repository for
[documentation](https://github.com/projectatomic/ansible-osbs/blob/master/README.md)
and [issue tracker](https://github.com/projectatomic/ansible-osbs/issues).

Role Variables
--------------

`atomic_reactor_source` determines the means of obtaining the There are
currently two methods to obtain the image, `pull` and `git`. The `pull` method
simply pulls the image from a given registry. The `git` method builds the image
by running `docker build` on given git repository.

    atomic_reactor_source: pull

When `atomic_reactor_source` is set to `pull`, you need to provide
`atomic_reactor_pull` dictionary such as the following:

    atomic_reactor_pull:
      registry: registry.hub.docker.com
      image: slavek/atomic-reactor:latest

When `atomic_reactor_source` is set to `git`, you need to provide
`atomic_reactor_git` dictionary such as the following:

    atomic_reactor_git:
      # base image source to be pulled (optional)
      base_registry: registry.hub.docker.com
      base_image: library/fedora:latest
      # allow retagging the base image to match FROM in Dockerfile (optional)
      base_image_retag: fedora:latest
      # Dockerfile source
      git_url: https://github.com/projectatomic/atomic-reactor.git
      git_branch: master
      git_subdir: ""
      git_local_path: "{{ ansible_env.HOME }}/atomic-reactor-buildroot"

OSBS expects the build image to be named `buildroot`. This name can be changed
by setting the `atomic_reactor_tag` variable.

    atomic_reactor_tag: buildroot

Dependencies
------------

Docker needs to be installed on the remote host.

Example Playbook
----------------

In default configuration the role pulls the image from
[slavek/atomic-reactor](https://hub.docker.com/r/slavek/atomic-reactor/)
repository on docker hub.

    - hosts: builders
      roles:
         - atomic-reactor

License
-------

BSD

Author Information
------------------

Martin Milata &lt;mmilata@redhat.com&gt;
