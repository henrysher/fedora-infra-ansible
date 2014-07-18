#!/usr/bin/python -tt
"""
This module should run after all other modules.

Takes the remaining logs, saves them out to a tmpfile.
Uses difflib.SequenceMatcher() to return logs which occur most often and are
at least a set percentage similar. This lets you catch logs which are
from multiple machines and more or less the same or similar logs (with memory
or process id offsets) from the same machine.

"""

import sys
import re
import difflib
from operator import itemgetter
import tempfile
import os
import shutil

##
# This is for testing purposes, so you can invoke this from the
# modules directory. See also the testing notes at the end of the
# file.
#
sys.path.insert(0, '../py/')
from epylog import Result, InternalModule

class common_unparsed_mod(InternalModule):
    def __init__(self, opts, logger):
        InternalModule.__init__(self)
        self.logger = logger
        rc = re.compile

        self.match_percentage = int(opts.get('match_percentage', '95'))
        self.debug_dump = int(opts.get('debug_dump', '1'))
        self.regex_map = {rc('^.+$'):self.expand_out_line}
        self.tmpdir = tempfile.mkdtemp(prefix='epylog-common-unparsed', dir='/var/tmp')
        self.matchfile = self.tmpdir + '/match_limited'
        self.matchfile_f = open(self.matchfile, 'w')
        self.complete = self.tmpdir + '/complete'
        self.complete_f = open(self.complete, 'w')
        

    ##
    # Line-matching routines
    #
    def expand_out_line(self, linemap):
        sys, msg, mult = self.get_smm(linemap)
        matchout = '%s\n' % (msg)
        com_out = '%s' % (linemap['line'])
        for i in range(0, int(mult)):
            self.complete_f.write(com_out)
        self.matchfile_f.write(matchout)

        #dirty like zebra
        if not os.path.exists(self.tmpdir + '/returned'):
            open(self.tmpdir + '/returned', 'w').close()
            return {'match':0}
        else:
            return None


    def finalize(self, rs):
        #FIXME - enable a debug mode where it writes
        # out to a file all of the first line and things which match it
        # and percentages of match for later investigation
        self.complete_f.close()
        self.matchfile_f.close()
        matches = {}
        full_matches = {}
        lines_matched = set()
        where = 0
        rl = open(self.matchfile, 'r')
        for l in rl:
            where += 1
            sub_where = 0
            for ol in open(self.matchfile, 'r'):
                sub_where += 1
                if sub_where < where: # if we're before it in the file we've already matched it
                    continue
                if sub_where in lines_matched:
                    continue

                c = difflib.SequenceMatcher(isjunk=lambda x: x in ('1','2','3','4','5','6','7','8','9','0'),a=l, b=ol)
                rq_ratio = int(c.real_quick_ratio()*100) # do the fast upper bound - find out if we should even glance at it.
                if rq_ratio < 60:
                    continue
                ratio = int(c.ratio()*100)
                if ratio >= self.match_percentage:
                    lines_matched.add(sub_where)
                    if l not in matches:
                        matches[l] = 0
                        full_matches[l] = []
                    matches[l] += 1
                    full_matches[l].append((ol,ratio))
        if self.debug_dump:
            fm_db = open(self.tmpdir + '/debug-match', 'w')
            for k in full_matches:
                fm_db.write(k)
                for (v,r) in full_matches[k]:
                    fm_db.write('  %s %s' % (r, v))
            fm_db.close()
            
        res = "<table border=0><tr><th>Count</th><th align=left>Log</th></tr>\n\n"
        for (k,v) in sorted(matches.items(), key=itemgetter(1), reverse=True)[:20]: # take the top 20 most common provided there are more than 1
            if v > 1:
                res += "<tr>\n<td bgcolor='#DDDDDD'>%s</td><td>%s</td>\n</tr>" % (v, k)
        res += "<tr>\n<td colspan=2>\n<h2>Complete messages</h2>\n<pre>\n"
        res += ''.join(sorted(open(self.complete, 'r').readlines()))
        res += "</pre>\n</td>\n</tr>\n</table>"
        return res



if __name__ == '__main__':
    from epylog.helpers import ModuleTest
    ModuleTest(common_unparsed_mod, sys.argv)
