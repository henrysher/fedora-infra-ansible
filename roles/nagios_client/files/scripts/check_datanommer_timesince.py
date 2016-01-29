#!/usr/bin/env python
""" NRPE check for datanommer/fedmsg health.
Given a category like 'bodhi', 'buildsys', or 'git', return an error if
datanommer hasn't seen a message of that type in such and such time.
You can alternatively provide a 'topic' which might look like
org.fedoraproject.prod.bodhi.update.comment.

Requires:  python-dateutil

Usage:

    $ check_datanommer_timesince CATEGORY WARNING_THRESH CRITICAL_THRESH

:Author: Ralph Bean <rbean@redhat.com>

"""

import dateutil.relativedelta
import subprocess
import sys
import json


def query_timesince(identifier):
    # If it has a '.', then assume it is a topic.
    if '.' in identifier:
        cmd = 'datanommer-latest --topic %s --timesince' % identifier
    else:
        cmd = 'datanommer-latest --category %s --timesince' % identifier
    sys.stderr.write("Running %r\n" % cmd)
    process = subprocess.Popen(cmd.split(), shell=False,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    prefix, stdout = stdout.split("INFO] ", 1)
    data = json.loads(stdout)
    return float(data[0])


def main():
    identifier, warning_threshold, critical_threshold = sys.argv[-3:]
    timesince = query_timesince(identifier)
    warning_threshold = int(warning_threshold)
    critical_threshold = int(critical_threshold)

    time_strings = []
    rd = dateutil.relativedelta.relativedelta(seconds=timesince)
    for denomination in ['years', 'months', 'days', 'hours', 'minutes', 'seconds']:
        value = getattr(rd, denomination, 0)
        if value:
            time_strings.append("%d %s" % (value, denomination))

    string = ", ".join(time_strings)
    reason = "datanommer has not seen a %r message in %s" % (identifier, string)

    if timesince > critical_threshold:
        print "CRIT: ", reason
        sys.exit(2)

    if timesince > warning_threshold:
        print "WARN: ", reason
        sys.exit(1)

    print "OK: ", reason
    sys.exit(0)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print "UNKNOWN: ", str(e)
        sys.exit(3)
