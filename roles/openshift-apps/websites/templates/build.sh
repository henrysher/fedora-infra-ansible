#!/bin/bash -xe
cd /tmp
git clone --branch {% if env == "staging" %}staging{% else %}master{% endif %} https://pagure.io/fedora-web/websites.git
cd websites
git rev-parse HEAD
exec ./build-prod.sh /output
