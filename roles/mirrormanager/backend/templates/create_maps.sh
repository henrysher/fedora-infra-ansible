#!/bin/sh

WORLDMAP="/usr/bin/mm2_generate-worldmap"

FRONTENDS="{% for host in groups['mm_frontend'] %} {{ host }} {% endfor %}"

OUTPUT=`mktemp -d`

trap "rm -f ${OUTPUT}/*; rmdir ${OUTPUT}" QUIT TERM INT HUP EXIT

${WORLDMAP} --output ${OUTPUT} > /dev/null

for f in ${FRONTENDS}; do
        rsync -aq ${OUTPUT}/{map.png,mirrors_location.txt} ${f}:/var/www/mirrormanager-statistics/map/
done
