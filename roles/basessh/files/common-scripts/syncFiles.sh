#!/bin/bash
# this script lets us sync files off of lockbox via rsync with locking and relatively niceness
# look in rsyncd.conf on lockbox for what's available here

set +e

HOST=batcave01

function cleanlock()
{
    /bin/rm -f /var/lock/$1.lock
}


function quit()
{
    echo $1
    if [ $2 ]
    then
        cleanlock $2
    fi
    exit 2
}

function newlock()
{
    if [ -f /var/lock/$1.lock ]
    then
        quit "Lockfile exists.. Remove /var/lock/$1.lock"
    else
        touch /var/lock/$1.lock
    fi
}

# General help
if [ $3 ] || [ ! $2 ]
then
    quit "$0 source dest"
fi

lockname=`basename $1`
newlock $lockname
if [ ! -d $2 ]
then
	mkdir $2
fi
/usr/bin/rsync -a $HOST::$1/* $2
cleanlock $lockname


