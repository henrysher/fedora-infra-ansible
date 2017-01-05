#!/usr/bin/env python
""" Nagios check for haproxy over-subscription.

fedmsg-gateway is the primary concern as it can eat up a ton of simultaneous
connections.

:Author:  Ralph Bean <rbean@redhat.com>
"""

import socket
import sys


def _numeric(value):
    """ Type casting utility """
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def query(sockname="/var/run/haproxy-stat"):
    """ Read stats from the haproxy socket and return a dict """
    s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    s.connect("/var/run/haproxy-stat")
    s.send('show info\n')
    try:
        response = s.recv(1024).strip()
        lines = response.split('\n')
        data = dict([map(str.strip, line.split(':')) for line in lines])
        data = dict([(k, _numeric(v)) for k, v in data.items()])
        return data
    except Exception, e:
        print str(e)
    finally:
        s.close()

    return None


def nagios_check(data):
    """ Print warnings and return nagios exit codes. """

    current = data['CurrConns']
    maxconn = data['Maxconn']
    percent = 100 * float(current) / float(maxconn)
    details = "%.2f%% subscribed.  %i current of %i maxconn." % (
        percent, current, maxconn,
    )

    if percent < 50:
        print "HAPROXY SUBS OK: " + details
        return 0

    if percent < 75:
        print "HAPROXY SUBS WARN: " + details
        return 1

    if percent <= 100:
        print "HAPROXY SUBS CRIT: " + details
        return 2

    print "HAPROXY SUBS UNKNOWN: " + details
    return 3


if __name__ == '__main__':
    try:
        data = query(sockname="/var/run/haproxy-stat")
    except Exception as e:
        print "HAPROXY SUBS UNKNOWN: " + str(e)
        sys.exit(3)
    sys.exit(nagios_check(data))
