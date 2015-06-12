import operator


def invert_fedmsg_policy(hosts, vars):
    """ Given hostvars that map hosts -> topics, invert that
    and return a dict that maps topics -> hosts.

    Really, returns a list of tuples -- not a dict.
    """

    inverted = {}
    for host in hosts:
        prefix = '.'.join([vars[host]['fedmsg_prefix'],
                           vars[host]['fedmsg_env']])
        fqdn = vars[host].get('fedmsg_fqdn', vars[host]['ansible_fqdn'])

        for cert in vars[host]['fedmsg_certs']:
            for topic in cert.get('can_send', []):
                key = prefix + '.' + topic
                inverted[key] = inverted.get(key, [])
                inverted[key].append(cert['service'] + '-' + fqdn)

    result = inverted.items()
    result.sort(key=operator.itemgetter(0))
    return result


class FilterModule(object):
    def filters(self):
        return {
            "invert_fedmsg_policy": invert_fedmsg_policy,
        }
