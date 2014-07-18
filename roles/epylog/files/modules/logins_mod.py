

#!/usr/bin/python -tt
"""
Description will eventually go here.
"""
##
# Copyright (C) 2003 by Duke University
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
# $Id$
#
# @Author Konstantin Ryabitsev <icon@linux.duke.edu>
# @version $Date$
#

import sys
import re
import time
import os
import sqlite3 as sqlite
sys.path.insert(0, '../py/')
from epylog import Result, InternalModule


def executeSQL(cursor, query, params=None):
    """
    Execute a python 2.5 (sqlite3) style query.

    @param cursor: A sqlite cursor
    @param query: The query to execute
    @param params: An optional list of parameters to the query
    """
    if params is None:
        return cursor.execute(query)
    
    return cursor.execute(query, params)

class logins_mod(InternalModule):
    def __init__(self, opts, logger):
        InternalModule.__init__(self)
        self.logger = logger
        self.opts = opts
        rc = re.compile

        self.ignore     = 0
        self.open       = 1
        self.failure    = 2
        self.root_open    = 11
        self.root_failure = 12
        self.pam_ignore = []
        self.xinetd_ignore = []
        self.logins_db = opts.get('loginsdb_path', '/var/lib/epylog/logins_db.sqlite') # where to keep the loginsdb
        self.time_fuzz = int(opts.get('time_fuzz', 60)) # how much to fuzz the time in minutes (default 60m)
        remove_older_than = int(opts.get('remove_older_than', 14)) # time in days to start remove from the db
        self.oldest_to_keep = time.time() - (remove_older_than*86400)
        if remove_older_than == '0': # if it is  zero then don't delete any, ever - hah your funeral
            self.oldest_to_keep = None

        ig_users = opts.get('ignore_users', '')
        ig_users.replace(',',' ')
        self.ignore_users = ig_users.split(' ')

        self.db_cx = None
        
        ##
        # PAM reports
        #
        pam_map = {
            rc('\(pam_unix\)\S*:.*authentication\s*failure'): self.pam_failure,
            rc('\(pam_unix\)\S*:\ssession\sopened\sfor'): self.pam_open,
            rc('\(pam_unix\)\S*:\sbad\susername'): self.pam_baduser,
            rc('\(pam_unix\)\S*:\sauth\scould\snot'): self.pam_chelper_failure,
            rc('pam_krb5\S*:\s\S+\ssucceeds\sfor'): self.pam_krb5_open,
            rc('pam_krb5\S*:\s\S+\sfails\sfor'): self.pam_krb5_failure
            }
        ##
        # XINETD reports
        #
        xinetd_map = {
            rc('xinetd\S*: START:'): self.xinetd_start
            }
        ##
        # SSH reports
        #
        sshd_map = {
            rc('sshd\[\S*: Accepted'): self.sshd_open,
            rc('sshd\[\S*: Failed'): self.sshd_failure
            }
        ##
        # IMAPD and IPOP3D
        #
        uw_imap_map = {
            rc('imapd\[\S*: Login\sfail'): self.uw_imap_failure,
            rc('imapd\[\S*: Authenticated\suser'): self.uw_imap_open,
            rc('imapd\[\S*: Login\suser'): self.uw_imap_open,
            rc('ipop3d\[\S*: Login\sfail'): self.uw_imap_failure,
            rc('ipop3d\[\S*: Login\suser'): self.uw_imap_open,
            rc('ipop3d\[\S*: Auth\suser'): self.uw_imap_open
            }
        ##
        # IMP
        #
        imp_map = {
            rc('IMP\[\S*: Login'): self.imp2_open,
            rc('IMP\[\S*: FAILED'): self.imp2_failure,
            rc('HORDE\[\S*\s*\[imp\] Login'): self.imp3_open,
            rc('HORDE\[\S*\s*\[imp\] FAILED'): self.imp3_failure
            }
        ##
        # DOVECOT
        #
        dovecot_map = {
            rc('imap-login:\sLogin:\s'): self.dovecot_open,
            rc('imap-login:\sAborted\slogin\s'): self.dovecot_failure
            }
        ##
        # Courier-IMAP
        #
        courier_map = {
            rc('\sLOGIN,\suser=\S+,\sip=\[\S+\]'): self.courier_open,
            rc('\sLOGIN FAILED,\sip=\[\S+\]'): self.courier_failure
            }
        ##
        # Cyrus-IMAP
        #
        cyrus_map = {
            rc('imapd\[\S*: login:'): self.cyrus_open,
            rc('pop3d\[\S*: login:'): self.cyrus_open,
            rc('imapd\[\S*: badlogin:'): self.cyrus_failure,
            rc('pop3d\[\S*: badlogin:'): self.cyrus_failure
            }
        ##
        # Qpopper
        #
        qpopper_map = {
            rc('apop\[\S*:\s\S+\sat\s.*\s\(\S*\):\s-ERR\s\[AUTH\]'): self.qpopper_failure,
            rc('apop\[\S*:\s\S+\sat\s.*\s\(\S*\):\s-ERR\s\[IN-USE\]'): self.qpopper_failure,
            rc('apop\[\S*:\s\(\S*\)\sPOP\slogin'): self.qpopper_open
            }

        ##
        # ProFTPD
        #
        proftpd_map = {
            rc('proftpd\[\S*:.*USER.*Login successful'): self.proftpd_open,
            rc('proftpd\[\S*:.*no such user found'): self.proftpd_failure,
            rc('proftpd\[\S*:.*Login failed'): self.proftpd_failure
        }

        regex_map = {}
        if opts.get('enable_pam', "1") != "0": regex_map.update(pam_map)
        if opts.get('enable_xinetd', "1") != "0": regex_map.update(xinetd_map)
        if opts.get('enable_sshd', "1") != "0": 
            regex_map.update(sshd_map)
            self.pam_ignore.append('sshd')
        if opts.get('enable_uw_imap', "0") != "0":
            regex_map.update(uw_imap_map)
            self.xinetd_ignore.append('imaps')
        if opts.get('enable_imp', "0") != "0": regex_map.update(imp_map)
        if opts.get('enable_dovecot',"0") != "0": regex_map.update(dovecot_map)
        if opts.get('enable_courier',"0") != "0": regex_map.update(courier_map)
        if opts.get('enable_cyrus', "0") != "0": regex_map.update(cyrus_map)
        if opts.get('enable_qpopper',"0") != "0": regex_map.update(qpopper_map)
        if opts.get('enable_proftpd',"0") != "0":
            regex_map.update(proftpd_map)
            self.pam_ignore.append('ftp')
            self.xinetd_ignore.append('ftp')

        self.safe_domains = []
        safe_domains = opts.get('safe_domains', '.*')
        for domain in safe_domains.split(','):
            domain = domain.strip()
            if domain:
                try:
                    domain_re = rc(domain)
                    self.safe_domains.append(domain_re)
                except:
                    logger.put(0, 'Error compiling domain regex: %s' % domain)
                    logger.put(0, 'Check config for Logins module!')

        self.regex_map = regex_map
        
        self.pam_service_re = rc('(\S+)\(pam_unix\)')
        self.pam_failure_re = rc('.*\slogname=(\S*).*\srhost=(\S*)')
        self.pam_failure_user_re = rc('\suser=(\S*)')
        self.pam_open_re = rc('.*for user (\S+) by\s(\S*)\s*\(uid=(\S+)\)')
        self.pam_failure_more_re = rc('(\S+)\smore\sauthentication\sfailures')
        self.pam_baduser_re = rc('\sbad\susername\s\[(.*)\]')
        self.pam_chelper_re = rc('password\sfor\s\[(.*)\]')
        self.pam_krb5_re = rc("^(\S+?)\[*\d*\]*:\spam_krb5\S*:\sauth.*\sfor\s`(\S+)'")
        self.xinetd_start_re = rc('START:\s*(\S*)\s')
        self.sshd_open_ruser_re = rc('Accepted\s(\S*)\sfor\s(\S*)\sfrom\s(\S*)\sport\s\d*\sruser\s(\S*)\s*(\S*)')
        self.sshd_open_re = rc('Accepted\s(\S*)\sfor\s(\S*)\sfrom\s(\S*)\sport\s\d+\s*(\S*)')
        self.sshd_fail_re = rc('Failed\s(\S*)\sfor.*\s(\S+)\sfrom\s(\S*)\sport\s\d*\s*(\S*)')
        self.uw_imap_fail_re = rc('auth=(.*)\shost=.*\[(\S*)\]')
        self.uw_imap_open_re = rc('user=(.*)\shost=.*\[(\S*)\]')
        self.uw_imap_service_re = rc('^(\S*)\[\d*\]:')
        self.dovecot_open_re = rc('Login:\s(\S+)\s\[(\S+)\]')
        self.dovecot_failure_re = rc('Aborted\slogin\s\[(\S+)\]')
        self.courier_open_re = rc('^(\S+?):.*\suser=(\S+),\sip=\[(\S+)\]')
        self.courier_failure_re = rc('^(\S+?):.*,\sip=\[(\S+)\]')
        self.imp2_open_re = rc('Login\s(\S*)\sto\s(\S*):\S*\sas\s(\S*)')
        self.imp2_fail_re = rc('FAILED\s(\S*)\sto\s(\S*):\S*\sas\s(\S*)')
        self.imp3_open_re = rc('success\sfor\s(\S*)\s\[(\S*)\]\sto\s\{(\S*):')
        self.imp3_fail_re = rc('LOGIN\s(\S*)\sto\s(\S*):\S*\sas\s(\S*)')
        self.proftpd_open_re = rc('proftpd\[\S*:.*\[(\S+)\].*USER\s(.*):\sLogin\ssuccessful')
        self.proftpd_failure_re = rc('proftpd\[\S*:.*\[(\S+)\].*USER\s([^:\s]*)')
        self.qpopper_open_re = rc('user "(.*)" at \(.*\)\s(\S*)')
        self.qpopper_fail_re = rc(':\s(.*)\sat\s(\S*)')
        self.cyrus_open_re = rc('login:.*\[(\S*)\]\s(\S*)\s')
        self.cyrus_fail_re = rc('badlogin:.*\[(\S*)\]\s\S\s(\S*)\sSASL')
        self.cyrus_service_re = rc('^(\S*)\[\d*\]:')
        
        self.sshd_methods = {'password': 'pw',
                             'publickey': 'pk',
                             'rhosts-rsa': 'rsa',
                             'rsa': 'rsa',
                             'hostbased': 'host',
                             'none': 'none'}

        self.report_wrap = '<table width="100%%" rules="cols" cellpadding="2">%s</table>'
        self.subreport_wrap = '<tr><th align="left" colspan="3"><h3>%s</h3></th></tr>\n%s\n'

        self.root_failures_title = '<font color="red">ROOT FAILURES</font>'
        self.root_logins_title = '<font color="blue">ROOT Logins</font>'
        self.user_failures_title = '<font color="red">User Failures</font>'
        self.user_logins_title = '<font color="blue">User Logins</font>'

        self.untrusted_host = '%(system)s::<font color="red">%(rhost)s</font>'

        self.flip = ' bgcolor="#dddddd"'

        self.line_rep = '<tr%s><td valign="top" width="15%%">%s</td><td valign="top" width="15%%">%s</td><td width="70%%">%s</td></tr>\n'

    ##
    # LINE MATCHING ROUTINES
    #
    def general_ignore(self, linemap):
        restuple = (self.ignore, None, None, None)
        return {restuple: 1}

    def pam_failure(self, linemap):
        action = self.failure
        self.logger.put(5, 'pam_failure invoked')
        system, message, mult = self.get_smm(linemap)
        service = self._get_pam_service(message)
        mo = self.pam_failure_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd pam failure string: %s' % message)
            return None
        byuser, rhost = mo.groups()
        mo = self.pam_failure_user_re.search(message)
        if mo: user = mo.group(1)
        else: user = 'unknown'
        if ((service == 'xscreensaver' and user == 'root')
            or service == 'sshd' or service == 'imap'):
            ##
            # xscreensaver will always fail as root.
            # SSHD is better handled by sshd part itself.
            # Imap failures are caught by imap routines.
            # Ignore these.
            #
            result = self.general_ignore(linemap)
            return result
        mo = self.pam_failure_more_re.search(message)
        if mo: mult += int(mo.group(1))
        restuple = self._mk_restuple(action, system, service, user,
                                     byuser, rhost, linemap['stamp'])
        return {restuple: mult}

    def pam_open(self, linemap):
        action = self.open
        system, message, mult = self.get_smm(linemap)
        service = self._get_pam_service(message)
        if service in self.pam_ignore:
            ##
            # the service will do a much better job.
            #
            result = self.general_ignore(linemap)
            return result
        mo = self.pam_open_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd pam open string: %s' % message)
            return None
        user, byuser, byuid = mo.groups()
        if byuser == '': byuser = self.getuname(int(byuid))
        restuple = self._mk_restuple(action, system, service, user, byuser, '', linemap['stamp'])
        return {restuple: mult}

    def pam_baduser(self, linemap):
        action = self.failure
        system, message, mult = self.get_smm(linemap)
        mo = self.pam_baduser_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd pam bad user string: %s' % message)
            return None
        user = mo.group(1)
        service = self._get_pam_service(message)
        restuple = self._mk_restuple(action, system, service, user, '', '', linemap['stamp'])
        return {restuple: mult}

    def pam_chelper_failure(self, linemap):
        action = self.failure
        system, message, mult = self.get_smm(linemap)
        mo = self.pam_chelper_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd pam console helper string: %s' % message)
            return None
        user = mo.group(1)
        service = self._get_pam_service(message)
        restuple = self._mk_restuple(action, system, service, user, '', '', linemap['stamp'])
        return {restuple: mult}

    def pam_krb5_open(self, linemap):
        action = self.open
        system, message, mult = self.get_smm(linemap)
        mo = self.pam_krb5_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd pam_krb5 succeeds line: %s' % message)
            return None
        service = mo.group(1)
        user = mo.group(2)
        if service == 'sshd':
            ##
            # sshd_open will do a much better job.
            #
            result = self.general_ignore(linemap)
            return result
        restuple = self._mk_restuple(action, system, service, user, '', '', linemap['stamp'])
        return {restuple: mult}

    def pam_krb5_failure(self, linemap):
        action = self.failure
        system, message, mult = self.get_smm(linemap)
        mo = self.pam_krb5_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd pam_krb5 failure line: %s' % message)
            return None
        service = mo.group(1)
        user = mo.group(2)
        if ((service == 'xscreensaver' and user == 'root')
            or service == 'sshd' or service == 'imap'):
            ##
            # xscreensaver will always fail as root.
            # SSHD is better handled by sshd part itself.
            # Imap failures are caught by imap routines.
            # Ignore these.
            #
            result = self.general_ignore(linemap)
            return result
        restuple = self._mk_restuple(action, system, service, user, '', '', linemap['stamp'])
        return {restuple: mult}
        
    def xinetd_start(self, linemap):
        action = self.open
        system, message, mult = self.get_smm(linemap)
        mo = self.xinetd_start_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd xinetd start string: %s' % message)
            return None
        service = mo.group(1)
        if service in self.xinetd_ignore:
            ##
            # the service will do a much better job.
            #
            result = self.general_ignore(linemap)
            return result
        restuple = self._mk_restuple(action, system, service, '', '', '', linemap['stamp'])
        return {restuple: mult}

    def sshd_open(self, linemap):
        action = self.open
        system, message, mult = self.get_smm(linemap)
        ruser = ''
        mo1 = self.sshd_open_ruser_re.search(message)
        mo2 = self.sshd_open_re.search(message)
        if mo1: method, user, rhost, ruser, service = mo1.groups()
        elif mo2: method, user, rhost, service = mo2.groups()
        else:
            self.logger.put(3, 'Odd sshd open string: %s' % message)
            return None
        method = self.sshd_methods.get(method, '??')
        rhost = self.gethost(rhost)
        if not service: service = 'ssh1'
        service = '%s(%s)' % (service, method)
        restuple = self._mk_restuple(action, system, service, user,
                                     ruser, rhost, linemap['stamp'])
        return {restuple: mult}

    def sshd_failure(self, linemap):
        action = self.failure
        system, message, mult = self.get_smm(linemap)
        mo = self.sshd_fail_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd sshd FAILURE string: %s' % message)
            return None
        method, user, rhost, service = mo.groups()
        method = self.sshd_methods.get(method, '??')
        rhost = self.gethost(rhost)
        if not service: service = 'ssh1'
        service = '%s(%s)' % (service, method)
        restuple = self._mk_restuple(action, system, service, user, '', rhost, linemap['stamp'])
        return {restuple: mult}

    def uw_imap_failure(self, linemap):
        action = self.failure
        system, message, mult = self.get_smm(linemap)
        service = self._get_uw_imap_service(message)
        service = '%s(uw)' % service
        mo = self.uw_imap_fail_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd imap FAILURE string: %s' % message)
            return None
        user, rhost = mo.groups()
        rhost = self.gethost(rhost)
        restuple = self._mk_restuple(action, system, service, user, '', rhost, linemap['stamp'])
        return {restuple: mult}

    def uw_imap_open(self, linemap):
        action = self.open
        system, message, mult = self.get_smm(linemap)
        service = self._get_uw_imap_service(message)
        service = '%s(uw)' % service
        mo = self.uw_imap_open_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd imap open string: %s' % message)
            return None
        user, rhost = mo.groups()
        rhost = self.gethost(rhost)
        restuple = self._mk_restuple(action, system, service, user, '', rhost, linemap['stamp'])
        return {restuple: mult}

    def dovecot_open(self, linemap):
        action = self.open
        system, message, mult = self.get_smm(linemap)
        service = 'imap(dc)'
        mo = self.dovecot_open_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd dovecot OPEN string: %s' % message)
            return None
        user, rhost = mo.groups()
        rhost = self.gethost(rhost)
        restuple = self._mk_restuple(action, system, service, user, '', rhost, linemap['stamp'])
        return {restuple: mult}

    def dovecot_failure(self, linemap):
        action = self.failure
        system, message, mult = self.get_smm(linemap)
        service = 'imap(dc)'
        mo = self.dovecot_failure_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd dovecot FAILURE string: %s' % message)
            return None
        rhost = mo.group(1)
        rhost = self.gethost(rhost)
        user = 'unknown'
        restuple = self._mk_restuple(action, system, service, user, '', rhost, linemap['stamp'])
        return {restuple: mult}

    def courier_open(self, linemap):
        action = self.open
        system, message, mult = self.get_smm(linemap)
        mo = self.courier_open_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd courier OPEN string: %s' % message)
            return None
        service, user, rhost = mo.groups()
        service = '%s(cr)' % service
        rhost = self.gethost(rhost)
        restuple = self._mk_restuple(action, system, service, user, '', rhost, linemap['stamp'])
        return {restuple: mult}

    def courier_failure(self, linemap):
        action = self.failure
        system, message, mult = self.get_smm(linemap)
        mo = self.courier_failure_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd courier FAILURE string: %s' % message)
            return None
        service, rhost = mo.groups()
        service = '%s(cr)' % service
        rhost = self.gethost(rhost)
        user = 'unknown'
        restuple = self._mk_restuple(action, system, service, user, '', rhost, linemap['stamp'])
        return {restuple: mult}

    def proftpd_open(self, linemap):
        action = self.open
        system, message, mult = self.get_smm(linemap)
        mo = self.proftpd_open_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd ProFTPD OPEN string: %s' % message)
            return None
        service = 'ftp(pro)'
        rhost, user = mo.groups()
        rhost = self.gethost(rhost)
        restuple = self._mk_restuple(action, system, service, user, '', rhost, linemap['stamp'])
        return {restuple: mult}

    def proftpd_failure(self, linemap):
        action = self.failure
        system, message, mult = self.get_smm(linemap)
        mo = self.proftpd_failure_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd ProFTPD FAILURE string: %s' % message)
            return None
        service = 'ftp(pro)'
        rhost, user = mo.groups()
        rhost = self.gethost(rhost)
        restuple = self._mk_restuple(action, system, service, user, '', rhost, linemap['stamp'])
        return {restuple: mult}

    def imp2_failure(self, linemap):
        action = self.failure
        system, message, mult = self.get_smm(linemap)
        mo = self.imp2_fail_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd IMP failure string: %s' % message)
            return None
        rhost, system, user = mo.groups()
        rhost = self.gethost(rhost)
        service = 'IMP2'
        restuple = self._mk_restuple(action, system, service, user, '', rhost, linemap['stamp'])
        return {restuple: mult}

    def imp2_open(self, linemap):
        action = self.open
        system, message, mult = self.get_smm(linemap)
        mo = self.imp2_open_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd IMP open string: %s' % message)
            return None
        rhost, system, user = mo.groups()
        rhost = self.gethost(rhost)
        service = 'IMP2'
        restuple = self._mk_restuple(action, system, service, user, '', rhost, linemap['stamp'])
        return {restuple: mult}

    def imp3_failure(self, linemap):
        action = self.failure
        system, message, mult = self.get_smm(linemap)
        mo = self.imp3_fail_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd IMP failure string: %s' % message)
            return None
        rhost, system, user = mo.groups()
        rhost = self.gethost(rhost)
        service = 'IMP3'
        restuple = self._mk_restuple(action, system, service, user, '', rhost, linemap['stamp'])
        return {restuple: mult}

    def imp3_open(self, linemap):
        action = self.open
        system, message, mult = self.get_smm(linemap)
        mo = self.imp3_open_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd IMP open string: %s' % message)
            return None
        user, rhost, system = mo.groups()
        rhost = self.gethost(rhost)
        service = 'IMP3'
        restuple = self._mk_restuple(action, system, service, user, '', rhost, linemap['stamp'])
        return {restuple: mult}

    def cyrus_failure(self,linemap):
        action = self.failure
        system, message, mult = self.get_smm(linemap)
        service = self._get_cyrus_service(message)
        mo = self.cyrus_fail_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd cyrus FAILURE string: %s' % message)
            return None
        rhost, user = mo.groups()
        rhost = self.gethost(rhost)
        restuple = self._mk_restuple(action, system, service, user, '', rhost, linemap['stamp'])
        return {restuple: mult}

    def cyrus_open(self,linemap):
        action = self.open
        system, message, mult = self.get_smm(linemap)
        service = self._get_cyrus_service(message)
        mo = self.cyrus_open_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd cyrus open string: %s' % message)
            return None
        rhost, user = mo.groups()
        rhost = self.gethost(rhost)
        restuple = self._mk_restuple(action, system, service, user, '', rhost, linemap['stamp'])
        return {restuple: mult}

    def qpopper_failure(self, linemap):
        action = self.failure
        system, message, mult = self.get_smm(linemap)
        mo = self.qpopper_fail_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd qpopper FAILURE string: %s' % message)
            return None
        user, rhost = mo.groups()
        rhost = self.gethost(rhost)
        service = 'qpopper'
        restuple = self._mk_restuple(action, system, service, user, '', rhost, linemap['stamp'])
        return {restuple: mult}

    def qpopper_open(self, linemap):
        action = self.open
        system, message, mult = self.get_smm(linemap)
        mo = self.qpopper_open_re.search(message)
        if not mo:
            self.logger.put(3, 'Odd qpopper open string: %s' % message)
            return None
        user, rhost = mo.groups()
        rhost = self.gethost(rhost)
        service = 'qpopper'
        restuple = self._mk_restuple(action, system, service, user, '', rhost, linemap['stamp'])
        return {restuple: mult}
    ##
    # HELPER METHODS
    #
    def _mk_restuple(self, action, system, service, user, byuser, rhost, stamp):
        if user == '': user = 'unknown'
        if user == 'root' or user == 'ROOT':
            action += 10
            remote = self._mk_userat(byuser, rhost)
            restuple = (action, system, service, remote, stamp)
        else:
            if rhost:
                match = 0
                for domain_re in self.safe_domains:
                    if domain_re.search(rhost):
                        match = 1
                        break
                if not match:
                    tmp = {'system': system, 'rhost': rhost}
                    system = self.untrusted_host % tmp
            restuple = (action, user, service, system, stamp)
        return restuple

    def _mk_dots(self, str, lim):
        if len(str) > lim:
            start = -(lim-2)
            str = '..' + str[start:]
        return str
        
    def _get_pam_service(self, str):
        service = 'unknown'
        mo = self.pam_service_re.search(str)
        if mo: service = mo.group(1)
        return service

    def _get_uw_imap_service(self, str):
        service = 'unknown'
        mo = self.uw_imap_service_re.search(str)
        if mo: service = mo.group(1)
        return service

    def _mk_userat(self, user, host):
        if user and host: userat = '%s@%s' % (user, host)
        elif user: userat = user
        elif host: userat = '@%s' % host
        else: userat = 'unknown'
        return userat

    def _get_cyrus_service(self, str):
        service = 'unknown'
        mo = self.cyrus_service_re.search(str)
        if mo: service = mo.group(1)
        return service



    def _check_for_login(self, username, service, hostname, tid):
        # check if we have a login which matches in the db,

        if not os.path.exists(self.logins_db):
            return False
        
        p = (username, service, hostname, self.last_entry)
        q = "select * from logins where username=? and service=? and host=? and pkey <= ?"
        if not self.db_cx:
            self._db_cx()
            
        cur = self.db_cx.cursor()
        ob = executeSQL(cur, q, p)
        for i in ob:
            # if we get any matches if they match within the fuzzed time then 
            # don't show it
            if  abs(tid - i[7]) <= self.time_fuzz*60:
                return True
        return False
    
    def _add_login(self, username, action, hostname, timestamp, service, u_from=None):
        if not self.db_cx:
            self._db_cx()
            
        cur = self.db_cx.cursor()
        t_st = time.localtime(int(timestamp))
        time_in_day = int(t_st[3]*60) + int(t_st[4])
        q = "insert into logins values (NULL, ?, ?, ?, ?, ?, ?, ?)"
        p = (action, username, hostname, u_from, service, timestamp, time_in_day)
        cur.execute(q, p)

        
    def _db_cx(self):
        if not os.path.exists(self.logins_db):
            self.db_cx = self._setup_logins_db()
        else:
            self.db_cx = sqlite.Connection(self.logins_db)
            
        q = "select max(pkey) from logins"
        last_e = executeSQL(self.db_cx.cursor(), q)
        val = last_e.fetchone()[0]
        if not val:
            self.last_entry = 0
        else:
            self.last_entry = val
        
    def _setup_logins_db(self):
        schema = [
        """PRAGMA synchronous="OFF";""",
        """CREATE TABLE logins ( pkey INTEGER PRIMARY KEY, action INTEGER, 
                username TEXT,  host TEXT, u_from TEXT, service TEXT, 
                stamp INTEGER, time_in_day INTEGER);""",
             ]

        cx = sqlite.Connection(self.logins_db)
        cursor = cx.cursor()
        for cmd in schema:
            executeSQL(cursor, cmd)
        
        return cx

    ##
    # FINALIZE!!
    #
    def finalize(self, rs):
        logger = self.logger
        ##
        # Prepare report
        #
        report = ''
        rep = {}
        
        # FIXME
        # go through each item in the rs
        # feed them into the db
        # pull back from the db all the info you need for the report
        # simplifies a lot of this code
        
        # chuck it all into the db
        for (rt,count) in rs.items():
            if rt[0] in (self.root_failure, self.root_open):
                (action, host, service, remote, stamp) = rt
                user = 'root'
            elif rt[0] in (self.open, self.failure):
                (action, user, service, host, stamp) = rt
                remote = 'NULL'
            else:
                continue
            if user in self.ignore_users:
                continue
            for num in range(0, count):
                self._add_login(user, action, host, stamp, service, remote)
        self.db_cx.commit()
        
        #return "lalallala"
        
        for action in [self.root_failure, self.root_open,
                      self.failure, self.open]:
            rep[action] = ''
            per_user = {}
            flipper = ''
            q = """select distinct username, service, host from logins where action = ? and pkey > ?"""
            p = (action, self.last_entry)
            act_tuple = [(i[0],i[1], i[2]) for i in executeSQL(self.db_cx.cursor(), q, p)]

            for entry in act_tuple:
                username = entry[0]
                if username not in per_user:
                    per_user[username] = {}
                service = entry[1]
                if service not in per_user[username]:
                    per_user[username][service] = []
                hn = entry[2]
                q = """select time_in_day from logins where username = ? and host = ? and service = ? and action = ? and pkey > ?"""
                p = (username, hn, service, action, self.last_entry)
            
                this_logins_times =  [row[0] for row in executeSQL(self.db_cx.cursor(), q, p)]
                count = 0
                for t in this_logins_times:
                    if not self._check_for_login(username, service, hn, t):
                        # DEBUG print 'new login %s %s %s %s' % (username, service, hn, t)
                        count += 1

                if count:
                    per_user[username][service].append('%s(%d)' % (hn, count))
                
            blank = 0
            for username in sorted(per_user):
                if flipper: flipper = ''
                else: flipper = self.flip
                for (svc,reps) in per_user[username].items():
                    if blank: key = '&nbsp;'
                    else: blank = 1
                    if reps:
                        rep[action] += self.line_rep % (flipper, username, 
                                                        svc, ', '.join(reps))
        
        if rep[self.root_failure]:
            report += self.subreport_wrap % (self.root_failures_title,
                                             rep[self.root_failure])
        if rep[self.root_open]:
            report += self.subreport_wrap % (self.root_logins_title,
                                             rep[self.root_open])
        if rep[self.failure]:
            report += self.subreport_wrap % (self.user_failures_title,
                                             rep[self.failure])
        if rep[self.open]:
            report += self.subreport_wrap % (self.user_logins_title,
                                             rep[self.open])

        report = self.report_wrap % report
        
        if self.oldest_to_keep:
            q = """delete from logins where stamp < ?"""
            p = (self.oldest_to_keep,)
            executeSQL(self.db_cx.cursor(), q, p)
            self.db_cx.commit()
            
        return report

if __name__ == '__main__':
    from epylog.helpers import ModuleTest
    ModuleTest(logins_mod, sys.argv)
    
