#!/bin/bash

# These defaults are commented out because selinux doesn't like us running that
# hostname on rhel7 for some reason.  Anyways, we always pass in the arguments
# via the collectd configuration information so wth.  -- threebean
#pause=10
#host=$( /usr/bin/hostname -s )

while getopts "h:p:s:" c; do
       case $c in
               h)      host=$OPTARG;;
               p)      pause=$OPTARG;;
               *)      echo "Usage: /bin/bash [-h <hostname>] [-p <seconds>]";;
       esac
done


 while [ $? -eq 0 ] ; do
   time="$(date +%s)"
   for db in {{ ' '.join(databases) }}
   do
      echo "PUTVAL $host/pg_conns/current_connections-$db $time:$(ps auxwww | grep -c $db)"
   done
   sleep $pause
 done
