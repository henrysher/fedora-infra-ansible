#!/bin/bash

# sync also to new mirrorlist containers on proxies

MIRRORLIST_PROXY="{% for host in groups['mirrorlist_proxies'] %} {{ host }} {% endfor %}"

for s in ${MIRRORLIST_PROXY}; do
	rsync -az --delete-delay --delay-updates --delete /usr/share/mirrormanager2/country_continent.csv /var/lib/mirrormanager/{*pkl,*txt,*proto} ${s}:/srv/mirrorlist/data/mirrorlist1/
done
