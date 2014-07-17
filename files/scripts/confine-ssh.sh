#!/bin/sh
# Confine ssh commands
case "$SSH_ORIGINAL_COMMAND" in
*\&*)
echo "Rejected"
;;
*\;*)
echo "Rejected"
;;
rsync\ --server\ --sender*)
$SSH_ORIGINAL_COMMAND
;;
*)
echo "Rejected"
;;
esac
