#!/usr/bin/env python

import json
import os
import socket
import sys
import zmq

try:
    service = sys.argv[1]
    check_consumer = sys.argv[2]
    exceptions_warning = sys.argv[3]
    exceptions_critical = sys.argv[4]
    fname = '/var/run/fedmsg/monitoring-%s.socket' % service
    if not os.path.exists(fname):
        print "UNKNOWN - %s does not exist" % fname
        sys.exit(3)
    connect_to = "ipc:///%s" % fname
    ctx = zmq.Context()
    s = ctx.socket(zmq.SUB)
    s.connect(connect_to)
    s.setsockopt(zmq.SUBSCRIBE, '')
    msg = s.recv()
    msg = json.loads(msg)

    for consumer in msg['consumers']:
        if consumer['name'] == check_consumer:
            if consumer['exceptions'] > exceptions_critical:         
                print 'CRITICAL: fedmsg consumer %s exceptions value is %i' % (consumer['name'],consumer['exceptions'])
                sys.exit(2)
            elif consumer['exceptions'] > exceptions_warning:
                print 'WARNING: fedmsg consumer %s exceptions value is %i' % (consumer['name'],consumer['exceptions'])
                sys.exit(1)
            else:
                print 'OK: fedmsg consumer %s exceptions value is %i' % (consumer['name'],consumer['exceptions'])
                sys.exit(0)

except Exception as err:
    print "UNKNOWN:", str(err)
    sys.exit(3)
