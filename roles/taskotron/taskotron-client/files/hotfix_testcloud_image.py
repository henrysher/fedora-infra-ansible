#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright 2015, Red Hat, Inc.
# License: GPL-2.0+ <http://spdx.org/licenses/GPL-2.0+>
# See the LICENSE file for more details on Licensing

"""
Representation of a cloud image which can be used to boot instances
"""

import sys
import os
import subprocess
import re
import shutil
import logging

import requests

from . import config
from .exceptions import TestcloudImageError

config_data = config.get_config()

log = logging.getLogger('testcloud.image')


def list_images():
    """List the images currently downloaded and available on the system

    :returns: list of images currently available
    """

    image_dir = config_data.STORE_DIR
    images = os.listdir(image_dir)

    return images


def find_image(name, uri=None):
    """Find an image matching a given name and optionally, a uri

    :param name: name of the image to look for
    :param uri: source uri to use if the image is found

    :returns: :py:class:`Image` if an image is found, otherwise None
    """
    images = list_images()

    if name in images:
        if uri is None:
            uri = 'file://{}/{}'.format(config_data.STORE_DIR, name)
        return Image(uri)
    else:
        return None


class Image(object):
    """Handles base cloud images and prepares them for boot. This includes
    downloading images from remote systems (http, https supported) or copying
    from mounted local filesystems.
    """

    def __init__(self, uri):
        """Create a new Image object for Testcloud

        :param uri: URI for the image to be represented. this URI must be of a
            supported type (http, https, file)
        :raises TestcloudImageError: if the URI is not of a supported type or cannot be parsed
        """

        self.uri = uri

        uri_data = self._process_uri(uri)

        self.name = uri_data['name']
        self.uri_type = uri_data['type']

        if self.uri_type == 'file':
            self.remote_path = uri_data['path']
        else:
            self.remote_path = uri

        self.local_path = "{}/{}".format(config_data.STORE_DIR, self.name)

    def _process_uri(self, uri):
        """Process the URI given to find the type, path and imagename contained
        in that URI.

        :param uri: string URI to be processed
        :return: dictionary containing 'type', 'name' and 'path'
        :raise TestcloudImageError: if the URI is invalid or uses an unsupported transport
        """

        type_match = re.search(r'(http|https|file)://([\w\.\-/]+)', uri)

        if not type_match:
            raise TestcloudImageError('invalid uri: only http, https and file uris'
                                      ' are supported: {}'.format(uri))

        uri_type = type_match.group(1)
        uri_path = type_match.group(2)

        name_match = re.findall('([\w\.\-]+)', uri)

        if not name_match:
            raise TestcloudImageError('invalid uri: could not find image name: {}'.format(uri))

        image_name = name_match[-1]
        return {'type': uri_type, 'name': image_name, 'path': uri_path}

    def _download_remote_image(self, remote_url, local_path):
        """Download a remote image to the local system, outputting download
        progress as it's downloaded.

        :param remote_url: URL of the image
        :param local_path: local path (including filename) that the image
            will be downloaded to
        """

        u = requests.get(remote_url, stream=True)
        if u.status_code == 404:
            raise TestcloudImageError('Image not found at the given URL: {}'.format(self.uri))

        try:
            with open(local_path + ".part", 'wb') as f:
                file_size = int(u.headers['content-length'])

                log.info("Downloading {0} ({1} bytes)".format(self.name, file_size))
                bytes_downloaded = 0
                block_size = 4096

                while True:

                    try:

                        for data in u.iter_content(block_size):

                            bytes_downloaded += len(data)
                            f.write(data)
                            bytes_remaining = float(bytes_downloaded) / file_size
                            if config_data.DOWNLOAD_PROGRESS:
                                # TODO: Improve this progress indicator by making
                                # it more readable and user-friendly.
                                status = r"{0}/{1} [{2:.2%}]".format(bytes_downloaded,
                                                                     file_size,
                                                                     bytes_remaining)
                                status = status + chr(8) * (len(status) + 1)
                                sys.stdout.write(status)

                    except TypeError:
                        #  Rename the file since download has completed
                        os.rename(local_path + ".part", local_path)
                        log.info("Succeeded at downloading {0}".format(self.name))
                        break

        except OSError:
            log.error("Problem writing to {}.".format(config_data.PRISTINE))

    def _handle_file_url(self, source_path, dest_path, copy=True):
        if not os.path.exists(dest_path):
            if copy:
                shutil.copy(source_path, dest_path)
            else:
                subprocess.check_call(['ln', '-s', '-f', source_path, dest_path])

    def _adjust_image_selinux(self, image_path):
        """If SElinux is enabled on the system, change the context of that image
        file such that libguestfs and qemu can use it.

        :param image_path: path to the image to change the context of
        """

        selinux_active = subprocess.call(['selinuxenabled'])

        if selinux_active != 0:
            log.debug('SELinux not enabled, not changing context of'
                      'image {}'.format(image_path))
            return

        image_context = subprocess.call(['chcon',
                                         '-h',
                                         '-u', 'system_u',
                                         '-t', 'virt_content_t',
                                         image_path])
        if image_context == 0:
            log.debug('successfully changed SELinux context for '
                      'image {}'.format(image_path))
        else:
            log.error('Error while changing SELinux context on '
                      'image {}'.format(image_path))

    def prepare(self, copy=True):
        """Prepare the image for local use by either downloading the image from
        a remote location or copying/linking it into the image store from a locally
        mounted filesystem

        :param copy: if true image will be copied to backingstores else symlink is created
                     in backingstores instead of copying. Only for file:// type of urls.
        """

        log.debug("Local downloads will be stored in {}.".format(
            config_data.STORE_DIR))

        if self.uri_type == 'file':
            self._handle_file_url(self.remote_path, self.local_path, copy=copy)
        else:
            if not os.path.exists(self.local_path):
                self._download_remote_image(self.remote_path, self.local_path)

        self._adjust_image_selinux(self.local_path)

        return self.local_path

    def remove(self):
        """Remove the image from disk. This operation cannot be undone.
        """

        log.debug("removing image {}".format(self.local_path))
        os.remove(self.local_path)

    def destroy(self):
        '''A deprecated method. Please call :meth:`remove` instead.'''

        log.debug('DEPRECATED: destroy() method was deprecated. Please use remove()')
        self.remove()
