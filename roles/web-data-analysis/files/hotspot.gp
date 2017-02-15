set grid
set xdata time
set format x "%Y-%m-%d"
set timefmt "%Y-%m-%d"

set datafile separator ","
set term png size 1600,1200

##
set output "/var/www/html/csv-reports/images/hotspot-all.png"
set title "IPs grabbing hotspot per day"
plot ["2014-12-01":"2017-12-31"] \
     '/var/www/html/csv-reports/hotspot/hotspotdata-all.csv' using 1:2 title 'Average every 5min' with lines lw 4, \
     '/var/www/html/csv-reports/hotspot/hotspotdata-all.csv' using 1:3 title 'Least 5min' with lines lw 4, \
     '/var/www/html/csv-reports/hotspot/hotspotdata-all.csv' using 1:4 title 'Max 5min' with lines lw 4
unset output

##
set output "/var/www/html/csv-reports/images/hotspot-all-ma.png"
set title "Moving Average of IPs grabbing hotspot"
plot ["2014-12-01":"2017-12-31"] \
     '/var/www/html/csv-reports/hotspot/hotspotdatadata-all-7day-ma.csv' using 1:2 title 'Average every 5min' with lines lw 4, \
     '/var/www/html/csv-reports/hotspot/hotspotdatadata-all-7day-ma.csv' using 1:3 title 'Least 5min' with lines lw 4, \
     '/var/www/html/csv-reports/hotspot/hotspotdatadata-all-7day-ma.csv' using 1:4 title 'Max 5min' with lines lw 4
unset output
