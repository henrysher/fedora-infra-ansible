#!/usr/bin/env bash

. /usr/lib64/nagios/plugins/utils.sh

if [[ "$#" -ne 3 ]]; then
  echo "Arguments: key warn crit"
  exit $STATE_UNKNOWN
fi

tasks="$(redis-cli llen "$1" | awk '{print $1}')"

check_range $tasks $2:$3
status=$?

if [[ "$status" == "$STATE_OK" ]]; then
  echo "OK: $1 queue has $tasks tasks"
elif [[ "$status" == "$STATE_WARNING" ]]; then
  echo "WARNING: $1 queue has $tasks tasks"
elif [[ "$status" == "$STATE_CRITICAL" ]]; then
  echo "CRITICAL: $1 queue has $tasks tasks"
fi

exit $status
