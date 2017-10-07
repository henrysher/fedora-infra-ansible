#!/bin/bash
# Borrowed heavily from the syncStatic cronjob script.

if [ ! -d  /srv/web/whatcanidoforfedora.org/.git ]
then
    /usr/bin/git clone -q \
        https://github.com/fedora-infra/asknot-ng.git \
        /srv/web/whatcanidoforfedora.org
fi

cd /srv/web/whatcanidoforfedora.org

/usr/bin/git clean -q -fdx || exit 1
/usr/bin/git reset -q --hard || exit 1
/usr/bin/git checkout -q develop || exit 1
/usr/bin/git pull -q --ff-only || exit 1

err=$(
    {
        ./build.sh &&\
        rsync -qa --delete-after --delay-updates build/ "/srv/web/whatcanidoforfedora.org/"; \
    } 2>&1
)

rc=$?
if [ $rc -ne 0 ]; then
    echo "whatcanidoforfedora.org build failed"
    echo "===================================="
    echo "$err"
    echo
fi
