# -*- coding: utf-8 -*-

import fedmsg.consumers
import koji

from autocloud.utils import get_image_url, produce_jobs, get_image_name
import autocloud

import logging
log = logging.getLogger("fedmsg")

DEBUG = autocloud.DEBUG


class AutoCloudConsumer(fedmsg.consumers.FedmsgConsumer):

    if DEBUG:
        topic = [
            'org.fedoraproject.dev.__main__.buildsys.build.state.change',
            'org.fedoraproject.dev.__main__.buildsys.task.state.change',
        ]

    else:
        topic = [
            'org.fedoraproject.prod.buildsys.build.state.change',
            'org.fedoraproject.prod.buildsys.task.state.change',
        ]

    config_key = 'autocloud.consumer.enabled'

    def __init__(self, *args, **kwargs):
        super(AutoCloudConsumer, self).__init__(*args, **kwargs)

    def _get_tasks(self, builds):
        """ Takes a list of koji createImage task IDs and returns dictionary of
        build ids and image url corresponding to that build ids"""

        if autocloud.VIRTUALBOX:
            _supported_images = ('Fedora-Cloud-Base-Vagrant',
                                 'Fedora-Cloud-Atomic-Vagrant',)
        else:
            _supported_images = ('Fedora-Cloud-Base-Vagrant',
                                 'Fedora-Cloud-Atomic-Vagrant',
                                 'Fedora-Cloud-Atomic', 'Fedora-Cloud-Base',)

        for build in builds:
            log.info('Got Koji build {0}'.format(build))

        # Create a Koji connection to the Fedora Koji instance
        koji_session = koji.ClientSession(autocloud.KOJI_SERVER_URL)

        image_files = []  # list of full URLs of files

        if len(builds) == 1:
            task_result = koji_session.getTaskResult(builds[0])
            name = task_result.get('name')
            #TODO: Change to get the release information from PDC instead
            # of koji once it is set up
            release = task_result.get('version')
            if name in _supported_images:
                task_relpath = koji.pathinfo.taskrelpath(int(builds[0]))
                url = get_image_url(task_result.get('files'), task_relpath)
                if url:
                    name = get_image_name(image_name=name)
                    data = {
                        'buildid': builds[0],
                        'image_url': url,
                        'name': name,
                        'release': release,
                    }
                    image_files.append(data)
        elif len(builds) >= 2:
            koji_session.multicall = True
            for build in builds:
                koji_session.getTaskResult(build)
            results = koji_session.multiCall()
            for result in results:

                if not result:
                    continue

                name = result[0].get('name')
                if name not in _supported_images:
                    continue

                #TODO: Change to get the release information from PDC instead
                # of koji once it is set up
                release = result[0].get('version')
                task_relpath = koji.pathinfo.taskrelpath(
                    int(result[0].get('task_id')))
                url = get_image_url(result[0].get('files'), task_relpath)
                if url:
                    name = get_image_name(image_name=name)
                    data = {
                        'buildid': result[0]['task_id'],
                        'image_url': url,
                        'name': name,
                        'release': release,
                    }
                    image_files.append(data)

        return image_files

    def consume(self, msg):
        """ This is called when we receive a message matching the topic. """

        if msg['topic'].endswith('.buildsys.task.state.change'):
            # Do the thing you've always done...  this will go away soon.
            # releng is transitioning away from it.
            self._consume_scratch_task(msg)
        elif msg['topic'].endswith('.buildsys.build.state.change'):
            # Do the new thing we need to do.  handle a 'real build' from koji,
            # not just a scratch task.
            self._consume_real_build(msg)
        else:
            raise NotImplementedError("Should be impossible to get here...")

    def _consume_real_build(self, msg):
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

        koji_session = koji.ClientSession(autocloud.KOJI_SERVER_URL)
        children = koji_session.getTaskChildren(msg['task_id'])
        for child in children:
            if child["method"] == "createImage":
                builds.append(child["id"])

        if len(builds) > 0:
            produce_jobs(self._get_tasks(builds))

    def _consume_scratch_task(self, msg):
        builds = list()  # These will be the Koji build IDs to upload, if any.

        msg_info = msg["body"]["msg"]["info"]

        log.info('Received %r %r' % (msg['topic'], msg['body']['msg_id']))

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
            produce_jobs(self._get_tasks(builds))
