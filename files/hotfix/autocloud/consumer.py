# -*- coding: utf-8 -*-
from datetime import datetime

import requests
import fedmsg.consumers
import fedfind.release

from sqlalchemy import exc

import autocloud

from autocloud.models import init_model, ComposeDetails, ComposeJobDetails
from autocloud.producer import publish_to_fedmsg
from autocloud.utils import is_valid_image, produce_jobs

import logging
log = logging.getLogger("fedmsg")

DEBUG = autocloud.DEBUG


class AutoCloudConsumer(fedmsg.consumers.FedmsgConsumer):
    """
    Fedmsg consumer for Autocloud
    """

    if DEBUG:
        topic = [
            'org.fedoraproject.dev.__main__.pungi.compose.status.change'
        ]

    else:
        topic = [
            'org.fedoraproject.prod.pungi.compose.status.change'
        ]

    config_key = 'autocloud.consumer.enabled'

    def __init__(self, *args, **kwargs):
        self.supported_archs = [arch for arch, _ in ComposeJobDetails.ARCH_TYPES]

        log.info("Autocloud Consumer is ready for action.")
        super(AutoCloudConsumer, self).__init__(*args, **kwargs)

    def consume(self, msg):
        """ This is called when we receive a message matching the topic. """

        log.info('Received %r %r' % (msg['topic'], msg['body']['msg_id']))

        STATUS_F = ('FINISHED_INCOMPLETE', 'FINISHED',)
        VARIANTS_F = ('CloudImages',)

        images = []
        compose_db_update = False
        msg_body = msg['body']
        status = msg_body['msg']['status']
        compose_images_json = None

        if status in STATUS_F:
            location = msg_body['msg']['location']
            json_metadata = '{}/metadata/images.json'.format(location)
            resp = requests.get(json_metadata)
            compose_images_json = getattr(resp, 'json', False)

        if compose_images_json is not None:
            compose_images_json = compose_images_json()
            compose_images = compose_images_json['payload']['images']
            compose_details = compose_images_json['payload']['compose']
            compose_images = dict((variant, compose_images[variant])
                                  for variant in VARIANTS_F
                                  if variant in compose_images)
            compose_id = compose_details['id']
            rel = fedfind.release.get_release(cid=compose_id)
            release = rel.release
            compose_details.update({'release': release})

            compose_images_variants = [variant for variant in VARIANTS_F
                                       if variant in compose_images]

            for variant in compose_images_variants:
                compose_image = compose_images[variant]
                for arch, payload in compose_image.iteritems():

                    if arch not in self.supported_archs:
                        continue

                    for item in payload:
                        relative_path = item['path']
                        if not is_valid_image(relative_path):
                            continue
                        absolute_path = '{}/{}'.format(location, relative_path)
                        item.update({
                            'compose': compose_details,
                            'absolute_path': absolute_path,
                        })
                        images.append(item)
                        compose_db_update = True

            if compose_db_update:
                session = init_model()
                compose_date = datetime.strptime(compose_details['date'], '%Y%m%d')
                try:
                    cd = ComposeDetails(
                        date=compose_date,
                        compose_id=compose_details['id'],
                        respin=compose_details['respin'],
                        type=compose_details['type'],
                        status=u'q',
                        location=location,
                    )

                    session.add(cd)
                    session.commit()

                    compose_details.update({
                        'status': 'queued',
                        'compose_job_id': cd.id,
                    })
                    publish_to_fedmsg(topic='compose.queued',
                                      **compose_details)
                except exc.IntegrityError:
                    session.rollback()
                    cd = session.query(ComposeDetails).filter_by(
                        compose_id=compose_details['id']).first()
                    log.info('Compose already exists %s: %s' % (
                        compose_details['id'],
                        cd.id
                    ))
                session.close()

            num_images = len(images)
            for pos, image in enumerate(images):
                image.update({'pos': (pos+1, num_images)})

            produce_jobs(images)
