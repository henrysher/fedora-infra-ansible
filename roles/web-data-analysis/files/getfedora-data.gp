set grid
set xdata time
set format x "%Y-%m-%d"
set timefmt "%Y-%m-%d"

set datafile separator ","
set term png size 1600,1200

##
set output "/var/www/html/csv-reports/images/getfedora-editions.png"
set title "Daily Editions Total"
plot ["2014-12-03":"2016-01-18"] \
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:2 title 'Total number' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:3 title 'Atomic' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:4 title 'Cloud' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:5 title 'Server' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:6 title 'Workstation' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:26 title 'Netinstall' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:7 title 'Unknown' with lines lw 4
unset output

##
set output "/var/www/html/csv-reports/images/getfedora-versions.png"
set title "Daily Version Totals"
plot ["2015-01-01":"2015-12-31"] \
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:2 title 'Total number' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:8 title 'Fedora-21' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:9 title 'Fedora-22' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:10 title 'Fedora-23' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:11 title 'Fedora-24' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:12 title 'Fedora-25' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:13 title 'Fedora-26' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:14 title 'Fedora-27' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:15 title 'Fedora-28' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:16 title 'Fedora-29' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:17 title 'Unknown' with lines lw 4
unset output

##
set output "/var/www/html/csv-reports/images/getfedora-arch.png"
set title "Daily Architectures Totals"
plot ["2015-01-01":"2015-12-31"] \
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:2 title 'Total number' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:18 title 'arm_32' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:19 title 'arm_64' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:20 title 'ppc_le' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:21 title 'ppc_he' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:22 title 's390x' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:23 title 'x86_32' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:24 title 'x86_64' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedora-all.csv' using 1:25 title 'unknown' with lines lw 4
unset output

