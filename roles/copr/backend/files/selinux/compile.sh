#!/bin/sh

checkmodule -M -m -o nrpe_copr.mod nrpe_copr.te
semodule_package -o nrpe_copr.pp -m nrpe_copr.mod
