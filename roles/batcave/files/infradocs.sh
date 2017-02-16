#!/bin/bash

pushd /git/infra-docs
git fetch -q origin
pushd /srv/web/infra/docs
git pull -q
