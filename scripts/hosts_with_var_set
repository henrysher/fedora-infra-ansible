#!/usr/bin/python
# doteast; base from skvidal
# dump out the hosts with var=value

import ansible.inventory
import sys
from optparse import OptionParser


parser = OptionParser(version="1.0")
parser.add_option('-i', dest='inventory', default=None,
                  help="Path to inventory file/dir")
parser.add_option('-o', dest='variable', default=None,
                  help="variable name to check")

opts, args = parser.parse_args(sys.argv[1:])

if opts.inventory:
    inv = ansible.inventory.Inventory(host_list=opts.inventory)
else:
    inv = ansible.inventory.Inventory()

if opts.variable.find("=") == -1:
    print "Error -o requires var=value format argument"
    sys.exit(-1)

var_name, value = opts.variable.split('=')

if value == "":
   value="None"

var_set = []

for host in sorted(inv.get_hosts()):
    vars = inv.get_variables(host.name)
    if vars.has_key(var_name):
      if str(vars.get(var_name)).find(value) != -1:
        var_set.append(host.name)

print 'hosts with %s:' % var_name
for host in sorted(var_set):
    print host


