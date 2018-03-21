# This file is part of fedimg.
# Copyright (C) 2014 Red Hat, Inc.
#
# fedimg is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# fedimg is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public
# License along with fedimg; if not, see http://www.gnu.org/licenses,
# or write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA
#
# Authors:  David Gay <dgay@redhat.com>
#

import logging
log = logging.getLogger("fedmsg")

import multiprocessing.pool

import fedmsg.consumers
import fedmsg.encoding
import fedfind.release

import fedimg.uploader
from fedimg.util import get_rawxz_urls, safeget


class FedimgConsumer(fedmsg.consumers.FedmsgConsumer):
    """ Listens for image Koji task completion and sends image files
        produced by the child createImage tasks to the uploader. """

    # It used to be that all *image* builds appeared as scratch builds on the
    # task.state.change topic.  However, with the switch to pungi4, some of
    # them (and all of them in the future) appear as full builds under the
    # build.state.change topic.  That means we have to handle both cases like
    # this, at least for now.
    topic = [
        'org.fedoraproject.prod.pungi.compose.status.change',
    ]

    config_key = 'fedimgconsumer'

    def __init__(self, *args, **kwargs):
        super(FedimgConsumer, self).__init__(*args, **kwargs)

        # threadpool for upload jobs
        self.upload_pool = multiprocessing.pool.ThreadPool(processes=4)

        log.info("Super happy fedimg ready and reporting for duty.")

    def consume(self, msg):
        """ This is called when we receive a message matching our topics. """

        log.info('Received %r %r' % (msg['topic'], msg['body']['msg_id']))

        STATUS_F = ('FINISHED_INCOMPLETE', 'FINISHED',)

        msg_info = msg['body']['msg']
        if msg_info['status'] not in STATUS_F:
            return

        location = msg_info['location']
        compose_id = msg_info['compose_id']
        cmetadata = fedfind.release.get_release_cid(compose_id).metadata

        images_meta = safeget(cmetadata, 'images', 'payload', 'images',
                              'CloudImages', 'x86_64')

        if images_meta is None:
            return

        self.upload_urls = get_rawxz_urls(location, images_meta)
        compose_meta = {
            'compose_id': compose_id,
        }

        if len(self.upload_urls) > 0:
            log.info("Processing compose id: %s" % compose_id)
            fedimg.uploader.upload(self.upload_pool,
                                   self.upload_urls,
                                   compose_meta)
