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
import koji

import fedimg.uploader
from fedimg.util import get_rawxz_url


class KojiConsumer(fedmsg.consumers.FedmsgConsumer):
    """ Listens for image Koji task completion and sends image files
        produced by the child createImage tasks to the uploader. """

    # It used to be that all *image* builds appeared as scratch builds on the
    # task.state.change topic.  However, with the switch to pungi4, some of
    # them (and all of them in the future) appear as full builds under the
    # build.state.change topic.  That means we have to handle both cases like
    # this, at least for now.
    topic = [
        'org.fedoraproject.prod.buildsys.task.state.change',  # scratch tasks
        'org.fedoraproject.prod.buildsys.build.state.change', # full builds (pungi4)
    ]

    config_key = 'kojiconsumer'

    def __init__(self, *args, **kwargs):
        super(KojiConsumer, self).__init__(*args, **kwargs)

        # threadpool for upload jobs
        self.upload_pool = multiprocessing.pool.ThreadPool(processes=4)

        log.info("Super happy fedimg ready and reporting for duty.")

    def _get_upload_urls(self, builds):
        """ Takes a list of koji createImage task IDs and returns a list of
        URLs to .raw.xz image files that should be uploaded. """

        for build in builds:
            log.info('Got Koji build {0}'.format(build))

        # Create a Koji connection to the Fedora Koji instance
        koji_session = koji.ClientSession(fedimg.KOJI_SERVER)

        rawxz_files = []  # list of full URLs of files

        # Get all of the .raw.xz URLs for the builds
        if len(builds) == 1:
            task_result = koji_session.getTaskResult(builds[0])
            url = get_rawxz_url(task_result)
            if url:
                rawxz_files.append(url)
        elif len(builds) >= 2:
            koji_session.multicall = True
            for build in builds:
                koji_session.getTaskResult(build)
            results = koji_session.multiCall()
            for result in results:
                if not result: continue
                url = get_rawxz_url(result[0])
                if url:
                    rawxz_files.append(url)

        # We only want to upload:
        # 64 bit: base, atomic, bigdata
        # Not uploading 32 bit, vagrant, experimental, or other images.
        upload_files = []  # files that will actually be uploaded
        for url in rawxz_files:
            u = url.lower()
            if u.find('x86_64') > -1 and u.find('vagrant') == -1:
                if (u.find('fedora-cloud-base') > -1
                        or u.find('fedora-cloud-atomic') > -1
                        or u.find('fedora-cloud-bigdata') > -1):
                    upload_files.append(url)
                    log.info('Image {0} will be uploaded'.format(url))

        return upload_files

    def consume(self, msg):
        """ This is called when we receive a message matching our topics. """

        log.info('Received %r %r' % (msg['topic'], msg['body']['msg_id']))

        if msg['topic'].endswith('.task.state.change'):
            # Scratch tasks.. the old way.
            return self._consume_scratch_task(msg)
        elif msg['topic'].endswith('.build.state.change'):
            # Full builds from pungi4.. the new way.
            return self._consume_full_build(msg)
        else:
            log.error("Unhandled message type received:  %r %r" % (
                msg['topic'], msg['body']['msg_id']))

    def _consume_full_build(self, msg):
        """ This is called when we receive a message matching the newer pungi4
        full build topic.
        """

        builds = list()  # These will be the Koji task IDs to upload, if any.

        msg = msg['body']['msg']
        if msg['owner'] != 'releng':
            log.debug("Dropping message.  Owned by %r" % msg['owner'])
            return

        if msg['instance'] != 'primary':
            log.info("Dropping message.  From %r instance." % msg['instance'])
            return

        # Don't upload *any* images if one of them fails.
        if msg['new'] != 1:
            log.info("Dropping message.  State is %r" % msg['new'])
            return

        # Create a Koji connection to the Fedora Koji instance to query.
        koji_session = koji.ClientSession(fedimg.KOJI_SERVER)
        children = koji_session.getTaskChildren(msg['task_id'])
        for child in children:
            if child["method"] == "createImage":
                builds.append(child["id"])

        if len(builds) > 0:
            fedimg.uploader.upload(self.upload_pool,
                                   self._get_upload_urls(builds))

    def _consume_scratch_task(self, msg):
        """ This is called when we receive a message matching the older scratch
        build topic.
        """

        builds = list()  # These will be the Koji task IDs to upload, if any.

        msg_info = msg["body"]["msg"]["info"]

        # If the build method is "image", we check to see if the child
        # task's method is "createImage".
        if msg_info["method"] == "image":
            if isinstance(msg_info["children"], list):
                for child in msg_info["children"]:
                    if child["method"] == "createImage":
                        # We only care about the image if the build
                        # completed successfully (with state code 2).
                        if child["state"] == 2:
                            builds.append(child["id"])

        if len(builds) > 0:
            fedimg.uploader.upload(self.upload_pool,
                                   self._get_upload_urls(builds))
