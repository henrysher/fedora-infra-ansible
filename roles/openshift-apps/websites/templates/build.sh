#!/bin/bash -xe
cd /tmp
git clone --branch {% if env == "staging" %}staging{% else %}master{% endif %} https://pagure.io/fedora-web/websites.git
cd websites
git rev-parse HEAD
bash ./build-prod.sh /output
python generate-htaccess.py
mv out/. /output/
