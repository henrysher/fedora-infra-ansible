# This file is part of fedimg.
# Copyright (C) 2014-2017 Red Hat, Inc.
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
#           Ralph Bean <rbean@redhat.com>
#           Sayan Chowdhury <sayanchowdhury@fedoraproject.org>

"""
Utility functions for fedimg.
"""
import logging
_log = logging.getLogger(__name__)

import functools
import os
import re
import socket
import subprocess
import tempfile

import paramiko
from libcloud.compute.types import Provider
from libcloud.compute.providers import get_driver


def get_file_arch(file_name):
    """ Takes a file name (probably of a .raw.xz image file) and returns
    the suspected architecture of the contained image. If it doesn't look
    like a 32-bit or 64-bit image, None is returned. """
    if file_name.find('x86_64') != -1:
        return 'x86_64'
    else:
        return None


def get_rawxz_urls(location, images):
    """ Iterates through all the images metadata and returns the url of .raw.xz
    files.
    """
    rawxz_list = [f['path'] for f in images if f['path'].endswith('.raw.xz')]
    if not rawxz_list:
        return []

    return map((lambda path: '{}/{}'.format(location, path)), rawxz_list)


def get_virt_types_from_url(url):
    """ Takes a URL to a .raw.xz image file) and returns the suspected
        virtualization type that the image file should be registered as. """
    return ['hvm']


def region_to_driver(region):
    """ Takes a region name (ex. 'eu-west-1') and returns
    the appropriate libcloud provider value. """
    cls = get_driver(Provider.EC2)
    return functools.partial(cls, region=region)


def ssh_connection_works(username, ip, keypath):
    """ Returns True if an SSH connection can me made to `username`@`ip`. """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    works = False
    try:
        ssh.connect(ip, username=username,
                    key_filename=keypath)
        works = True
    except (paramiko.BadHostKeyException,
            paramiko.AuthenticationException,
            paramiko.SSHException, socket.error):
        pass
    ssh.close()
    return works


def get_value_from_dict(_dict, *keys):
    for key in keys:
        try:
            _dict = _dict[key]
        except KeyError:
            return None
    return _dict


def external_run_command(command):
    _log.debug("Starting the command: %r" % command)
    ret = subprocess.Popen(' '.join(command), stdin=subprocess.PIPE, shell=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           close_fds=True)
    out, err = ret.communicate()
    _log.debug("Finished executing the command: %r" % command)
    retcode = ret.returncode
    return out, err, retcode


def get_item_from_regex(output, regex):
    match = re.search(regex, output)
    if match is None:
        return ''
    else:
        return match.group(1)


def get_file_name_image(image_url):
    return image_url.split('/')[-1]


def get_source_from_image(image_url):
    tmpdir = tempfile.mkdtemp()
    file_name = get_file_name_image(image_url)
    file_path = os.path.join(tmpdir, file_name)

    _log.info("[PREP] Preparing temporary directory for download: %r" % tmpdir)
    output, error, retcode = external_run_command([
        'wget',
        image_url,
        '-P',
        tmpdir
    ])

    if retcode != 0:
        return ''

    return file_path


def get_volume_type_from_image(image, region):
    return image.extra['block_device_mapping'][0]['ebs']['volume_type']


def get_virt_type_from_image(image):
    return 'hvm'


def get_image_name_from_image(image_url, virt_type='', region='', respin='0',
                              volume_type=''):

    file_name = get_file_name_image(image_url)
    build_name = file_name.replace('.raw.xz', '')

    return '-'.join(
        [x for x in [build_name, virt_type, region, volume_type, respin] if x])


def get_image_name_from_ami_name(image_name, region):
    name_vt_region, volume_type, respin = image_name.rsplit('-', 2)
    name_vt = name_vt_region.rsplit('-', 3)[:-3][0]

    return '-'.join(
        [x for x in [name_vt, region, volume_type, respin] if x])


def get_image_name_from_ami_name_for_fedmsg(image_name):
    name_vt_region, volume_type, respin = image_name.rsplit('-', 2)
    image_name = name_vt_region.rsplit('-', 4)[:-4][0]

    return image_name
