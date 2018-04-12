#!/bin/env python
# -*- coding: utf8 -*-
""" Triggers an upload process with the specified raw.xz URL. """

import argparse
import logging
import logging.config
import multiprocessing.pool

import fedmsg.config
import fedimg.uploader

logging.config.dictConfig(fedmsg.config.load_config()['logging'])
log = logging.getLogger('fedmsg')


def trigger_upload(url, compose_id, push_notifications):
    upload_pool = multiprocessing.pool.ThreadPool(processes=4)
    compose_meta = {'compose_id': compose_id}
    fedimg.uploader.upload(upload_pool, [url], compose_meta=compose_meta)


def get_args():
    parser = argparse.ArgumentParser(
        description="Trigger a manual upload process with the "
                    "specified raw.xz URL")
    parser.add_argument(
        "-u", "--url", type=str, help=".raw.xz URL", required=True)
    parser.add_argument(
        "-c", "--compose-id", type=str, help="compose id of the .raw.xz file",
        required=True)
    parser.add_argument(
        "-p", "--push-notifications",
        help="Bool to check if we need to push fedmsg notifications",
        action="store_true", required=False)
    args = parser.parse_args()

    return args.url, args.compose_id, args.push_notifications


def main():
    url, compose_id, push_notifications = get_args()
    trigger_upload(url, compose_id, push_notifications)

if __name__ == '__main__':
    main()
