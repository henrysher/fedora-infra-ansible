# -*- coding: utf-8 -*-
import copy
import datetime
import json
import os
import subprocess
import sys

from collections import defaultdict

import fedfind.release

from retask.queue import Queue

from autocloud.constants import SUCCESS, FAILED, ABORTED, RUNNING
from autocloud.models import init_model, ComposeJobDetails, ComposeDetails
from autocloud.producer import publish_to_fedmsg

import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

tree = lambda: defaultdict(tree)
results = tree()

def handle_err(session, data, out, err):
    """
    Prints the details and exits.
    :param out:
    :param err:
    :return: None
    """
    # Update DB first.
    data.status = u'f'
    data.output = "%s: %s" % (out, err)
    timestamp = datetime.datetime.now()
    data.last_updated = timestamp
    session.commit()
    log.debug("%s: %s", out, err)


def system(cmd):
    """
    Runs a shell command, and returns the output, err, returncode

    :param cmd: The command to run.
    :return:  Tuple with (output, err, returncode).
    """
    ret = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
    out, err = ret.communicate()
    returncode = ret.returncode
    return out, err, returncode


def refresh_storage_pool():
    '''Refreshes libvirt storage pool.

    http://kushaldas.in/posts/storage-volume-error-in-libvirt-with-vagrant.html
    '''
    out, err, retcode = system('virsh pool-list')
    lines = out.split('\n')
    if len(lines) > 2:
        for line in lines[2:]:
            words = line.split()
            if len(words) == 3:
                if words[1] == 'active':
                    system('virsh pool-refresh {0}'.format(words[0]))


def image_cleanup(image_path):
    """
    Delete the image if it is processed or if there is any exception occur

    :param basename: Absoulte path for image
    """
    if os.path.exists(image_path):
        try:
            os.remove(image_path)
        except OSError as e:
            log.error('Error: %s - %s.', e.filename, e.strerror)


def create_dirs():
    """
    Creates the runtime dirs
    """
    system('mkdir -p /var/run/tunir')
    system('mkdir -p /var/run/autocloud')


def create_result_text(out):
    """
    :param out: Output text from the command.
    """
    lines = out.splitlines()
    for line in lines:
        if line.startswith('Result file at:'):
            result_filename = line.split(' ')[1]

    result_filename = result_filename.strip()
    if os.path.exists(result_filename):
        new_content = ''
        with open(result_filename) as fobj:
            new_content = fobj.read()
        job_status_index = out.find('Job status:')
        if job_status_index == -1:
            return out # No job status in the output.
        new_line_index = out[job_status_index:].find('\n')
        out = out[:job_status_index + new_line_index]
        out = out + '\n\n' + new_content
        system('rm -f {0}'.format(result_filename))
        return out
    return out


