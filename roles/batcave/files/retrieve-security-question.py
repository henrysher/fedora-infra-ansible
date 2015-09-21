#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
# Use this script to retrieve the security_question and security_answer from FAS (requires FAS >= 0.8.14)
# Author: Patrick Uiterwijk <puiterwijk@fedoraproject.org>
#
# Copyright 2012 Patrick Uiterwijk. All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE FEDORA PROJECT ''AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO
# EVENT SHALL THE FREEBSD PROJECT OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
# OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF
# ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies,
# either expressed or implied, of the Fedora Project.


import os
import getpass
import sys
import gpgme
from fedora.client import AccountSystem
from fedora.client import AuthError
from fedora.client import ServerError
import argparse
from io import BytesIO


parser = argparse.ArgumentParser()
parser.add_argument('admin_user', help='The user as which to log in to retrieve the question and answer')
parser.add_argument('target_user', help='The user of which to retrieve the security question and answer')
parser.add_argument('--verbose', action='store_true')
parser.add_argument('--no-answer', action='store_true', help='Only show the question, do not decrypt the answer')
parser.add_argument('--site', help='The FAS URL to get the information from')
parser.add_argument('--insecure', action='store_true', default=False,
        help='Do not check the certificate for the server.  *WARNING*: Only use this for testing')
parser.add_argument('--gpg_home', help='The directory where secring.gpg and pubring.gpg reside')
args = parser.parse_args()

args.admin_pass = getpass.getpass()

if args.site == None:
    args.site = 'https://admin.fedoraproject.org/accounts/'

if args.verbose:
    print 'Using site: %(site)s' % {'site': args.site}

if args.verbose:
    if args.gpg_home == None:
        print 'Using default gpg_home'
    else:
        print 'Using gpg_home: %(gpghome)s' % {'gpghome': args.gpg_home}

if args.gpg_home != None:
    os.putenv('GNUPGHOME', args.gpg_home)

fas = AccountSystem(args.site, username=args.admin_user, password=args.admin_pass, insecure=args.insecure)

if args.verbose:
    print 'Getting user details...'
try:
    details = fas.person_by_username(args.target_user)
except AuthError:
    print 'Failed to login to FAS. Please check admin_user and admin_pass!'
    sys.exit(2)
except ServerError:
    print 'Failed to retrieve user details: the server reported an error!'
    sys.exit(3)

if not 'username' in details.keys():
    print 'Error: user %(username)s is not known on this FAS site!' % {'username': args.target_user}
    sys.exit(4)

if not 'security_question' in details.keys():
    print 'Error: security_question was not retrieved by FAS! Are you sure you are using FAS >= 0.8.14, and that admin_user has the privileges to retrieve security_question?'
    sys.exit(5)

if details.security_question == None or details.security_answer == None:
    print 'Error: unable to retrieve security_question or security_answer. Are you sure you have privileges to return this information?'
    sys.exit(6)

if not args.no_answer:
    if args.verbose:
        print 'Decrypting answer...'
    cipher = BytesIO(details.security_answer.encode('utf-8'))
    plain = BytesIO()
    ctx = gpgme.Context()
    ctx.decrypt(cipher, plain)
    details.security_answer = plain.getvalue()

print 'Security question: %(question)s' % {'question': details.security_question}
if not args.no_answer:
    print 'Security answer: %(answer)s' % {'answer': details.security_answer}
