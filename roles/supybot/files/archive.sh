#!/bin/bash

cd /srv/web/meetbot/teams
for team in *; do
    pushd $team >/dev/null 2>&1
    tar -cphf /srv/web/meetbot/archives/$team.tgz *.log.txt
    popd >/dev/null 2>&1
done
