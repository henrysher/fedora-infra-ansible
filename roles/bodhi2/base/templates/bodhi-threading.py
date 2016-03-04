config = {
    # This sets uptwo master threads to handle incoming messages.
    # Each of those master consumer threads then can fork off many masher
    # threads to mash different repos.
    # If you crank up this number, you should also crank up:
    # - the iptables rules in inventory/group_vars/bodhi-backend
    # - the fedmsg endpoints in roles/fedmsg/base/templates/endpoints-bodhi.py
    {% if inventory_hostname.startswith('bodhi-backend02') %}
    # https://github.com/fedora-infra/bodhi/issues/795
    "moksha.workers_per_consumer": 1,
    {% else %}
    "moksha.workers_per_consumer": 2,
    {% endif %}
    "moksha.threadpool_size": 22,
}
