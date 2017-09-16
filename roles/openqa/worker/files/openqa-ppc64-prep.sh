#!/bin/sh

# On boot, /dev/kvm perms are 0600 for some reason
chmod ugo+rw /dev/kvm

# SMT must be off for qemu to work properly
ppc64_cpu --smt=off
