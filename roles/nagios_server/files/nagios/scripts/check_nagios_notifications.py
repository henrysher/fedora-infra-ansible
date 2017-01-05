#!/usr/bin/env python
#
#  A script to read the Nagios status file and send email for notifications
#  off, but have recovered.
#
#  Written by Athmane Madjoudj <athmane@fedoraproject.org>, 2011-11-15
#  based on tummy.com's work <jafo@tummy.com>, 2010-11-16
#  Released under the GPLv2.

import re
from smtplib import SMTP
from email.mime.text import MIMEText
from socket import gethostname

# Settings
debug = 0
EMAIL_FROM="nagios@fedoraproject.org"
EMAIL_TO="sysadmin-noc-members@fedoraproject.org"
#EMAIL_TO="athmane@fedoraproject.org"
nagios_status_file = '/var/log/nagios/status.dat'

class NagiosStatus:
    def __init__(self, filename):
        self.filename = filename
        self.hosts = {}
        self.load_status_file()

    def load_status_file(self):
        fp = open(self.filename, 'r')
        while True:
            line = fp.readline()
            if not line: break

            m = re.match(r'^hoststatus\s+{\s*$', line)
            if m:
                if debug >= 2: print 'START OF HOST'
                data = { 'services' : [] }
                while True:
                    line = fp.readline()
                    if not line: break
                    if debug >= 2: print 'host: %s' % line.rstrip()
                    m2 = re.match(r'^\s+([^=]+)=(\S.*)*$', line.rstrip())
                    if not m2: break
                    data[m2.group(1)] = m2.group(2)
                self.hosts[data['host_name']] = data
                if debug >= 2: print 'END OF HOST'

            m = re.match(r'^servicestatus\s+{\s*$', line)
            if m:
                if debug >= 2: print 'START OF SERVICE'
                data = {}
                while True:
                    line = fp.readline()
                    if not line: break
                    if debug >= 2: print 'service: %s' % line.rstrip()
                    m2 = re.match(r'^\s+([^=]+)=(.*)$', line.rstrip())
                    if not m2: break
                    data[m2.group(1)] = m2.group(2)
                self.hosts[data['host_name']]['services'].append(data)
                if debug >= 2: print 'END OF SERVICE'

def main():
    status = NagiosStatus(nagios_status_file)
    output = ""
    for host in sorted(status.hosts.keys()):
        host = status.hosts[host]
        if host.get('notifications_enabled', None) == None:
            output+= 'Host %s has no notifications_enabled line \n' % host['host_name']
            continue

        #  are there any hard states that aren't 0 or 1?
        hard_states = [ x for x in
                [ int(x['last_hard_state']) for x in host['services'] ]
                if not x in [0,1] ]
        need_newline = False
        if host['notifications_enabled'] == '0' and not hard_states:
            output += ('Host %s has notifications disabled and all services ok \n'
                    % host['host_name'])
            need_newline = True

        for service in host['services']:
            if debug: print '%s@%s' % ( service['check_command'], host['host_name'] )
            if debug: print '   notifications_enabled: %(notifications_enabled)s  last_hard_state: %(last_hard_state)s' % service
            if (int(service['notifications_enabled']) == 0
                    and int(service['last_hard_state']) in [0,1]):
                output+= (('Service %(check_command)s@%(host_name)s\n'
                    '   has notifications disabled, but is ok\n') % service)
                need_newline = True

        if need_newline: output+="\n\n"
    
    if output.strip() != '':
        msg_body = "List of notifications off for recovered hosts/services: \n\n"+output
        msg = MIMEText(msg_body)
        msg['Subject']="Notifications status on %s" % gethostname()
        msg['From']=EMAIL_FROM
        msg['To']=EMAIL_TO
        smtp_conn = SMTP()
        smtp_conn.connect('localhost')
        smtp_conn.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
        smtp_conn.quit()

if __name__ == '__main__':
    main()
