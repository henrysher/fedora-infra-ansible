#!/usr/bin/env python

import json
import os
import socket
import sys
import zmq

try:
    service = sys.argv[1]
    check_list = frozenset(sys.argv[2:])
    fname = '/var/run/fedmsg/monitoring-%s.socket' % service

    if not check_list:
        print "UNKNOWN - empty list of fedmsg consumers and producers to check"
        sys.exit(3)

    if not os.path.exists(fname):
        print "UNKNOWN - %s does not exist" % fname
        sys.exit(3)

    connect_to = "ipc:///%s" % fname
    ctx = zmq.Context()
    s = ctx.socket(zmq.SUB)
    s.connect(connect_to)
    s.setsockopt(zmq.SUBSCRIBE, '')
    poller = zmq.Poller()
    poller.register(s, zmq.POLLIN)

    timeout = 10000

    events = dict(poller.poll(timeout))
    if s in events and events[s] == zmq.POLLIN:
        msg = s.recv()
        msg = json.loads(msg)
    else:
       print 'UNKNOWN - ZMQ timeout.  No message received in %i ms' % timeout
       sys.exit(3)

    for consumer in msg['consumers']:
        if consumer['name'] in check_list and not consumer['initialized']:
            print 'ERROR: fedmsg consumer %s is not initialized' % consumer['name']
            sys.exit(2)

    for producer in msg['producers']:
        if producer['name'] in check_list and not producer['initialized']:
            print 'ERROR: fedmsg producer %s is not initialized' % producer['name']
            sys.exit(2)

    for item in check_list:
        if item not in [p['name'] for p in msg['producers'] + msg['consumers']]:
            print 'ERROR: %s not found among installed plugins' % item
            sys.exit(2)

    print "OK: fedmsg consumer(s) and producer(s) initialized"
    sys.exit(0)

except Exception as err:
    print "UNKNOWN:", str(err)
    sys.exit(3)
