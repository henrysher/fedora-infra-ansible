#!/bin/bash

# take location of planet config
# pull it and run planet against it

buildconfig=$1
if [ ! -z "$2" ]; then 
    planetname="$2"
else
    planetname=`echo $buildconfig| cut -d'/' -f4`
fi

planetcmd=/usr/bin/venus-planet
buildcfgcmd="/usr/local/bin/planetconfigbuilder.py $1"
cfgfile=`$buildcfgcmd`
if [ $? != 0 ]; then
   echo "could not build config file for $1"
fi

/usr/local/bin/lock-wrapper "$planetname" "$planetcmd $cfgfile"