def auto_job(task_data):
    """
    This fuction queues the job, and then executes the tests,
    updates the db as required.

    :param taskid: Koji taskid.
    :param image_url: URL to download the fedora image.
    :return:
    """
    # TODO:
    # We will have to update the job information on DB, rather
    # than creating it. But we will do it afterwards.

    compose_image_url = task_data['absolute_path']
    compose_id = task_data['compose']['id']
    release = task_data['compose']['release']
    job_id = task_data['job_id']
    image_type = task_data['type']

    job_type = 'vm'

    # Just to make sure that we have runtime dirs
    create_dirs()

    session = init_model()
    timestamp = datetime.datetime.now()
    data = None
    try:
        data = session.query(ComposeJobDetails).get(str(job_id))
        data.status = u'r'
        data.last_updated = timestamp
    except Exception as err:
        log.error("%s" % err)
        log.error("%s: %s", compose_id, compose_image_url)
    session.commit()

    params = {
        'compose_url': compose_image_url,
        'compose_id': compose_id,
        'status': RUNNING,
        'job_id': job_id,
        'release': release,
        'family': data.family.value,
        'type': image_type,
        'image_name': data.image_name,
    }
    publish_to_fedmsg(topic='image.running', **params)

    # Now we have job queued, let us start the job.
    # Step 1: Download the image
    image_url = compose_image_url
    basename = os.path.basename(image_url)
    image_path = '/var/run/autocloud/%s' % basename
    log.debug("Going to download {0}".format(image_url))
    out, err, ret_code = system('wget %s -O %s' % (image_url, image_path))
    if ret_code:
        image_cleanup(image_path)
        handle_err(session, data, out, err)
        log.debug("Return code: %d" % ret_code)

        params.update({'status': FAILED})
        publish_to_fedmsg(topic='image.failed', **params)
        return FAILED, check_status_of_compose_image(compose_id)

    # Step 2: Create the conf file with correct image path.
    if basename.find('vagrant') == -1:
        conf = {"image": "/var/run/autocloud/%s" % basename,
                "name": "fedora",
                "password": "passw0rd",
                "ram": 2048,
                "type": "vm",
                "user": "fedora"}

    else: # We now have a Vagrant job.
        conf = {
            "name": "fedora",
            "type": "vagrant",
            "image": "/var/run/autocloud/%s" % basename,
            "ram": 2048,
            "user": "vagrant",
            "port": "22"
        }
        if basename.find('virtualbox') != -1:
            conf['provider'] = 'virtualbox'
        job_type = 'vagrant'

        #Now let us refresh the storage pool
        refresh_storage_pool()

    with open('/var/run/autocloud/fedora.json', 'w') as fobj:
        fobj.write(json.dumps(conf))

    system('/usr/bin/cp -f /etc/autocloud/fedora.txt /var/run/autocloud/fedora.txt')

    cmd = 'tunir --job fedora --config-dir /var/run/autocloud/'
    # Now run tunir
    out, err, ret_code = system(cmd)
    if ret_code:
        image_cleanup(image_path)
        handle_err(session, data, create_result_text(out), err)
        log.debug("Return code: %d" % ret_code)
        params.update({'status': FAILED})
        publish_to_fedmsg(topic='image.failed', **params)
        return FAILED, check_status_of_compose_image(compose_id)
    else:
        image_cleanup(image_path)

    # Enabling direct stdout as output of the command
    out = create_result_text(out)
    if job_type == 'vm':
        com_text = out[out.find('/usr/bin/qemu-kvm'):]
    else:
        com_text = out

    data.status = u's'
    timestamp = datetime.datetime.now()
    data.last_updated = timestamp
    data.output = com_text
    session.commit()

    params.update({'status': SUCCESS})
    publish_to_fedmsg(topic='image.success', **params)
    return SUCCESS, check_status_of_compose_image(compose_id)


def check_status_of_compose_image(compose_id):
    session = init_model()
    compose_job_objs = session.query(ComposeJobDetails).filter_by(
        compose_id=compose_id).all()
    compose_obj = session.query(ComposeDetails).filter_by(
        compose_id=compose_id).first()

    is_running = False

    for compose_job_obj in compose_job_objs:
        status = compose_job_obj.status.code
        if status in ('r', 'q'):
            is_running = True
            break

    if is_running:
        return False

    for compose_job_obj in compose_job_objs:
        status = compose_job_obj.status.code

        if status in ('s',):
            results[compose_id][SUCCESS] = results[compose_id].get(SUCCESS, 0) + 1
        elif status in ('f', 'a'):
            results[compose_id][FAILED] = results[compose_id].get(FAILED, 0) + 1

    if isinstance(results[compose_id][SUCCESS], defaultdict):
        results[compose_id][SUCCESS] = 0

    if isinstance(results[compose_id][FAILED], defaultdict):
        results[compose_id][FAILED] = 0

    compose_obj.passed = results[compose_id][SUCCESS]
    compose_obj.failed = results[compose_id][FAILED]
    compose_obj.status = u'c'

    session.commit()

    compose_id = compose_obj.compose_id
    rel = fedfind.release.get_release(cid=compose_id)
    release = rel.release

    params = {
        'compose_id': compose_obj.compose_id,
        'respin': compose_obj.respin,
        'type': compose_obj.type,
        'date': datetime.datetime.strftime(compose_obj.date, '%Y%m%d'),
        'results': results[compose_id],
        'release': release,
        'status': 'completed',
        'compose_job_id': compose_obj.id
    }

    publish_to_fedmsg(topic='compose.complete', **params)
    results.pop(compose_id, {})

    return True


def main():
    jobqueue = Queue('jobqueue')
    jobqueue.connect()

    while True:
        task = jobqueue.wait()

        task_data = task.data
        pos, num_images = task_data['pos']

        compose_details = task_data['compose']

        if pos == 1:
            session = init_model()
            compose_id = compose_details['id']
            compose_obj = session.query(ComposeDetails).filter_by(
                compose_id=compose_id).first()
            compose_obj.status = u'r'
            session.commit()


            params = copy.deepcopy(compose_details)
            params.update({'status': 'running'})
            publish_to_fedmsg(topic='compose.running', **params)

        result, running_status = auto_job(task_data)



if __name__ == '__main__':
    main()
