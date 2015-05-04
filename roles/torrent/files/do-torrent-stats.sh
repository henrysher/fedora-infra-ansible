#!/bin/bash

statscmd=/usr/local/bin/torrent-data.py
btdata=/srv/torrent/data/bttrack.dat
outputdir=/srv/web/stats/
hourlydir=$outputdir/hourly
dailydir=$outputdir/daily
latestlink=$outputdir/current-stats.json

if ! [ -f $btdata ]; then
   echo "cannot find $btdata"
   exit 1
fi

if ! [ -d $outputdir ]; then
    mkdir -p $outputdir
fi

if ! [ -d $hourlydir ]; then
    mkdir -p $hourlydir
fi

if ! [ -d $dailydir ]; then
    mkdir -p $dailydir
fi


if ! [ -f $statscmd ]; then
   echo "Cannot find stats generating command $statscmd"
   exit 1
fi

now=`date +%Y-%m-%d-%H:%M`
today=`date +%Y-%m-%d`
outputfile="$hourlydir/torrent-stats-$now.json"
dataloc=`mktemp`

\cp -f $btdata $dataloc

$statscmd $dataloc $outputfile
rm -f $dataloc

rm -f $latestlink
ln -s $outputfile $latestlink

if [ ! -f "$dailydir/torrent-stats-$today.json" ]; then
    \cp -f $outputfile $dailydir/torrent-stats-$today.json
fi

/usr/sbin/tmpwatch -f 720 $hourlydir
    
