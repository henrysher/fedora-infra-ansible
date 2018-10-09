#!/usr/bin/env bash
# (c) 2018 Red Hat, Inc.
# LGPL
# Author: Rick Elrod <relrod@redhat.com>

CMD="aws s3 sync                   \
  --delete                         \
  --exclude */.snapshot/*          \
  --exclude */source/*             \
  --exclude */SRPMS/*              \
  --exclude */debug/*              \
  --exclude */beta/*               \
  --exclude */ppc/*                \
  --exclude */ppc64/*              \
  --exclude */repoview/*           \
  --exclude */Fedora/*             \
  --exclude */Live/*               \
  --exclude */isolinux/*           \
  --exclude */images/*             \
  --exclude */EFI/*                \
  --exclude */core/*               \
  --exclude */extras/*             \
  --exclude */LiveOS/*             \
  --exclude */development/*        \
  --exclude */releases/test/*      \
  --exclude */releases/8/*         \
  --exclude */releases/9/*         \
  --exclude */releases/10/*        \
  --exclude */releases/11/*        \
  --exclude */releases/12/*        \
  --exclude */releases/13/*        \
  --exclude */releases/14/*        \
  --exclude */releases/15/*        \
  --exclude */releases/16/*        \
  --exclude */releases/17/*        \
  --exclude */releases/18/*        \
  --exclude */releases/19/*        \
  --exclude */releases/20/*        \
  --exclude */releases/21/*        \
  --exclude */releases/22/*        \
  --exclude */releases/23/*        \
  --exclude */releases/24/*        \
  --exclude */releases/25/*        \
  --exclude */releases/26/*        \
  --exclude */updates/8/*          \
  --exclude */updates/9/*          \
  --exclude */updates/10/*         \
  --exclude */updates/11/*         \
  --exclude */updates/12/*         \
  --exclude */updates/13/*         \
  --exclude */updates/14/*         \
  --exclude */updates/15/*         \
  --exclude */updates/16/*         \
  --exclude */updates/17/*         \
  --exclude */updates/18/*         \
  --exclude */updates/19/*         \
  --exclude */updates/20/*         \
  --exclude */updates/21/*         \
  --exclude */updates/22/*         \
  --exclude */updates/23/*         \
  --exclude */updates/24/*         \
  --exclude */updates/25/*         \
  --exclude */updates/26/*         \
  --exclude */updates/testing/8/*  \
  --exclude */updates/testing/9/*  \
  --exclude */updates/testing/10/* \
  --exclude */updates/testing/11/* \
  --exclude */updates/testing/12/* \
  --exclude */updates/testing/13/* \
  --exclude */updates/testing/14/* \
  --exclude */updates/testing/15/* \
  --exclude */updates/testing/16/* \
  --exclude */updates/testing/17/* \
  --exclude */updates/testing/18/* \
  --exclude */updates/testing/19/* \
  --exclude */updates/testing/20/* \
  --exclude */updates/testing/21/* \
  --exclude */updates/testing/22/* \
  --exclude */updates/testing/23/* \
  --exclude */updates/testing/24/* \
  --exclude */updates/testing/25/* \
  --exclude */updates/testing/26/* \
  --no-follow-symlinks             \
  "
  #--dryrun                         \

# Sync EPEL
echo $CMD /srv/pub/epel/ s3://s3-mirror-us-west-1-02.fedoraproject.org/pub/epel/
$CMD /srv/pub/epel/ s3://s3-mirror-us-west-1-02.fedoraproject.org/pub/epel/

# Sync Fedora
echo $CMD /srv/pub/fedora/ s3://s3-mirror-us-west-1-02.fedoraproject.org/pub/fedora/
$CMD /srv/pub/fedora/ s3://s3-mirror-us-west-1-02.fedoraproject.org/pub/fedora/
