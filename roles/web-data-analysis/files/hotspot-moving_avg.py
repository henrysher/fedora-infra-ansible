#!/usr/bin/python

# This file is part of Fedora Project Infrastructure Ansible
# Repository.
#
# Fedora Project Infrastructure Ansible Repository is free software:
# you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later
# version.
#
# Fedora Project Infrastructure Ansible Repository is distributed in
# the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with Fedora Project Infrastructure Ansible Repository.  If
# not, see <http://www.gnu.org/licenses/>.

# This is a complete horrible hack to get something done. Patches are
# really welcome.

import pandas
#import matplotlib.pyplot as plt
import math

rolling = 7

tree = {}

df = pandas.read_csv("/var/www/html/csv-reports/hotspot/hotspotdata-all.csv")

dates = df['1970-01-01']
AVG   = pandas.rolling_mean(df['AVG'],rolling)
LEAST = pandas.rolling_mean(df['LEAST'],rolling)
MAX   = pandas.rolling_mean(df['MAX'],rolling)


for i in xrange(0,len(dates)):
    if math.isnan(MAX[i]):
        csv_line = ",".join([dates[i],"0","0"])
    else:
        csv_line = ",".join([dates[i],
                             str(int(AVG[i])),
                             str(int(LEAST[i])),
                             str(int(MAX[i])),
                         ])
    print csv_line
