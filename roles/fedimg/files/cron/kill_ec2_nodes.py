#!/bin/env python
# -*- coding: utf8 -*-

# NOTE this is taken from the github repo
# https://github.com/fedora-infra/fedimg/blob/develop/bin/kill_ec2_nodes.py

import logging
logging.basicConfig()

from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver
import datetime
import fedimg

EC2_ACCESS_ID = fedimg.AWS_ACCESS_ID
EC2_SECRET_KEY = fedimg.AWS_SECRET_KEY

def kill_all_instances(region):
    """
    Kills all the instances which are running for 2 hours or more.

    :param region: AWS region
    """
    cls = get_driver(Provider.EC2)
    driver = cls(EC2_ACCESS_ID, EC2_SECRET_KEY, region=region)
    nodes = driver.list_nodes()
    for n in nodes:
        d1 = datetime.datetime.strptime(n.extra['launch_time'], '%Y-%m-%dT%H:%M:%S.000Z')
        d2 =  datetime.datetime.utcnow()
        delta = d2 - d1
        if delta.total_seconds() > 7200: # If more than 2 hours of up time.
            n.destroy()


if __name__ == '__main__':
    regions = set([metadata.split('|')[0]
                   for metadata in fedimg.AWS_AMIS.split('\n')])
    for region in regions:
        kill_all_instances(region)
