#!/bin/bash

# This copyrighted material is made available to anyone wishing to use, modify,
# copy, or redistribute it subject to the terms and conditions of the GNU
# General Public License v.2.  This program is distributed in the hope that it
# will be useful, but WITHOUT ANY WARRANTY expressed or implied, including the
# implied warranties of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.  You should have
# received a copy of the GNU General Public License along with this program;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street,
# Fifth Floor, Boston, MA 02110-1301, USA.

rm -f /root/GeoIPCountryCSV.zip

wget -q -T 5 -t 1 http://geolite.maxmind.com/download/geoip/database/GeoIPCountryCSV.zip
unzip -q GeoIPCountryCSV.zip || exit 1

awk -F \" '{print $10","$6","$8}' GeoIPCountryWhois.csv > cbe.csv
rm -f GeoIPCountryWhois.csv

(for c in $(awk -F , '{print $1}' cbe.csv | sort -u)
do
  echo "acl \"$c\" {"
  grep "^$c," cbe.csv | awk -F , 'function s(b,e,l,m,n) {l = int(log(e-b+1)/log(2)); m = 2^32-2^l; n = and(m,e); if (n == and(m,b)) printf "\t%u.%u.%u.%u/%u;\n",b/2^24%256,b/2^16%256,b/2^8%256,b%256,32-l; else {s(b,n-1); s(n,e)}} s($2,$3)'
  echo -e "};\n"
done) > /var/named/GeoIP.acl

rm -f cbe.csv

exit 0

