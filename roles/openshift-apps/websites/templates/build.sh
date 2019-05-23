#!/bin/bash -xe
cd /tmp
git clone --branch {% if env == "staging" %}staging{% else %}master{% endif %} https://pagure.io/fedora-web/websites.git
cd websites
git rev-parse HEAD
bash ./build-prod.sh /output
curl -O https://codeblock.fedorapeople.org/atomic-htaccess.py
mkdir -p out build
python atomic-htaccess.py
cp -r out/. /output/
