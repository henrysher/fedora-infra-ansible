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

df = pandas.read_csv("/var/www/html/csv-reports/mirrors/mirrorsdata-all.csv")

dates = df['1970-01-01']
epel4 = pandas.rolling_mean(df['02-epel4'],rolling)
epel5 = pandas.rolling_mean(df['03-epel5'],rolling)
epel6 = pandas.rolling_mean(df['04-epel6'],rolling)
epel7 = pandas.rolling_mean(df['05-epel7'],rolling)
fed03 = pandas.rolling_mean(df['06-f03'], rolling)
fed04 = pandas.rolling_mean(df['07-f04'], rolling)
fed05 = pandas.rolling_mean(df['08-f05'], rolling)
fed06 = pandas.rolling_mean(df['09-f06'], rolling)
fed07 = pandas.rolling_mean(df['10-f07'], rolling)
fed08 = pandas.rolling_mean(df['11-f08'], rolling)
fed09 = pandas.rolling_mean(df['12-f09'], rolling)
fed10 = pandas.rolling_mean(df['13-f10'], rolling)
fed11 = pandas.rolling_mean(df['14-f11'], rolling)
fed12 = pandas.rolling_mean(df['15-f12'], rolling)
fed13 = pandas.rolling_mean(df['16-f13'], rolling)
fed14 = pandas.rolling_mean(df['17-f14'], rolling)
fed15 = pandas.rolling_mean(df['18-f15'], rolling)
fed16 = pandas.rolling_mean(df['19-f16'], rolling)
fed17 = pandas.rolling_mean(df['20-f17'], rolling)
fed18 = pandas.rolling_mean(df['21-f18'], rolling)
fed19 = pandas.rolling_mean(df['22-f19'], rolling)
fed20 = pandas.rolling_mean(df['23-f20'], rolling)
fed21 = pandas.rolling_mean(df['24-f21'], rolling)
fed22 = pandas.rolling_mean(df['25-f22'], rolling)
fed23 = pandas.rolling_mean(df['26-f23'], rolling)
fed24 = pandas.rolling_mean(df['27-f24'], rolling)
fed25 = pandas.rolling_mean(df['28-f25'], rolling)
fed26 = pandas.rolling_mean(df['29-f26'], rolling)
fed27 = pandas.rolling_mean(df['30-f27'], rolling)
fed28 = pandas.rolling_mean(df['31-f28'], rolling)
fed29 = pandas.rolling_mean(df['32-f29'], rolling)
rawhide = pandas.rolling_mean(df['33-rawhide'], rolling)
unk_rel = pandas.rolling_mean(df['34-unk_rel'], rolling)
EPEL  = pandas.rolling_mean(df['35-epel'], rolling)
Fedora = pandas.rolling_mean(df['36-fedora'], rolling)
alpha = pandas.rolling_mean(df['37-alpha'], rolling)
ARM = pandas.rolling_mean(df['38-arm'], rolling)
ARM64 = pandas.rolling_mean(df['39-arm64'], rolling)
ia64 = pandas.rolling_mean(df['40-ia64'], rolling)
mips = pandas.rolling_mean(df['41-mips'], rolling)
ppc = pandas.rolling_mean(df['42-ppc'], rolling)
s390 = pandas.rolling_mean(df['43-s390'], rolling)
sparc = pandas.rolling_mean(df['44-sparc'], rolling)
tilegx = pandas.rolling_mean(df['45-tilegx'], rolling)
x86_32 = pandas.rolling_mean(df['46-x86_32'], rolling)
x86_64 = pandas.rolling_mean(df['47-x86_64'], rolling)
x86_32_e = pandas.rolling_mean(df['48-x86_32_e'], rolling)
x86_32_f = pandas.rolling_mean(df['49-x86_32_f'], rolling)
x86_64_e = pandas.rolling_mean(df['50-x86_64_e'], rolling)
x86_64_f = pandas.rolling_mean(df['51-x86_64_f'], rolling)
ppc_e = pandas.rolling_mean(df['52-ppc_e'], rolling)
ppc_f = pandas.rolling_mean(df['53-ppc_f'], rolling)
unk_arc = pandas.rolling_mean(df['54-unk_arc'], rolling)
centos =  pandas.rolling_mean(df['55-centos'], rolling)
rhel =  pandas.rolling_mean(df['56-rhel'], rolling)
ppc64 = pandas.rolling_mean(df['57-ppc64'], rolling)
ppc64le = pandas.rolling_mean(df['58-ppc64le'], rolling)
modular = pandas.rolling_mean(df['59-modular'], rolling)
modular_rawhide = pandas.rolling_mean(df['60-modular_rawhide'], rolling)
modular_f27 = pandas.rolling_mean(df['61-modular_f27'], rolling)
modular_f28 = pandas.rolling_mean(df['62-modular_f28'], rolling)
modular_f29 = pandas.rolling_mean(df['63-modular_f29'], rolling)
modular_f30 = pandas.rolling_mean(df['64-modular_f30'], rolling)

