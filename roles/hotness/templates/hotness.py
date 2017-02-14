import os
import socket
hostname = socket.gethostname().split('.', 1)[0]

description_template = """Latest upstream release: %(latest_upstream)s
Current version/release in %(repo_name)s: %(repo_version)s-%(repo_release)s
URL: %(url)s

Please consult the package updates policy before you issue an update to a stable branch: https://fedoraproject.org/wiki/Updates_Policy

More information about the service that created this bug can be found at: %(explanation_url)s

Please keep in mind that with any upstream change, there may also be packaging changes that need to be made. Specifically, please remember that it is your responsibility to review the new version to ensure that the licensing is still correct and that no non-free or legally problematic items have been added upstream.

Based on the information from anitya:  https://release-monitoring.org/project/%(projectid)s/
"""

config = {
    {% if env == 'staging' %}
    # Establish a loop from prod anitya back into the staging hotness.
    'endpoints': {
        'anitya-public-relay': [
            'tcp://release-monitoring.org:9940',
        ],
    },
    {% endif %}

    'hotness.bugzilla.enabled': True,

    'hotness.bugzilla': {
        'user': '{{ upstream_release_bugzilla_user }}',
        'password': '{{ upstream_release_bugzilla_password }}',
{% if env == 'staging' %}
        'url': 'https://partner-bugzilla.redhat.com',
        'explanation_url': 'https://stg.fedoraproject.org/wiki/Upstream_release_monitoring',
{% else %}
        'url': 'https://bugzilla.redhat.com',
        'explanation_url': 'https://fedoraproject.org/wiki/Upstream_release_monitoring',
{% endif %}
        'product': 'Fedora',
        'version': 'rawhide',
        'keywords': 'FutureFeature,Triaged',
        'bug_status': 'NEW',
        'short_desc_template': "%(name)s-%(latest_upstream)s is available",
        'description_template': description_template,
    },

    'hotness.koji': {
{% if env == 'staging' %}
        'server': 'https://koji.stg.fedoraproject.org/kojihub',
        'weburl': 'https://koji.stg.fedoraproject.org/koji',
{% else %}
        'server': 'https://koji.fedoraproject.org/kojihub',
        'weburl': 'https://koji.fedoraproject.org/koji',
{% endif %}
        'git_url': 'https://src.fedoraproject.org/git/rpms/{package}.git',

        'krb_principal': 'hotness/hotness01{{env_suffix}}.phx2.fedoraproject.org@{{ipa_realm}}',
        'krb_keytab': '/etc/krb5.hotness_hotness01{{env_suffix}}.phx2.fedoraproject.org.keytab',
        'krb_ccache': None,
        'krb_proxyuser': None,
        'krb_sessionopts': {'timeout': 3600, 'krb_rdns': False},

        'user_email': ('Fedora Release Monitoring ',
                       '<release-monitoring@fedoraproject.org>'),
        'opts': {'scratch': True},
        'priority': 30,
        'target_tag': 'rawhide',
    },

    'hotness.anitya': {
        'url': 'https://release-monitoring.org',
        'username': '{{ fedoraDummyUser }}',
        'password': '{{ fedoraDummyUserPassword }}',
    },

{% if env == 'staging' %}
    'hotness.pkgdb_url': 'https://admin.stg.fedoraproject.org/pkgdb/api',
    "hotness.mdapi_url": "https://apps.stg.fedoraproject.org/mdapi",
{% else %}
    'hotness.pkgdb_url': 'https://admin.fedoraproject.org/pkgdb/api',
    "hotness.mdapi_url": "https://apps.fedoraproject.org/mdapi",
{% endif %}

    'hotness.yumconfig': '/etc/hotness-yum.conf',

    # The time in seconds the-new-hotness should wait for a socket to connect
    # before giving up.
    'hotness.connect_timeout': 15,
    # The time in seconds the-new-hotness should wait for a read from a socket
    # before giving up.
    'hotness.read_timeout': 15,
    # The number of times the-new-hotness should retry a network request that
    # that failed for any reason (e.g. read timeout, DNS error, etc)
    'hotness.requests_retries': 3,

    "hotness.cache": {
        "backend": "dogpile.cache.dbm",
        "expiration_time": 290,
        "arguments": {
            "filename": "/var/tmp/the-new-hotness-cache.dbm",
        },
    },
}

