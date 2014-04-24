#!/usr/bin/python -tt
# skvidal@fedoraproject.org
# gplv2+

#nagios definition
## 'host-notify-by-jabber' command definition
#define command{
#        command_name    host-notify-by-jabber
#        command_line    /usr/local/bin/xmppsend -a config.ini "Host '$HOSTALIAS$' is $HOSTSTATE$ - Info : $HOSTOUTPUT$" $CONTACTPAGER$
#        }
#
## 'notify-by-jabber' command definition
#define command{
#        command_name    notify-by-jabber
#        command_line    /usr/local/bin/xmppsend -a config.ini "$NOTIFICATIONTYPE$ $HOSTNAME$ $SERVICED ESC$ $SERVICESTATE$ $SERVICEOUTPUT$ $LONGDATETIME$" $CONTACTPAGER$
#        }
#

# needs a config file to get username/pass/other info format is:

#[xmpp_nagios]
#server=jabber.org
#resource=nagios
#port=5222
#username=yourusername
#password=yourpasssword

defaults = {'server':'jabber.org',
            'port':'5222',
            'resource':'nagios'}

# until xmppony is inplace

import warnings
warnings.simplefilter("ignore")

import xmpp
from xmpp.protocol import Message


from optparse import OptionParser
import ConfigParser
import sys
import os


parser = OptionParser()
parser.add_option("-a", dest="authfile", default=None, help="file to retrieve username/password/server/port/resource information from")
opts, args = parser.parse_args()

conf = ConfigParser.ConfigParser(defaults=defaults)
if not opts.authfile or not os.path.exists(opts.authfile):
   print "no config/auth file specified, can't continue"
   sys.exit(1)

conf.read(opts.authfile)
if not conf.has_section('xmpp_nagios') or not conf.has_option('xmpp_nagios', 'username') or not conf.has_option('xmpp_nagios', 'password'):
    print "cannot find at least one of: config section 'xmpp_nagios' or username or password"
    sys.exit(1)
server = conf.get('xmpp_nagios', 'server')
username = conf.get('xmpp_nagios', 'username')
password = conf.get('xmpp_nagios', 'password')
resource = conf.get('xmpp_nagios', 'resource')
port = conf.get('xmpp_nagios', 'port')


if len(args) < 1:
    print "xmppsend message [to whom, multiple args]"
    sys.exit(1)

msg = args[0]

msg = msg.replace('\\n', '\n')

c = xmpp.Client(server=server, port=port, debug=[])
con  = c.connect()
if not con:
    print "Error: could not connect to server: %s:%s" % (c.Server, c.Port)
    sys.exit(1)

auth = c.auth(user=username, password=password, resource=resource)
if not auth:
    print "Error: Could not authenticate to server: %s:%s" % (c.Server, c.Port)
    sys.exit(1)

if len(args) < 2:
    r = c.getRoster()
    for user in r.keys():
        if user == username:
            continue
        c.send(Message(user, '%s' % msg))
else:
    for user in args[1:]:
        c.send(Message(user, '%s' % msg))


    