print "1970-01-01,,02-epel4,03-epel5,04-epel6,05-epel7,06-f03,07-f04,08-f05,09-f06,10-f07,11-f08,12-f09,13-f10,14-f11,15-f12,16-f13,17-f14,18-f15,19-f16,20-f17,21-f18,22-f19,23-f20,24-f21,25-f22,26-f23,27-f24,28-f25,29-f26,30-f27,31-f28,32-f29,33-rawhide,34-unk_rel,35-epel,36-fedora,37-alpha,38-arm,39-arm64,40-ia64,41-mips,42-ppc,43-s390,44-sparc,45-tilegx,46-x86_32,47-x86_64,48-x86_32_e,49-x86_32_f,50-x86_64_e,51-x86_64_f,52-ppc_e,53-ppc_f,54-unk_arc,55-centos,56-rhel,57-ppc64,58-ppc64le,59-modular,60-modular_rawhide,61-modular_f27,62-modular_f28,63-modular_f29,64-modular_f30";

for i in xrange(0,len(dates)):
    if math.isnan(epel4[i]):
        csv_line = ",".join([dates[i],"0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"])
    else:
        csv_line = ",".join([dates[i],str(int(epel4[i])),str(int(epel5[i])),str(int(epel6[i])),str(int(epel7[i])),str(int(fed03[i])),str(int(fed04[i])),str(int(fed05[i])),str(int(fed06[i])),str(int(fed07[i])),str(int(fed08[i])),str(int(fed09[i])),str(int(fed10[i])),str(int(fed11[i])),str(int(fed12[i])),str(int(fed13[i])),str(int(fed14[i])),str(int(fed15[i])),str(int(fed16[i])),str(int(fed17[i])),str(int(fed18[i])),str(int(fed19[i])),str(int(fed20[i])),str(int(fed21[i])),str(int(fed22[i])),str(int(fed23[i])),str(int(fed24[i])),str(int(fed25[i])),str(int(fed26[i])),str(int(fed27[i])),str(int(fed28[i])),str(int(fed29[i])),str(int(rawhide[i])),str(int(unk_rel[i])),str(int(EPEL[i])),str(int(Fedora[i])),str(int(alpha[i])),str(int(ARM[i])),str(int(ARM64[i])),str(int(ia64[i])),str(int(mips[i])),str(int(ppc[i])),str(int(s390[i])),str(int(sparc[i])),str(int(tilegx[i])),str(int(x86_32[i])),str(int(x86_64[i])), str(int(x86_32_e[i])),str(int(x86_32_f[i])),str(int(x86_64_e[i])),str(int(x86_64_f[i])),str(int(ppc_e[i])),str(int(ppc_f[i])), str(int(unk_arc[i])),str(int(centos[i])),str(int(rhel[i])),str(int(ppc64[i])),str(int(ppc64le[i])),str(int(modular[i])),str(int(modular_rawhide[i])),str(int(modular_f27[i])),str(int(modular_f28[i])),str(int(modular_f29[i])),str(int(modular_f30[i]))])
    print csv_line
