#!/usr/bin/python -tt -W ignore::DeprecationWarning
##
# Copyright (C) 2012 by Konstantin Ryabitsev and contributors
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
import os
import re
import sys
import cgi
import logging
import urllib2

import totpcgi
import totpcgi.backends

logging.basicConfig(level=logging.info)

if len(sys.argv) > 1:
    # blindly assume it's the config file
    config_file = sys.argv[1]
else:
    config_file = '/etc/totpcgi/totpcgi.conf'

import ConfigParser

from fedora.client import AuthError
from fedora.client.fasproxy import FasProxyClient

config = ConfigParser.RawConfigParser()
config.read(config_file)

require_pincode = config.getboolean('main', 'require_pincode')
success_string  = config.get('main', 'success_string')

fas_url = config.get('main', 'fas_url')
try:
    fas = FasProxyClient(fas_url)
except Exception, e:
    logging.exception("Problem connecting to FAS")
    sys.exit(1)

backends = totpcgi.backends.Backends()

try:
    backends.load_from_config(config)
except totpcgi.backends.BackendNotSupported, ex:
    logging.exception("Backend engine not supported")
    sys.exit(1)

### Begin custom Fedora Functions

def google_auth_fas_pincode_verify(user, pincode):
    if not fas.verify_password(user, pincode):
      raise totpcgi.UserPincodeError('User Password Error')

backends.pincode_backend.verify_user_pincode = google_auth_fas_pincode_verify

client_id = '1'

def parse_token(token):
    if token > 44:
        otp = token[-44:]
    if otp.startswith('ccccc'):
        return token[:-44], otp

    # Not a password + yubikey
    return False

class YubikeyAuthenticator(object):
    auth_regex = re.compile('^status=(?P<rc>\w{2})')
    def __init__(self, require_pincode=False):
        self.require_pincode = require_pincode

    def verify_user_token(self, user, token):
        # Parse the token apart into a password and token
        password, otp = parse_token(token)

        # Verify token against yubikey server
        server_prefix = 'http://yubikey:8080/yk-val/verify?id='
        server_url = server_prefix + client_id + "&otp=" + otp

        fh = urllib2.urlopen(server_url)

        for line in fh:
            match = self.auth_regex.search(line.strip('\n'))
            if match:
                if match.group('rc') == 'OK':
                    # Yubikey token is valid
                    break
                raise totpcgi.VerifyFailed(line.split('=')[1])
        else:
            raise totpcgi.VerifyFailed('yk-val returned malformed response')


        # Verify that the yubikey token belongs to the user
        # As a side effect, verify the password is good as well
        # if the user+password are wrong, this will raise a fedora.client.AuthError
        try:
            response = fas.send_request('/config/list/%s/yubikey' % user,
                    auth_params={'username': user, 'password': password})
        except AuthError, e:
            raise totpcgi.VerifyFailed('User Password Error: %s' % e)
        if not response[1].configs.prefix or not response[1].configs.enabled:
            raise totpcgi.VerifyFailed('Yubikey OTP unconfigured')
        elif len(response[1].configs.prefix) != 12:
            raise totpcgi.VerifyFailed('Invalid Yubikey OTP prefix')
        if not otp.startswith(response[1].configs.prefix):
            raise totpcgi.VerifyFailed('Unauthorized/Invalid OTP')

        # Okay, everything passed
        return 'Valid yubikey returned'


### End of custom Fedora Functions

def bad_request(why):
    output = 'ERR\n' + why + '\n'
    sys.stdout.write('Status: 400 BAD REQUEST\n')
    sys.stdout.write('Content-type: text/plain\n')
    sys.stdout.write('Content-Length: %s\n' % len(output))
    sys.stdout.write('\n')

    sys.stdout.write(output)
    sys.exit(0)

def cgimain():
    form = cgi.FieldStorage()

    must_keys = ('user', 'token', 'mode')

    for must_key in must_keys:
        if must_key not in form:
            bad_request("Missing field: %s" % must_key)

    user  = form.getfirst('user')
    token = form.getfirst('token')
    mode  = form.getfirst('mode')

    remote_host = os.environ['REMOTE_ADDR']

    if mode != 'PAM_SM_AUTH':
        bad_request('We only support PAM_SM_AUTH')

    if parse_token(token):
        ga = YubikeyAuthenticator(require_pincode)
    else:
        # totp/googleauth
        ga = totpcgi.GoogleAuthenticator(backends, require_pincode)

    try:
        status = ga.verify_user_token(user, token)
    except Exception, ex:
        logging.warning(
            "TOKEN FAILURE! user=%s, mode=%s, host=%s, message=%s",
            user,
            mode,
            remote_host,
            str(ex))
        bad_request(str(ex))

    logging.info(
        "Token success! user=%s, mode=%s, host=%s, message=%s",
        user,
        mode,
        remote_host,
        status)

    sys.stdout.write('Status: 200 OK\n')
    sys.stdout.write('Content-type: text/plain\n')
    sys.stdout.write('Content-Length: %s\n' % len(success_string))
    sys.stdout.write('\n')

    sys.stdout.write(success_string)

if __name__ == '__main__':
    try:
        cgimain()
    except Exception:
        logging.exception("Server error during processing")
        output = 'ERR\nInternal server error\n'
        sys.stdout.write('Status: 500 SERVER ERROR\n')
        sys.stdout.write('Content-type: text/plain\n')
        sys.stdout.write('Content-Length: %s\n' % len(output))
        sys.stdout.write('\n')

        sys.stdout.write(output)
        sys.exit(0)
