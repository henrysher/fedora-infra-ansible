import requests
import json
import subprocess
import logging

req = requests.get('https://bodhi.fedoraproject.org/composes/')
bodhi_composes = req.json()

if len(bodhi_composes['composes']) == 0:
    bodhi_push_cmd = ["bodhi-push", "--username", "releng"]
    push = subprocess.Popen(bodhi_push_cmd, stdout=PIPE, stderr=PIPE, stdin=PIPE)
    push.stdin.write('y')
