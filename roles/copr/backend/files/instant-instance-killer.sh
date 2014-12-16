#!/usr/bin/env bash

source /home/copr/cloud/ec2rc.sh

/bin/euca-describe-instances | grep INSTANCE | while read line; do
    id="$(echo $line | cut -d' ' -f2)"
    state="$(echo $line | cut -d' ' -f6)"
    if [[ "$state" == "error" ]]; then
        /bin/euca-terminate-instances "$id"
    fi
done
