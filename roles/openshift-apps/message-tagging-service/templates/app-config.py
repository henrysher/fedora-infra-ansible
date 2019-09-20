# -*- coding: utf-8 -*-


class BaseConfiguration:
    log_level = 'DEBUG'

    koji_cert = None
    keytab = '/etc/krb5.keytab'
    principal = '{{ app }}/{{ app }}{{ env_suffix }}.fedoraproject.org@{{ ipa_realm }}'

    messaging_backend = 'fedora-messaging'
    build_state = 'ready'

    {% if env == 'staging' %}

    dry_run = True
    # Running in staging, a rule file inside my perosnal repo is used in order to test conveniently.
    rules_file_url = 'https://pagure.io/mts-rules/raw/master/f/rules.yaml'
    mbs_api_url = 'https://mbs.stg.fedoraproject.org/module-build-service/1/'
    koji_profile = 'stg'

    {% else %}

    # Disable dry_run when enable MTS
    dry_run = True
    rules_file_url = ('https://infrastructure.fedoraproject.org/cgit/ansible.git/tree/'
                      'roles/openshift-apps/message-tagging-service/files/mts-rules.yml')
    mbs_api_url = 'https://mbs.fedoraproject.org/module-build-service/1/'
    koji_profile = 'koji'

    {% endif %}
