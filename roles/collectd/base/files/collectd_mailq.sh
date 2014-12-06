#!/bin/bash
export PATH=/usr/local/bin:/usr/bin:/bin:/usr/local/sbin:/usr/sbin:/sbin

host=$(hostname -s)
pause=10

while getopts "h:p:s:" opt; do
    case "$opt" in
        h)
            host=$OPTARG
            ;;
        p)
            pause=$OPTARG
            ;;
        *)
            echo "Usage: $0 [-h <hostname>] [-p <seconds>]" >&2;
            exit 1
            ;;
    esac
done

while [ $? -eq 0 ]; do
    ts=$(date +%s)
    queue_size=$(mailq | awk 'END { print (/Mail queue is empty/ ? 0 : $5) }')
    echo "PUTVAL \"$host/mail_queue/email_count\" $ts:$queue_size";
    sleep $pause
done
