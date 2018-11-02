#!/usr/bin/env python
from __future__ import print_function
import sys
import requests
import json
import subprocess
import logging

req = requests.get('https://bodhi.fedoraproject.org/composes/')
bodhi_composes = req.json()

if len(bodhi_composes['composes']) == 0:
    bodhi_push_cmd = ['bodhi-push', '--username', 'releng']
    push = subprocess.Popen(bodhi_push_cmd, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    push.stdin.write('y')
    _, err = push.communicate()
    push.wait()
    if push.returncode != 0:
        print(err, file=sys.stderr)
        sys.exit(1)
