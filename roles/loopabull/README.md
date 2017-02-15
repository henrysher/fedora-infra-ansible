Loopabull
=========

Fedora's deployment of [loopabull](https://github.com/maxamillion/loopabull)

Role Variables
--------------

See defaults/main.yml for full docs on role variables

Example Playbook
----------------

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - {
            role: loopabull,
                plugin: fedmsg,
                routing_keys: [
                    "org.fedoraproject.prod.buildsys.build.state.change"
                ],
                playbooks_dir: /usr/local/loopabull-playbooks/,
                ansible_cfg_path: /etc/ansible/ansible.cfg,
                playbook_cmd: /usr/bin/ansible-playbook

         }

License
-------

GPLv3+

Author Information
------------------

Adam Miller (maxamillion@fedoraproject.org)

