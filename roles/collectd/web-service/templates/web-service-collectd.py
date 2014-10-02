#!/usr/bin/env python
""" monitor website request times for collectd """

import time
import socket
import urllib


hostname = socket.gethostname()  # Use FQDN, I guess..


def get_loadtime(url):
    start = time.time()
    _ = urllib.urlopen(url)
    return time.time() - start


if __name__ == '__main__':
    site = "{{ site }}"
    url = "{{ url }}"
    interval = int("{{ interval }}")

    try:
        while True:
            loadtime = get_loadtime(url)
            timestamp = int(time.time())
            print "PUTVAL %s/%s/delay-%s interval=%i %i:%f" % (
                hostname, 'web', site, interval, timestamp, loadtime)
            time.sleep((interval - (loadtime % interval)) % interval)
    except KeyboardInterrupt:
        pass
