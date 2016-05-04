# Moving Average

import pandas
import matplotlib.pyplot as plt
import math

rolling = 7

tree = {}

df = pandas.read_csv("data-all.csv")

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
rawhide = pandas.rolling_mean(df['28-rawhide'], rolling)
unk_rel = pandas.rolling_mean(df['29-unk_rel'], rolling)
EPEL  = pandas.rolling_mean(df['30-epel'], rolling)
Fedora = pandas.rolling_mean(df['31-fedora'], rolling)
alpha = pandas.rolling_mean(df['32-alpha'], rolling)
ARM = pandas.rolling_mean(df['33-arm'], rolling)
ARM64 = pandas.rolling_mean(df['34-arm64'], rolling)
ia64 = pandas.rolling_mean(df['35-ia64'], rolling)
mips = pandas.rolling_mean(df['36-mips'], rolling)
ppc = pandas.rolling_mean(df['37-ppc'], rolling)
s390 = pandas.rolling_mean(df['38-s390'], rolling)
sparc = pandas.rolling_mean(df['39-sparc'], rolling)
tilegx = pandas.rolling_mean(df['40-tilegx'], rolling)
x86_32 = pandas.rolling_mean(df['41-x86_32'], rolling)
x86_64 = pandas.rolling_mean(df['42-x86_64'], rolling)
x86_32_e = pandas.rolling_mean(df['43-x86_32_e'], rolling)
x86_32_f = pandas.rolling_mean(df['44-x86_32_f'], rolling)
x86_64_e = pandas.rolling_mean(df['45-x86_64_e'], rolling)
x86_64_f = pandas.rolling_mean(df['46-x86_64_f'], rolling)
ppc_e = pandas.rolling_mean(df['47-ppc_e'], rolling)
ppc_f = pandas.rolling_mean(df['48-ppc_f'], rolling)
unk_arc = pandas.rolling_mean(df['49-unk_arc'], rolling)
centos =  pandas.rolling_mean(df['50-centos'], rolling)
rhel =  pandas.rolling_mean(df['51-rhel'], rolling)

for i in xrange(0,len(dates)):
    if math.isnan(epel4[i]):
        csv_line = ",".join([dates[i],"0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0","0"])
    else:
        csv_line = ",".join([dates[i],str(int(epel4[i])),str(int(epel5[i])),str(int(epel6[i])),str(int(epel7[i])),str(int(fed03[i])),str(int(fed04[i])),str(int(fed05[i])),str(int(fed06[i])),str(int(fed07[i])),str(int(fed08[i])),str(int(fed09[i])),str(int(fed10[i])),str(int(fed11[i])),str(int(fed12[i])),str(int(fed13[i])),str(int(fed14[i])),str(int(fed15[i])),str(int(fed16[i])),str(int(fed17[i])),str(int(fed18[i])),str(int(fed19[i])),str(int(fed20[i])),str(int(fed21[i])),str(int(fed22[i])),str(int(fed23[i])),str(int(fed24[i])),str(int(rawhide[i])),str(int(unk_rel[i])),str(int(EPEL[i])),str(int(Fedora[i])),str(int(alpha[i])),str(int(ARM[i])),str(int(ARM64[i])),str(int(ia64[i])),str(int(mips[i])),str(int(ppc[i])),str(int(s390[i])),str(int(sparc[i])),str(int(tilegx[i])),str(int(x86_32[i])),str(int(x86_64[i])), str(int(x86_32_e[i])),str(int(x86_32_f[i])),str(int(x86_64_e[i])),str(int(x86_64_f[i])),str(int(ppc_e[i])),str(int(ppc_f[i])), str(int(unk_arc[i])),str(int(centos[i])),str(int(rhel[i]))])
    print csv_line
