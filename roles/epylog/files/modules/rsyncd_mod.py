#!/usr/bin/python -tt
"""
Rsyncd log parsing module for Epylog
"""

##
# Copyright (C) 2003 by Duke University
# Written by Seth Vidal <skvidal at phy.duke.edu>
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


import sys
import re

##
# This is for testing purposes, so you can invoke this from the
# modules directory. See also the testing notes at the end of the
# file.
#
sys.path.insert(0, '../py/')
from epylog import Result, InternalModule

class rsyncd_mod(InternalModule):
    ##
    # opts: is a map with extra options set in
    #       [conf] section of the module config, or on the
    #       command line using -o flag to the module.
    # logger: A logging object. API:
    #         logger.put(loglvl, 'Message')
    #         Only critical stuff needs to go onto lvl 0.
    #         Common output goes to lvl 1.
    #         Others are debug levels.
    #
    def __init__(self, opts, logger):
        ##
        # Do a "super-init" so the class we are subclassing gets
        # instantiated.
        #
        InternalModule.__init__(self)
        self.logger = logger
        ##
        # Convenience
        #
        rc = re.compile

        self.regex_map = {
            rc('rsyncd\[\d+\]: rsync on'): self.rsync_hosts,
            rc('rsyncd\[\d+\]: (?:sent|wrote)\s\S*\sbytes'): self.rsync_results
        }
        self.topcount = int(opts.get('report_top', 5)) #get report_top, default to 5 if not set
        ig_s = opts.get('ignore_hosts', '')
        ig_s.replace(',',' ')
        self.ignore_hosts = ig_s.split(' ')
        # dict to store all of our data
        self.rsync_pid_bytes = {}
        self.rsync_pid_host = {}
        self.rsync_host_loc = rc('rsyncd\[(\d+)\]: rsync\son\s(\S*)\sfrom\s.*\((\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\)')
        self.rsync_bytes = rc('rsyncd\[(\d+)\]: (?:sent|wrote)\s(\d+) bytes  (?:read|received)\s(\d+) bytes  total size (\d+)')

    def rsync_hosts(self, linemap):
        (sys, msg, multi) = self.get_smm(linemap)
        pid, loc, ip = self.rsync_host_loc.search(msg).groups()
        host = self.gethost(ip)
        if host not in self.ignore_hosts:
            self.rsync_pid_host[pid] = (host, loc)
        return {(loc, host): 1}

    def rsync_results(self, linemap):
        (sys, msg, multi) = self.get_smm(linemap)
        pid, wbytes, rbytes, tbytes = self.rsync_bytes.search(msg).groups()
        self.rsync_pid_bytes[pid] = (wbytes, rbytes, tbytes)
        return {(pid, wbytes): 1}

    def _uniq(self, s):
        """Return a list of the elements in s, but without duplicates.
    
        For example, unique([1,2,3,1,2,3]) is some permutation of [1,2,3],
        unique("abcabc") some permutation of ["a", "b", "c"], and
        unique(([1, 2], [2, 3], [1, 2])) some permutation of
        [[2, 3], [1, 2]].
    
        For best speed, all sequence elements should be hashable.  Then
        unique() will usually work in linear time.
    
        If not possible, the sequence elements should enjoy a total
        ordering, and if list(s).sort() doesn't raise TypeError it's
        assumed that they do enjoy a total ordering.  Then unique() will
        usually work in O(N*log2(N)) time.
    
        If that's not possible either, the sequence elements must support
        equality-testing.  Then unique() will usually work in quadratic
        time.
        """
    
        n = len(s)
        if n == 0:
            return []
    
        # Try using a dict first, as that's the fastest and will usually
        # work.  If it doesn't work, it will usually fail quickly, so it
        # usually doesn't cost much to *try* it.  It requires that all the
        # sequence elements be hashable, and support equality comparison.
        u = {}
        try:
            for x in s:
                u[x] = 1
        except TypeError:
            del u  # move on to the next method
        else:
            return u.keys()
    
        # We can't hash all the elements.  Second fastest is to sort,
        # which brings the equal elements together; then duplicates are
        # easy to weed out in a single pass.
        # NOTE:  Python's list.sort() was designed to be efficient in the
        # presence of many duplicate elements.  This isn't true of all
        # sort functions in all languages or libraries, so this approach
        # is more effective in Python than it may be elsewhere.
        try:
            t = list(s)
            t.sort()
        except TypeError:
            del t  # move on to the next method
        else:
            assert n > 0
            last = t[0]
            lasti = i = 1
            while i < n:
                if t[i] != last:
                    t[lasti] = last = t[i]
                    lasti += 1
                i += 1
            return t[:lasti]
    
        # Brute force is all that's left.
        u = []
        for x in s:
            if x not in u:
                u.append(x)
        return u
        
    def _sortByVal(self, dict, reverse=0):
        if type(dict) is not type({}): return []
        keys = dict.keys()
        s = map(lambda k: (dict[k], k), keys)
        s.sort()
        if reverse: s.reverse()
        return s
        
    def finalize(self, resultset):
        ##
        # A resultset is a dictionary of all values returned by your
        # handler functions -- except they are unique and show how many
        # times each tuple occurs.
        # See epylog.Result for some convenience methods to use when
        # processing and analyzing the results.
        #
        
        hostloc = {} # key = host, val = [loc, loc, loc]
        hosttotal = {} # key = host val = totalwbytes
        
        foo = "<table border=0>\n\t<tr>\n"
        
        for pid in self.rsync_pid_host.keys():
            (host, loc) = self.rsync_pid_host[pid]
            if self.rsync_pid_bytes.has_key(pid):
                if not hostloc.has_key(host):
                    hostloc[host] = []
                if not hosttotal.has_key(host):
                    hosttotal[host] = 0L
                hostloc[host].append(loc)
                bytes = long(self.rsync_pid_bytes[pid][0])
                hosttotal[host] += bytes
        
        for host in hostloc.keys():
            hostloc[host] = self._uniq(hostloc[host])
        
        hosts = self._sortByVal(hosttotal, 1)
        count = 0L
        for (tot,host) in hosts[:self.topcount]:
            if count % 2:
                bgcolor = "#dddddd"
            else:
                bgcolor = "#ffffff"
            count+=1
            line = '\t\t<td bgcolor=%s valign=\"top\">%s</td>\n' % (bgcolor, host)
            line = line + '\t\t<td bgcolor=%s valign="top">\n' % bgcolor
            for loc in hostloc[host]:
                line = line + '\t\t\t%s<br>\n' % loc
            line = line + '\t\t</td>\n'
            size, marker = self.mk_size_unit(hosttotal[host])
            line = line + '\t\t<td bgcolor=%s valign="top">%s%s</td>\n' % (bgcolor, size, marker)
            line = line + '\t</tr>\n'
            foo = foo + line
        foo = foo + '</table>\n'
        return foo

##
# This is useful when testing your module out.
# Invoke without command-line parameters to learn about the proper
# invocation.
#
if __name__ == '__main__':
    from epylog.helpers import ModuleTest
    ModuleTest(rsyncd_mod, sys.argv)
