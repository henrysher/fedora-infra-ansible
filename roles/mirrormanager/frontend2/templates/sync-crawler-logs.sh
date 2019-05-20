#!/bin/bash

CRAWLERS="{% for host in groups['mm_crawler'] %} {{ host }} {% endfor %}"

for i in ${CRAWLERS}; do
	rsync -aq ${i}::crawler/*log /var/log/mirrormanager/crawler/
done
