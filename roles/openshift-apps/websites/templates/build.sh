#!/bin/bash -xe
cd /tmp
git clone --branch {% if env == "staging" %}staging{% else %}master{% endif %} https://pagure.io/fedora-web/websites.git
cd websites
exec ./build-prod.sh /output
