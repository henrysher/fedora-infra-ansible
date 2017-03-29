# -*- coding: utf-8 -*-
from retask.task import Task
from retask.queue import Queue

import autocloud
from autocloud.models import init_model, ComposeJobDetails
from autocloud.producer import publish_to_fedmsg

import datetime

import logging
log = logging.getLogger("fedmsg")


def produce_jobs(infox):
    """ Queue the jobs into jobqueue
    :args infox: list of dictionaries contains the image url and the buildid
    """
    jobqueue = Queue('jobqueue')
    jobqueue.connect()

    family_mapping = {
        'Cloud_Base': 'b',
        'Atomic': 'a'
    }

    session = init_model()
    timestamp = datetime.datetime.now()
    for info in infox:
        image_name = info['path'].split('/')[-1].split(info['arch'])[0]
        jd = ComposeJobDetails(
            arch=info['arch'],
            compose_id=info['compose']['id'],
            created_on=timestamp,
            family=family_mapping[info['subvariant']],
            image_url=info['absolute_path'],
            last_updated=timestamp,
            release=info['compose']['release'],
            status='q',
            subvariant=info['subvariant'],
            user='admin',
            image_format=info['format'],
            image_type=info['type'],
            image_name=image_name,
        )
        session.add(jd)
        session.commit()

        job_details_id = jd.id
        log.info('Save {jd_id} to database'.format(jd_id=job_details_id))

        info.update({'job_id': jd.id})
        task = Task(info)
        jobqueue.enqueue(task)
        log.info('Enqueue {jd_id} to redis'.format(jd_id=job_details_id))

        publish_to_fedmsg(topic='image.queued',
                          compose_url=info['absolute_path'],
                          compose_id=info['compose']['id'],
                          image_name=image_name,
                          status='queued',
                          job_id=info['job_id'],
                          release=info['compose']['release'],
                          family=jd.family.value,
                          type=info['type'])

        session.close()


def is_valid_image(image_url):
    if autocloud.VIRTUALBOX:
        supported_image_ext = ('.vagrant-virtualbox.box',)
    else:
        supported_image_ext = ('.qcow2', '.vagrant-libvirt.box')

    if image_url.endswith(supported_image_ext):
        return True

    return False


def get_image_name(image_name):
    if 'vagrant' in image_name.lower():
        if autocloud.VIRTUALBOX:
            image_name = '{image_name}-Virtualbox'.format(
                image_name=image_name)
        else:
            image_name = '{image_name}-Libvirt'.format(image_name=image_name)
    return image_name
