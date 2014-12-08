#!/usr/bin/python
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# Copyright 2008 (c) Red Hat, Inc - written by Seth Vidal <skvidal@fedoraproject.org>

from ConfigParser import ConfigParser, ParsingError
import os
import os.path
import sys
import pwd
import time

class Config(object):
    def __init__(self, fn='/etc/planetbuilder.conf'):
        """read in our config data"""
        self.ignore_users = []
        self.banned_stanzas = ['Planet', 'main', 'DEFAULT']
        self.base_config = None
        self.group = None
        self.output = sys.stdout
        self.output_fn = None
        
        cp = ConfigParser()
        cp.read(fn)
        if cp.has_section('main'):
            if cp.has_option('main', 'base_config'):
                self.base_config = cp.get('main', 'base_config')
            if cp.has_option('main', 'group'):
                self.group = cp.get('main', 'group')
                
            if cp.has_option('main', 'ignore_users'):
                iu = cp.get('main', 'ignore_users')
                iu = iu.replace(',',' ')    
                for user in iu.split(' '):
                    self.ignore_users.append(user)
            if cp.has_option('main', 'banned_stanzas'):
                bs = cp.get('main', 'banned_stanzas')
                bs = bs.replace(',',' ')    
                for banned in bs.split(' '):
                    self.banned_stanzas.append(banned)
            if cp.has_option('main', 'output'):
                of = cp.get('main', 'output')
                self.output = open(of, 'w')
                self.output_fn = of
                
def error_print(msg):
    print >> sys.stderr, msg
    
class PlanetBuilderException(Exception):
    def __init__(self, value=None):
        Exception.__init__(self)
        self.value = value

    def __str__(self):
        return "%s" %(self.value,)


class PlanetBuilder(object):
    def __init__(self, config_file):
        self.entries = {}
        self.conf = Config(config_file)
        
    def add(self, entry):
        if not entry.feed or not entry.name:
            raise PlanetBuilderException, "entry %s lacks feed or name" % entry

        if entry.feed in self.conf.banned_stanzas:
            raise PlanetBuilderException, "entry %s is in banned list" % entry
        
        if self.entries.has_key(entry.feed):
            raise PlanetBuilderException, "entry %s already exists in list" % entry

        self.entries[entry.feed] = entry

    def compile(self):
        result = "#planet config compiled on %s\n" % time.ctime()
        result += "#using group %s and config %s\n" % (self.conf.group, self.conf.base_config)
        if self.conf.base_config:
            bc = open(self.conf.base_config, 'r').read()
            result += bc
        
        for e in self.entries.values():
            e_format = "# Origin: %s\n" % (e.origin)
            e_format += "[%s]\nname=%s\n" % (e.feed, e.name)
            if e.face:
                e_format += "face=%s\n" % (e.face)
            if e.username:
                e_format += "fasname=%s\n" % (e.username)
            result += e_format
            result += "\n"

        self.result = result

    def produce_output(self):
        self.conf.output.write(self.result)        
        self.conf.output.close()
                    
class PlanetEntry(object):

    def __init__(self, origin, feed=None, name=None, face=None, username=None):
        self.origin = origin
        self.feed = feed
        self.name = name
        self.username = username
        if not name:
            self.name = origin
        self.face = face

    def __str__(self):
        return '%s:%s' % (self.origin, self.feed)

class PlanetFile(object):
    def __init__(self, filename, username):
        self.entries = []
        # open up with cp
        cp = ConfigParser()
        try:
            cp.read(filename)
        except ParsingError, e:
            error_print("Problem parsing %s - %s" % (filename, str(e)))
            return
            
        for s in cp.sections():
            name = face = None
            if cp.has_option(s, 'name'):
                name = cp.get(s, 'name')
            if cp.has_option(s, 'face'):
                face = cp.get(s, 'face')
            e = PlanetEntry(filename, feed=s, name=name, face=face, username=username)
            self.entries.append(e)
    
    def __iter__(self):
        return self.entries.__iter__()
    
def main(config_file='/etc/planetbuilder.conf'):
    pb = PlanetBuilder(config_file)

    fn = '.planet'
    if pb.conf.group:
        fn = '.planet.%s' % pb.conf.group
        
    for (n, p, u, g, c, h, s) in pwd.getpwall():
        if u < 500:
            continue
        if n in pb.conf.ignore_users:
            continue
        
        if os.path.exists(h + '/' + fn):
            for entry in PlanetFile(h + '/' + fn, n):
                pb.add(entry)

    pb.compile()
    pb.produce_output()
    print pb.conf.output_fn


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
        
        
    
    
