#!/bin/bash

MIRRORLIST_SERVERS="{% for host in groups['mirrorlist2'] %} {{ host }} {% endfor %}"

for s in ${MIRRORLIST_SERVERS}; do
	rsync -az --delete-delay --delay-updates --delete /var/lib/mirrormanager/{*pkl,*txt} ${s}:/var/lib/mirrormanager/
	ssh $s 'kill -HUP $(cat /var/run/mirrormanager/mirrorlist_server.pid)'
done

# sync also to new mirrorlist containers on proxies

MIRRORLIST_PROXY="proxy02.fedoraproject.org proxy05.fedoraproject.org"

for s in ${MIRRORLIST_PROXY}; do
	rsync -az --delete-delay --delay-updates --delete /var/lib/mirrormanager/{*pkl,*txt} ${s}:/srv/mirrorlist/data/mirrorlist1/
done
