#!/bin/sh

checkmodule -M -m -o copr_rules.mod copr_rules.te
semodule_package -o copr_rules.pp -m copr_rules.mod
