#!/usr/bin/env python
""" fedmsg-service-collectd.py -- produce collectd stats on fedmsg daemons """

import json
import os
import pprint
import socket
import sys
import time
import zmq


#hostname = socket.gethostname().split('.')[0]
hostname = socket.gethostname()  # Use FQDN, I guess..


def print_consumer(service, consumer):
    timestamp = int(time.time())
    print "PUTVAL %s/%s/queue_length-%s interval=5 %i:%i" % (
        hostname,
        service,
        '%s_backlog' % consumer['name'],
        timestamp,
        consumer['backlog']
    )
    print "PUTVAL %s/%s/gauge-%s interval=5 %i:%i" % (
        hostname,
        service,
        '%s_exceptions' % consumer['name'],
        timestamp,
        consumer['exceptions']
    )
    # These got introduced in a later version of moksha, so not every host has them
    if 'headcount_in' in consumer:
        print "PUTVAL %s/%s/gauge-%s interval=5 %i:%i" % (
            hostname,
            service,
            '%s_in' % consumer['name'],
            timestamp,
            consumer['headcount_in']
        )

    if 'headcount_out' in consumer:
        print "PUTVAL %s/%s/gauge-%s interval=5 %i:%i" % (
            hostname,
            service,
            '%s_out' % consumer['name'],
            timestamp,
            consumer['headcount_out']
        )

    # And these got introduced even later
    if 'times' in consumer:
        maxval = 1000 * max(consumer['times'] or [0])
        minval = 1000 * min(consumer['times'] or [0])

        avgval = 0
        if consumer['times']:
            avgval = 1000 * sum(consumer['times']) / len(consumer['times'])

        print "PUTVAL %s/%s/response_time-%s interval=5 %i:%i" % (
            hostname,
            service,
            '%s_min' % consumer['name'],
            timestamp,
            minval,
        )
        print "PUTVAL %s/%s/response_time-%s interval=5 %i:%i" % (
            hostname,
            service,
            '%s_max' % consumer['name'],
            timestamp,
            maxval,
        )
        print "PUTVAL %s/%s/response_time-%s interval=5 %i:%i" % (
            hostname,
            service,
            '%s_avg' % consumer['name'],
            timestamp,
            avgval,
        )


def print_producer(service, producer):
    timestamp = int(time.time())
    print "PUTVAL %s/%s/gauge-%s interval=5 %i:%i" % (
        hostname,
        service,
        '%s_exceptions' % producer['name'],
        timestamp,
        producer['exceptions']
    )


if __name__ == '__main__':
    service = "{{ process }}"
    fname = '/var/run/fedmsg/monitoring-%s.socket' % service

    if not os.path.exists(fname):
        print "UNKNOWN - %s does not exist" % fname
        sys.exit(3)

    connect_to = "ipc:///%s" % fname

    ctx = zmq.Context()
    s = ctx.socket(zmq.SUB)
    s.connect(connect_to)

    s.setsockopt(zmq.SUBSCRIBE, '')

    try:
        while True:
            msg = s.recv()
            msg = json.loads(msg)
            for consumer in msg['consumers']:
                 if consumer['initialized']:
                    print_consumer(service, consumer)
            for producer in msg['producers']:
                 if producer['initialized']:
                    print_producer(service, producer)
    except KeyboardInterrupt:
        pass
