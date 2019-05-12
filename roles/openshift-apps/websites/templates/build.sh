#!/bin/bash -xe
git clone --branch {% if env == "staging" %}staging{% else %}master{% endif %} https://pagure.io/fedora-web/websites.git
cd websites
exec ./build.sh /output
