#!/usr/bin/env python

import json
import os
import socket
import sys
import zmq

try:
    service = sys.argv[1]
    check_consumer = sys.argv[2]
    backlog_warning = int(sys.argv[3])
    backlog_critical = int(sys.argv[4])
    fname = '/var/run/fedmsg/monitoring-%s.socket' % service

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
        if consumer['name'] == check_consumer:
            if consumer['backlog'] is None:
                print 'ERROR: fedmsg consumer %s is not initialized' % consumer['name']
                sys.exit(3)
            elif consumer['backlog'] > backlog_critical:
                print 'CRITICAL: fedmsg consumer %s backlog value is %i' % (consumer['name'],consumer['backlog'])
                sys.exit(2)
            elif consumer['backlog'] > backlog_warning:
                print 'WARNING: fedmsg consumer %s backlog value is %i' % (consumer['name'],consumer['backlog'])
                sys.exit(1)
            else:
                print 'OK: fedmsg consumer %s backlog value is %i' % (consumer['name'],consumer['backlog'])
                sys.exit(0)

    print "UNKNOWN: fedmsg consumer %s not found" % check_consumer
    sys.exit(3)
except Exception as err:
    print "UNKNOWN:", str(err)
    sys.exit(3)
