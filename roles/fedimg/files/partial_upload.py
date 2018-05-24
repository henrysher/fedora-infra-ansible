#!/bin/env python
# -*- coding: utf8 -*-
""" Triggers a partial upload process with the specified raw.xz URL. """

import argparse
import logging
import logging.config

import fedmsg.config

from fedimg.config import AWS_ACCESS_ID
from fedimg.config import AWS_SECRET_KEY
from fedimg.config import AWS_BASE_REGION, AWS_REGIONS
from fedimg.services.ec2.ec2copy import main as ec2copy
from fedimg.services.ec2.ec2initiate import main as ec2main

logging.config.dictConfig(fedmsg.config.load_config()['logging'])
log = logging.getLogger('fedmsg')


def get_args():
    parser = argparse.ArgumentParser(
        description="Trigger a partial upload based on the arguments")
    parser.add_argument(
        "-u", "--url", type=str, help=".raw.xz URL", required=True)
    parser.add_argument(
        "-c", "--compose-id", type=str, help="compose id of the .raw.xz file",
        required=True)
    parser.add_argument(
        "-p", "--push-notifications",
        help="Bool to check if we need to push fedmsg notifications",
        action="store_true", required=False)
    parser.add_argument(
        "-v", "--volume", help="volume type for the image", required=False)

    args = parser.parse_args()

    return (
        args.url,
        args.compose_id,
        args.push_notifications,
        args.volume
    )


def main():
    url, compose_id, push_notifications, volume = get_args()

    if volume is not None:
        volume = [volume]

    images_metadata = ec2main(
        image_urls=url,
        access_id=AWS_ACCESS_ID,
        secret_key=AWS_SECRET_KEY,
        regions=None,
        volume_types=volume,
        push_notifications=push_notifications,
        compose_id=compose_id
    )

    for image_metadata in images_metadata:
        image_id = image_metadata['image_id']
        aws_regions = list(set(AWS_REGIONS) - set([AWS_BASE_REGION]))
        ec2copy(
            aws_regions,
            AWS_ACCESS_ID,
            AWS_SECRET_KEY,
            image_ids=[image_id],
            push_notifications=push_notifications,
            compose_id=compose_id
        )


if __name__ == '__main__':
    main()
