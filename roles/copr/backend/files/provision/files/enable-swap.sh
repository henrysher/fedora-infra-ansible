#!/usr/bin/bash

set -e

swap_device=
if test -e /dev/xvda1 && test -e /dev/nvme0n1; then
    swap_device=/dev/nvme0n1
elif test -e /dev/nvme1n1; then
    swap_device=/dev/nvme1n1
fi

test -n "$swap_device"

mkswap "$swap_device"
swapon "$swap_device"
