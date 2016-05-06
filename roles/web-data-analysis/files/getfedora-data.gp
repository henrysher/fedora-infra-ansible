set grid
set xdata time
set format x "%Y-%m-%d"
set timefmt "%Y-%m-%d"

set datafile separator ","
set term png size 1600,1200

##
set output "/var/www/html/csv-reports/images/getfedora-editions.png"
set title "Daily Editions Total Unique IPs"
plot ["2014-12-01":"2016-12-31"] \
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:2 title 'Total downloads' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:3 title 'Editions' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:4 title 'Atomic' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:5 title 'Cloud' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:6 title 'Server' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:7 title 'Workstation' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:8 title 'Unknown' with lines lw 4
unset output

##
set output "/var/www/html/csv-reports/images/getfedora-versions.png"
set title "Daily Editions Total Unique IPs"
plot ["2014-12-01":"2016-12-31"] \
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:2 title 'Total downloads' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:3 title 'Editions' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($4+$5+$6+$7+$8) title 'Atomic' with filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($5+$6+$7+$8) title 'Cloud' with filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($6+$7+$8) title 'Server' with filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($7+$8) title 'Workstation' with filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($8) title 'Unknown' with filledcurves x1
unset output

##
set output "/var/www/html/csv-reports/images/getfedora-versions-filled.png"
set title "Daily Version Totals"
plot ["2014-12-01":"2016-12-31"] \
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:2 title 'Total number' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($9+$10+$11+$12+$13+$14) title 'Fedora-20' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($10+$11+$12+$13+$14) title 'Fedora-21' with filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($11+$12+$13+$14) title 'Fedora-22' with filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($12+$13+$14) title 'Fedora-23' with filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:(13+$14) title 'Fedora-24' with filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($14) title 'Unknown' with  filledcurves x1
unset output

##
set output "/var/www/html/csv-reports/images/getfedora-arch.png"
set title "Daily Architectures Totals"
plot ["2014-12-01":"2016-12-31"] \
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:2 title 'Total number' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:15 title 'arm_32' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:16 title 'arm_64' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:17 title 'ppc_le' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:18 title 'ppc_he' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:19 title 's390x' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:20 title 'x86_32' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:21 title 'x86_64' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:22 title 'unknown' with lines lw 4
unset output

##
set output "/var/www/html/csv-reports/images/getfedora-arch-filled.png"
set title "Daily x86 Architectures Filled Totals"
plot ["2014-12-01":"2016-12-31"] \
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:2 title 'Total number' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($20+$21) title 'x86_32' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($21) title 'x86_64' with  filledcurves x1
unset output

##
set output "/var/www/html/csv-reports/images/getfedora-arch-less-filled.png"
set title "Daily Other Architectures Totals"
plot ["2014-01-01":"2016-12-31"] \
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($15+$16+$17+$18+$19+$22) title 'arm_32' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($16+$17+$18+$19+$22) title 'arm_64' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($17+$18+$19+$22) title 'ppc_le' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($18+$19+$22) title 'ppc_he' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($19+$22) title 's390x' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($22) title 'unknown' with  filledcurves x1
unset output

##
set output "/var/www/html/csv-reports/images/getfedora-netinstalls.png"
set title "Daily Netinstalls Total"
plot ["2014-01-01":"2016-12-31"] \
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:23 title 'Total Netinstalls' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:24 title 'Server' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:25 title 'Workstation' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:26 title 'Cloud' with lines lw 4
unset output

##
set output "/var/www/html/csv-reports/images/getfedora-netinstalls-filled.png"
set title "Daily Netinstalls Total"
plot ["2014-01-01":"2016-12-31"] \
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:23 title 'Total Netinstalls' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($24+$25+$26) title 'Server' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($25+$26) title 'Workstation' with filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($26) title 'Cloud' with  filledcurves x1
unset output

##
set output "/var/www/html/csv-reports/images/getfedora-spins.png"
set title "Daily Desktop Spins Total"
plot ["2014-01-01":"2016-12-31"] \
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:27 title 'Total Spins' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:28 title 'XFCE' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:30 title 'LXDE' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:33 title 'Mate' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:40 title 'Cinnamon' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:41 title 'KDE' with lines lw 4, \
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:29 title 'SoaS' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:31 title 'Security' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:32 title 'Robotics' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:34 title 'Scientific' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:35 title 'Jams' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:36 title 'Design' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:37 title 'Electronics' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:38 title 'Games' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:39 title 'Minimal' with lines lw 4
unset output

##
set output "/var/www/html/csv-reports/images/getfedora-spins-filled.png"
set title "Daily Desktop Spins Total"
plot ["2014-01-01":"2016-12-31"] \
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:27 title 'Total Spins' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($28+$30+$33+$40+$41+$29+$31+$32+$34+$35+$36+$37+$38+$39) title 'XFCE' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($30+$33+$40+$41+$29+$31+$32+$34+$35+$36+$37+$38+$39) title 'LXDE' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($33+$40+$41+$29+$31+$32+$34+$35+$36+$37+$38+$39) title 'Mate' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($40+$41+$29+$31+$32+$34+$35+$36+$37+$38+$39) title 'Cinnamon' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($41+$29+$31+$32+$34+$35+$36+$37+$38+$39) title 'KDE' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($29+$31+$32+$34+$35+$36+$37+$38+$39) title 'SoaS' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($31+$32+$34+$35+$36+$37+$38+$39) title 'Security' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($32+$34+$35+$36+$37+$38+$39) title 'Robotics' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($34+$35+$36+$37+$38+$39) title 'Scientific' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($35+$36+$37+$38+$39) title 'Jams' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($36+$37+$38+$39) title 'Design' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($37+$38+$39) title 'Electronics' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($38+$39) title 'Games' with  filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($39) title 'Minimal' with  filledcurves x1
unset output

##
set output "/var/www/html/csv-reports/images/getfedora-rough-filled.png"
set title "Daily Labs Stuff Total"
plot ["2014-01-01":"2016-12-31"] \
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:2 title 'Total downloads' with lines lw 4,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($3+27) title 'Editions' with filledcurves x1,\
     '/var/www/html/csv-reports/getfedora/getfedoradata-all.csv' using 1:($27) title 'Total Spins' with filledcurves x1
unset output
