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
