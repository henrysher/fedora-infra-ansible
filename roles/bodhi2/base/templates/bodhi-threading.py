config = {
    # This sets uptwo master threads to handle incoming messages.
    # Each of those master consumer threads then can fork off many masher
    # threads to mash different repos.
    # If you crank up this number, you should also crank up:
    # - the iptables rules in inventory/group_vars/bodhi-backend
    # - the fedmsg endpoints in roles/fedmsg/base/templates/endpoints-bodhi.py
    "moksha.workers_per_consumer": 2,
    "moksha.threadpool_size": 22,
}
