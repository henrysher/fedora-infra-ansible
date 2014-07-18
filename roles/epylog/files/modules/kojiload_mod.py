#!/usr/bin/python -tt
"""
Rsyncd log parsing module for Epylog
"""

##
# Copyright (C) 2012 by Red Hat, Inc
# Written by Seth Vidal <skvidal at fedoraproject.org>
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

class kojiload_mod(InternalModule):
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
        #kojiload: Load: 7.1 Total: 192.0 Use: 3.7% (Very Light Load)
        self.regex_map = {
            rc('kojiload: Load:.*'): self.load_results
        }
        # dict to store all of our data
        self.loads = [] # list of kojiload percentages
        self.kojiloads = rc('kojiload: Load: (.*) Total: (.*) Use: (.*)\%.*')


    def load_results(self, linemap):
        (sys, msg, multi) = self.get_smm(linemap)
        load, total, use_percent = self.kojiloads.search(msg).groups()
        for i in range(multi):
            self.loads.append(float(use_percent))
        return {(load,total): 1}
        
        
    def finalize(self, resultset):
        ##
        # A resultset is a dictionary of all values returned by your
        # handler functions -- except they are unique and show how many
        # times each tuple occurs.
        # See epylog.Result for some convenience methods to use when
        # processing and analyzing the results.
        #
        if not self.loads:
            return "No kojiloads returned, that seems odd."
        
        max_load = max(self.loads)
        min_load = min(self.loads)
        avg_load = sum(self.loads)/len(self.loads)
        
        foo = "Max: %s%%<br>\nMin: %s%%<br>\nAvg: %.1f%%<br>\n" %  (max_load, 
                                        min_load, avg_load)
        return foo
         
##
# This is useful when testing your module out.
# Invoke without command-line parameters to learn about the proper
# invocation.
#
if __name__ == '__main__':
    from epylog.helpers import ModuleTest
    ModuleTest(kojiload_mod, sys.argv)
