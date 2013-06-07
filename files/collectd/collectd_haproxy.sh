#!/bin/bash

sock='/var/run/haproxy-stat'
host="$(hostname -s)"
pause=10

while getopts "h:p:s:" c; do
       case $c in
               h)      host=$OPTARG;;
               p)      pause=$OPTARG;;
               s)      sock=$OPTARG;;
               *)      echo "Usage: $0 [-h <hostname>] [-p <seconds>] [-s <sockfile>]";;
       esac
done

while [ $? -eq 0 ]; do
       time="$(date +%s)"
       echo 'show stat' | socat - UNIX-CLIENT:$sock \
       |while IFS=',' read pxname svname qcur qmax scur smax slim stot bin bout dreq dresp ereq econ eresp wretr wredis status weight act bck chkfail chdown lastchg downtime qlimit pid iid sid throttle lbtot tracked type; do
               [ "$svname" != 'BACKEND' ] && continue
               echo "PUTVAL $host/haproxy/haproxy_backend-$pxname $time:$stot:$econ:$eresp"
       done
       sleep $pause
done

