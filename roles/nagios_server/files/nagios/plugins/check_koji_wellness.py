#!/usr/bin/env python
import sys
import re

import requests

koji_host = sys.argv[1]
try:
    koji_pkg = sys.argv[2]
except IndexError:
    koji_pkg = 'koji'

NAGIOS = {
    'OK': 0,
    'WARN': 1,
    'CRIT': 2
}

TARGETS = {
    'web': 'https://%s/koji/' % koji_host,
    'hub': 'https://%s/kojihub/' % koji_host,
    'pkg': 'https://%s/packages/%s/' % (koji_host, koji_pkg)
}


def do_request(url, method='GET', headers=None, body=None):
    try:
        res = getattr(requests, method.lower())(url, headers=headers, data=body)
    except requests.exceptions.ConnectionError as e:
        return (500, e.message)
    return (res.status_code, res.text)


def check_web():
    url = TARGETS['web']
    (status_code, data) = do_request(url)
    if status_code != 200:
        return (NAGIOS['CRIT'], 'Unable to access "%s"' % url)
    if not re.search(r'<div class="pageHeader">[a-zA-Z\s]+</div>', data):
        return (NAGIOS['WARN'], 'Unable to match content from "%s"' % url)
    return (NAGIOS['OK'], '')


def check_hub(method='system.listMethods'):
    url = TARGETS['hub']
    xmlrpc = '''<?xml version="1.0" encoding="utf-8"?>
    <methodCall>
        <methodName>%s</methodName>
        <params></params>
    </methodCall>''' % method
    headers = {
        'Content-Type': 'text/xml'
    }
    (status_code, data) = do_request(url, method='POST', headers=headers, body=xmlrpc)
    if status_code != 200:
        return (NAGIOS['CRIT'], 'Unable to access "%s"' % url)
    if len(re.findall(r'<value><string>[a-zA-Z0-9\._]+</string></value>', data)) == 0:
        return (NAGIOS['WARN'], 'Unable to parse content from "%s"' % url)
    return (NAGIOS['OK'], None)


def check_pkg():
    url = TARGETS['pkg']
    (status_code, data) = do_request(url)
    if status_code != 200:
        return (NAGIOS['CRIT'], 'Unable to access "%s"' % url)
    if len(re.findall(r'<img src="/icons/folder.gif" alt="\[DIR\]"> <a href="[0-9.\/]+">[0-9.\/]+</a>', data)) == 0:
        return (NAGIOS['WARN'], 'Unable to match content from "%s"' % url)
    return (NAGIOS['OK'], None)


def main():
    ok = NAGIOS['OK']
    for (code, msg) in (check_web(), check_hub(), check_pkg()):
        if code != ok:
            return (code, msg)
    return (ok, None)


if __name__ == '__main__':
    (code, reason) = main()
    if code != NAGIOS['OK']:
        sys.stderr.write('%s\n' % reason)
    else:
        sys.stdout.write('All checks passed.\n')
    sys.exit(code)
