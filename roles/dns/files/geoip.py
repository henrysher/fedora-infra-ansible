#!/usr/bin/env python
# (c) 2019 Red Hat, Inc.
# Rick Elrod <relrod@redhat.com>
# etc.

import csv
import sys

if len(sys.argv) != 4:
    print "Usage: geoip-to-acl.py <GeoLite2-Country-Blocks-IPv4.csv> "\
          "<GeoLite2-Country-Blocks-IPv6.csv> "\
          "<GeoLite2-Country-Locations-en.csv>"
    sys.exit(1)

v4blocks = sys.argv[1]
v6blocks = sys.argv[2]
locations = sys.argv[3]

location_map = {}
subnet_map = {}

with open(locations) as loc_in:
    reader = csv.reader(loc_in)
    # Skip the header line
    reader.next()
    for row in reader:
        # If we have a narrowed down country, use it.
        # Otherwise, use the continent.
        if row[4] == '':
            location_map[int(row[0])] = row[2]
        else:
            location_map[int(row[0])] = row[4]

# Handle v4
with open(v4blocks) as v4_in:
    reader = csv.reader(v4_in)
    # Skip the header line
    reader.next()
    for row in reader:
        # Figure out if we need to use row[1] or row[2]
        if row[1] == '' and row[2] == '':
            # If the subnet has no country attached to it at all (??), skip it.
            continue
        elif row[2] == '':
            geo_code = location_map[int(row[1])]
        else:
            geo_code = location_map[int(row[2])]

        if subnet_map.get(geo_code):
            subnet_map[geo_code].append(row[0])
        else:
            subnet_map[geo_code] = [row[0]]

# Handle v6
with open(v6blocks) as v6_in:
    reader = csv.reader(v6_in)
    # Skip the header line
    reader.next()
    for row in reader:
        # Figure out if we need to use row[1] or row[2]
        if row[1] == '' and row[2] == '':
            # If the subnet has no country attached to it at all (??), skip it.
            continue
        elif row[2] == '':
            geo_code = location_map[int(row[1])]
        else:
            geo_code = location_map[int(row[2])]

        if subnet_map.get(geo_code):
            subnet_map[geo_code].append(row[0])
        else:
            subnet_map[geo_code] = [row[0]]

# And generate the ACLs
for k,v in sorted(subnet_map.iteritems()):
    print 'acl "%s" {' % k
    for subnet in v:
        print '\t%s;' % subnet
    print '};'
    print ''
