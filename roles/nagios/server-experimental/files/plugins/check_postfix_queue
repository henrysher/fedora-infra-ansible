#!/bin/bash
#
# 19-07-2010
# Author: Cherwin Nooitmeer <cherwin@gmail.com>
#

# exit codes
e_ok=0
e_warning=1
e_critical=2
e_unknown=3

# regular expression that matches queue IDs (e.g. D71EF7AC80F8)
queue_id='^[A-F0-9][A-F0-9][A-F0-9][A-F0-9][A-F0-9][A-F0-9][A-F0-9][A-F0-9][A-F0-9][A-F0-9]'

usage="Invalid command line usage"

if [ -z $1 ]; then
    echo $usage
    exit $e_unknown
fi

while getopts ":w:c:" options
do
    case $options in
        w ) warning=$OPTARG ;;
        c ) critical=$OPTARG ;;
        * ) echo $usage
            exit $e_unknown ;;
    esac
done

# determine queue size
qsize=$(mailq | egrep -c $queue_id)
if [ -z $qsize ]
then
    exit $e_unknown
fi

if [ $qsize -ge $critical ]; then
    retval=$e_critical
elif [ $qsize -ge $warning ]; then
    retval=$e_warning
elif [ $qsize -lt $warning ]; then
    retval=$e_ok
fi

echo "$qsize mail(s) in queue | mail_queue=$qsize"
exit $retval
