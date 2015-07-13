#!/bin/bash 
# skvidal - 2013-06-25
# takes 2 args: grep_search_string subdir_to_write_to
# ex: bash grab-daily-logs.sh /repos/openstack/ rdo


logpath='/var/log/httpd/'
basedest="/srv/people/site/accesslogs/"
logfn='fedorapeople.org-access.log'
search="$1"
destpath="$basedest/$2"
dstamp=`date -d yesterday +%Y-%m-%d`

# basedest
if [ ! -d $basedest ]; then
    mkdir -p $basedest
    chown apache.apache $basedest
    chmod 770 $basedest
fi

#make sure there is an index.html up one so you can't find it
if [ ! -f $basedest/index.html ]; then
    echo "nothing to see" > $basedest/index.html
    chmod 664 $basedest/index.html
fi

#make the destpath
if [ ! -d $destpath ]; then
    mkdir -p $destpath
    chown apache.apache $destpath
    chmod 770 $destpath
fi

# grab the logs
grep $search $logpath/${logfn}-${dstamp} >> ${destpath}/${dstamp}.log
chown apache.apache $destpath/${dstamp}.log
chmod 640 $destpath/${dstamp}.log

# clean up the old logs
/usr/sbin/tmpwatch -f 720 -m $destpath
