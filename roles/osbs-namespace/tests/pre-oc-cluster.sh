#!/bin/bash
set -xeuo pipefail

# Script inspired by:
#   https://github.com/radanalyticsio/radanalyticsio.github.io/blob/master/.travis.yml

TEST_DIR=`pwd`
ORIGIN_DIR=$TEST_DIR/../origin
OC_VERSION='v3.7.0'
OC_RELEASE_NAME='openshift-origin-client-tools-v3.7.0-7ed6862-linux-64bit'

# Add required insecure container registry
sudo sed -i -e 's/sock/sock --insecure-registry 172.30.0.0\/16/' /etc/default/docker
sudo cat /etc/default/docker
sudo service docker restart

# Download and setup oc binary
sudo mkdir -p $ORIGIN_DIR
sudo chmod -R 766 $ORIGIN_DIR
sudo curl -L \
    https://github.com/openshift/origin/releases/download/${OC_VERSION}/${OC_RELEASE_NAME}.tar.gz | \
    sudo tar -C $ORIGIN_DIR -xz ${OC_RELEASE_NAME}/oc
sudo cp $ORIGIN_DIR/${OC_RELEASE_NAME}/oc /bin/
sudo chmod +x /bin/oc

oc version

# Below cmd is important to get oc working in ubuntu
sudo docker run -v /:/rootfs -ti --rm \
    --entrypoint=/bin/bash \
    --privileged openshift/origin:v3.7.0 \
    -c "mv /rootfs/bin/findmnt /rootfs/bin/findmnt.backup"

# Avoid error from travis wrapper script with unbound variable:
#   https://github.com/travis-ci/travis-ci/issues/5434
set +u
