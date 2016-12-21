#!/bin/bash
# fetch data files from the opentracker stats output
# store them away for later analysis
# skvidal 
base=/srv/web/stats/raw
baseurl='http://torrent.fedoraproject.org:6969/stats?mode='
date=`date +%Y-%m-%d`
hour=`date +%H`
wgetcmd="wget --timeout=20 -q -4"
#per-torrent stats
src="${baseurl}tpbs&format=txt"
dest=$base/torrent/$date
if [ ! -d $dest ]; then
   mkdir -p $dest
fi
$wgetcmd -O $dest/$hour.txt.gz $src
gunzip $dest/$hour.txt.gz
ln -sf $dest/$hour.txt $base/torrent/current.txt


#totalstats
src="${baseurl}everything"
dest=$base/everything/$date
if [ ! -d $dest ]; then
   mkdir -p $dest
fi
$wgetcmd -O $dest/$hour.xml $src
ln -sf $dest/$hour.xml $base/everything/current.xml


# generate the json files
hourdate=`date +%Y-%m-%d-%H-%M`
/usr/local/bin/torrentjsonstats.py $base/torrent/current.txt > /srv/web/stats/hourly/torrent-stats-$hourdate.json
ln -sf /srv/web/stats/hourly/torrent-stats-$hourdate.json /srv/web/stats/current-stats.json

if [ $hour == '12' ]; then
  /usr/local/bin/torrentjsonstats.py $base/torrent/current.txt > /srv/web/stats/daily/torrent-stats-$date.json
fi

