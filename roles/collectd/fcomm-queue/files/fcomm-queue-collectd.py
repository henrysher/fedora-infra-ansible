#!/usr/bin/env python
import retask.queue
import socket
import time

interval = 2

hostname = socket.gethostname().split('.')[0]

queue = retask.queue.Queue('fedora-packages')
queue.connect()

while True:
    print "PUTVAL %s/redis/queue_length interval=%i %i:%i" % (
        hostname,
        interval,
        int(time.time()),
        queue.length,
    )
    time.sleep(interval)
