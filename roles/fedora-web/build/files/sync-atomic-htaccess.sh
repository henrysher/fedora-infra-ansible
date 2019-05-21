#!/usr/bin/env bash
set -e
cd /srv/web/atomic-htaccess-generator
python /usr/local/bin/atomic-htaccess-generator.py
# The . here is meaningful!
cp -r out/. /srv/websites/getfedora.org/
