#!/usr/bin/env python

import arrow
import json
import os
import socket
import sys
import time
import zmq

try:
    service = sys.argv[1]
    check_producer = sys.argv[2]
    elapsed_warning = int(sys.argv[3])
    elapsed_critical = int(sys.argv[4])
    fname = '/var/run/fedmsg/monitoring-%s.socket' % service

    if not os.path.exists(fname):
        print "UNKNOWN - %s does not exist" % fname
        sys.exit(3)

    if not os.access(fname, os.W_OK):
        print "UNKNOWN - cannot write to %s" % fname
        sys.exit(3)

    connect_to = "ipc:///%s" % fname
    ctx = zmq.Context()
    s = ctx.socket(zmq.SUB)
    s.connect(connect_to)
    s.setsockopt(zmq.SUBSCRIBE, '')

    poller = zmq.Poller()
    poller.register(s, zmq.POLLIN)

    timeout = 20000

    events = dict(poller.poll(timeout))
    if s in events and events[s] == zmq.POLLIN:
        msg = s.recv()
        msg = json.loads(msg)
    else:
       print 'UNKNOWN - ZMQ timeout.  No message received in %i ms' % timeout
       sys.exit(3)

    now = time.time()

    for prod in msg['producers']:
        if prod['name'] != check_producer:
            continue
        diff = now - prod['last_ran']
        then = arrow.get(prod['last_ran']).humanize()
        if diff > elapsed_critical:
            print "CRITICAL: %s last ran %s (%i seconds ago)" % (
                check_producer, then, diff)
            sys.exit(2)
        elif diff > elapsed_warning:
            print "WARNING: %s last ran %s (%i seconds ago)" % (
                check_producer, then, diff)
            sys.exit(1)
        else:
            print "OK: %s last ran %s (%i seconds ago)" % (
                check_producer, then, diff)
            sys.exit(0)

    print "UNKNOWN: fedmsg producer %s not found" % check_producer
    sys.exit(3)
except Exception as err:
    print "UNKNOWN:", str(err)
    sys.exit(3)
