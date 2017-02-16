#!/bin/bash

pushd /git/infra-docs >& /dev/null
git fetch -q origin
pushd /srv/web/infra/docs >& /dev/null
git pull -q
