#!/usr/bin/python -tt
"""
Reports on selinux messages

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

class selinux_mod(InternalModule):
    def __init__(self, opts, logger):
        InternalModule.__init__(self)
        self.logger = logger
        self.logger.put(3, 'initializing selinux')
        rc = re.compile

        self.ignore = 0
        self.preventing = 1

        selinux_map = {
            rc('.*setroubleshoot\: SELinux is preventing'): self.selinux
            }

        do_selinux = int(opts.get('enable_selinux', '1'))

        self.regex_map = {}
        if do_selinux: self.regex_map.update(selinux_map)
        
        self.selinux_message_re = rc('setroubleshoot: (.*). For complete SELinux')

        self.selinux_title = '<font color="blue">SELinux Report</font>'
        self.selinux_preventing_title = '<font color="blue">SELinux Prevention Report</font>'

        self.report_wrap = '<table border="0" width="100%%" rules="cols" cellpadding="2">%s</table>'
        self.subreport_wrap = '<tr><th colspan="2" align="left"><h3>%s</h3></th></tr>\n%s'
        
        self.line_rep = '<tr%s><td valign="top" width="25%%">%s</td><td valign="top" width="75%%">%s</td></tr>\n'

        self.flip = ' bgcolor="#dddddd"'


    ##
    # Line-matching routines
    #
    def selinux(self, linemap):
        action = self.preventing
        self.logger.put(3, 'selinux invoked')
        sys, msg, mult = self.get_smm(linemap)

        self.logger.put(3, 'test selinux %d' % mult)
        message = self._get_selinux_message(msg)
        self.logger.put(3, 'selinux message: %s' % message)

        restuple = self._mk_restuple(sys, action, message)
        self.logger.put(3, 'selinux finished')
        return {restuple: mult}


    ##
    # Helpers
    #
    def _mk_restuple(self, sys, action, message):
        return (action, message, sys)

    def _get_selinux_message(self, str):
        message = 'unknown'
        mo = self.selinux_message_re.search(str)
        if mo: message = mo.group(1)
        return message


    ####
    # Finalize the report
    def finalize(self, rs):
        logger = self.logger
        ##
        # Prepare report
        #
        report = ''
        rep = {}

        # (action, message)
        for action in [self.preventing]:
            rep[action] = ''
            flipper = ''
            for message in rs.get_distinct((action,)):
                if flipper: flipper = ''
                else: flipper = self.flip
                service_rep = []

                for system in rs.get_distinct((action, message,)):
                    service_rep.append(system)

                system_list = ', '.join(service_rep)
                rep[action] += self.line_rep % (flipper, message, system_list)

        if rep[self.preventing]:
            report += self.subreport_wrap % (self.selinux_preventing_title, rep[self.preventing])
            logger.put(3, 'selinux report: self.preventing added')

        report = self.report_wrap % report
        return report


if __name__ == '__main__':
    from epylog.helpers import ModuleTest
    ModuleTest(selinux_mod, sys.argv)
