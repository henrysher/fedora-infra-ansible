#!/bin/bash

pause=10
host=$( hostname -s )

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
      echo "PUTVAL $host/pg_conns/pg_conns-$db $time:$(ps auxwww | grep -c $db)"
   done
   sleep $pause
 done
