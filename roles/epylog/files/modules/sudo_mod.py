#!/usr/bin/python -tt
"""
Reports on sudo usage by users.

Jeremy Kindy (kindyjd at wfu.edu), Wake Forest University
"""

import sys
import re

##
# This is for testing purposes, so you can invoke this from the
# modules directory. See also the testing notes at the end of the
# file.
#
sys.path.insert(0, '../py/')
from epylog import Result, InternalModule

class sudo_mod(InternalModule):
    def __init__(self, opts, logger):
        InternalModule.__init__(self)
        self.logger = logger
        self.logger.put(2, 'initializing sudo')
        rc = re.compile

        self.ignore = 0
        self.open = 1
        self.not_allowed = 2

        sudo_map = {
            rc('.*sudo\:\s+\S+\s\:\sTTY'): self.sudo,
            rc('.*sudo:'): self.sudo_na
            }

        do_sudo = int(opts.get('enable_sudo', '1'))

        self.regex_map = {}
        if do_sudo: self.regex_map.update(sudo_map)
        
        self.sudo_user_name_re = rc('sudo:\s*(\S*)')
        self.sudo_as_user_re = rc('.*USER=(\S*)\s\;\sCOMMAND')
        self.sudo_command_name_re = rc('.*COMMAND=(.*)')
        self.sudo_error_message_re = rc('sudo:\s*\S*\s+:\s+(.*)\s+;\s+TTY')


        self.sudo_title = '<font color="blue">User Sudo Report</font>'
        self.sudo_open_title = '<font color="blue">User Sudo Report</font>'
        self.sudo_not_allowed_title = '<font color="red">Disallowed Sudo Commands</font>'

        self.report_wrap = '<table border="0" width="100%%" rules="cols" cellpadding="2">%s</table>'
        self.subreport_wrap = '<tr><th colspan="5" align="left"><h3>%s</h3></th></tr>\n%s'
        self.subreport_na_wrap = '<tr><th colspan="5" align="left"><h3>%s</h3></th></tr>\n%s'
        
        self.line_rep = '<tr%s><td valign="top" width="15%%">%s</td><td valign="top" width="45%%" colspan="2">%s</td><td width="25%%">%s</td><td width="15%%">%s</td></tr>\n'
        self.line_rep_na = '<tr%s><td valign="top" width="15%%">%s</td><td valign="top" width="30%%">%s</td><td valign="top" width="15%%">%s</td><td width="25%%">%s</td><td width="15%%">%s</td></tr>\n'

        self.flip = ' bgcolor="#dddddd"'


    ##
    # Line-matching routines
    #
    def sudo(self, linemap):
        action = self.open
        self.logger.put(2, 'sudo invoked')
        sys, msg, mult = self.get_smm(linemap)

        self.logger.put(3, 'test sudo %d' % mult)
        user = self._get_sudo_user(msg)
        self.logger.put(3, 'sudo user: %s' % user)
        asuser = self._get_sudo_as_user(msg)
        self.logger.put(3, 'sudo asuser: %s' % asuser)
        command_name = self._get_sudo_command_name(msg)
        self.logger.put(3, 'sudo command: %s' % command_name)

        restuple = self._mk_restuple(sys, action, user, asuser, command_name, None)
        self.logger.put(2, 'sudo finished')
        return {restuple: mult}

    def sudo_na(self, linemap):
        action = self.not_allowed
        self.logger.put(2, 'sudo_na invoked')
        sys, msg, mult = self.get_smm(linemap)

        self.logger.put(3, 'test sudo %d' % mult)
        user = self._get_sudo_user(msg)
        self.logger.put(3, 'sudo user: %s' % user)
        asuser = self._get_sudo_as_user(msg)
        self.logger.put(3, 'sudo asuser: %s' % asuser)
        command_name = self._get_sudo_command_name(msg)
        self.logger.put(3, 'sudo command: %s' % command_name)
        error_message = self._get_sudo_error_message(msg)
        self.logger.put(3, 'sudo error_message: %s' % error_message)

        restuple = self._mk_restuple(sys, action, user, asuser, command_name, error_message)
        self.logger.put(2, 'sudo finished')
        return {restuple: mult}

    def sudo_ignore(self, linemap):
        restuple = self._mk_restuple(None, self.ignore, None, None, None, None)
        return {restuple: 1}

    ##
    # Helpers
    #
    def _mk_restuple(self, sys, action, user=None, asuser=None, command_name=None, error_message=None):
        return (action, user, command_name, asuser, error_message, sys)
        #return (sys, action, user, asuser, command_name)

    def _get_sudo_user(self, str):
        user = 'unknown'
        mo = self.sudo_user_name_re.search(str)
        if mo: user = mo.group(1)
        return user

    def _get_sudo_as_user(self, str):
        asuser = 'unknown'
        mo = self.sudo_as_user_re.search(str)
        if mo: asuser = mo.group(1)
        return asuser

    def _get_sudo_error_message(self, str):
        pass_attempts = 0
        mo = self.sudo_error_message_re.search(str)
        if mo: pass_attempts = mo.group(1)
        return pass_attempts

    def _get_sudo_command_name(self, str):
        command_name = 'unknown'
        mo = self.sudo_command_name_re.search(str)
        if mo: command_name = mo.group(1)
        return command_name


    ####
    # Finalize the report
    def finalize(self, rs):
        logger = self.logger
        ##
        # Prepare report
        #
        report = ''
        rep = {}

        # (action, user, command_name, system, error_message)
        for action in [self.open, self.not_allowed]:
            rep[action] = ''
            flipper = ''
            for user in rs.get_distinct((action,)):
                #logger.put(2, 'sudo user: %s' % user)
                if flipper: flipper = ''
                else: flipper = self.flip
                service_rep = []
                blank = 0
                for command_name in rs.get_distinct((action, user)):
                    for asuser in rs.get_distinct((action, user, command_name)):
                        for error_message in rs.get_distinct((action, user, command_name, asuser)):
                            mymap = rs.get_submap((action, user, command_name, asuser, error_message))
                            #logger.put(2, 'sudo command_name: %s' % command_name)
                            key2s = []
                            for key2 in mymap.keys():
                                hostname = key2[0]
                                key2s.append('%s(%d)' % (hostname, mymap[key2]))
                            hostnames = ', '.join(key2s)
                            #logger.put(2, 'sudo hostnames: %s' % hostnames)
                            service_rep.append([command_name, hostnames, asuser, error_message])
                for svcrep in service_rep:
                    #logger.put(2, 'sudo svcrep: %s' % svcrep)
                    if blank: user = '&nbsp;'
                    else: blank = 1
                    if (action == self.open):
                        rep[action] += self.line_rep % (flipper, user, svcrep[0], svcrep[1], svcrep[2])
                    else:
                        rep[action] += self.line_rep_na % (flipper, user, svcrep[0], svcrep[3], svcrep[1], svcrep[2])


        if rep[self.open]:
            report += self.subreport_wrap % (self.sudo_open_title, rep[self.open])
            logger.put(2, 'sudo report: self.open added')

        if rep[self.not_allowed]:
            report += self.subreport_na_wrap % (self.sudo_not_allowed_title, rep[self.not_allowed])
            logger.put(2, 'sudo report: self.not_allowed added')

        report = self.report_wrap % report
        return report


if __name__ == '__main__':
    from epylog.helpers import ModuleTest
    ModuleTest(sudo_mod, sys.argv)
