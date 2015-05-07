#!/bin/bash

MIRRORLIST_SERVERS="{% for host in groups['mirrorlist2'] %} {{ host }} {% endfor %}"

for s in ${MIRRORLIST_SERVERS}; do
	rsync -a --delete-delay --delay-updates --delete /var/lib/mirrormanager/ ${s}:/var/lib/mirrormanager/
	ssh $s 'kill -HUP $(cat /var/run/mirrormanager/mirrorlist_server.pid)'
done
