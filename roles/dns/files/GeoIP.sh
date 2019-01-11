#!/usr/bin/env bash
# Rick Elrod <relrod@redhat.com>
# (c) 2019 Red Hat, Inc.
# etc.

# Fail early
set -e

rm -f GeoLite2-Country-CSV.zip csvs/*

wget -q -T 5 -t 1 https://geolite.maxmind.com/download/geoip/database/GeoLite2-Country-CSV.zip
unzip -j GeoLite2-Country-CSV.zip -d csvs/
geoip.py csvs/GeoLite2-Country-Blocks-IPv4.csv csvs/GeoLite2-Country-Blocks-IPv6.csv csvs/GeoLite2-Country-Locations-en.csv > /var/named/GeoIP.acl
