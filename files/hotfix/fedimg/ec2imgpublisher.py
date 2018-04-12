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
# Authors:  Sayan Chowdhury <sayanchowdhury@fedoraproject.org>
#

import logging
log = logging.getLogger("fedmsg")

import re

from time import sleep

import fedimg.messenger

from fedimg.utils import external_run_command, get_item_from_regex
from fedimg.utils import get_image_name_from_ami_name
from fedimg.services.ec2.ec2base import EC2Base


class EC2ImagePublisher(EC2Base):
    """ Comment goes here """

    def __init__(self, **kwargs):
        defaults = {
            'access_key': None,
            'compose_id': None,
            'image_id': None,
            'image_name': 'Fedora-AMI',
            'image_description': 'Fedora AMI Description',
            'service': 'EC2',
            'region': None,
            'secret_key': None,
            'visibility': 'all',
            'push_notifications': False,
        }

        for (prop, default) in defaults.iteritems():
            setattr(self, prop, kwargs.get(prop, default))

    def _retry_till_image_is_public(self, image):
        """ Comment goes here """

        driver = self._connect()

        is_image_public = False
        while True:
            try:
                is_image_public = driver.ex_modify_image_attribute(
                    image,
                    {'LaunchPermission.Add.1.Group': 'all'})
            except Exception as e:
                if 'InvalidAMIID.Unavailable' in str(e):
                    # The copy isn't completed yet, so wait for 20 seconds
                    # more.
                    sleep(20)
                    continue
            break

        return is_image_public

    def _retry_till_snapshot_is_public(self, snapshot):

        driver = self._connect()

        while True:
            is_snapshot_public = driver.ex_modify_snapshot_attribute(
                snapshot,
                {'CreateVolumePermission.Add.1.Group': 'all'})

            if is_snapshot_public:
                break

        return is_snapshot_public


    def _retry_till_snapshot_is_available(self, image):

        driver = self._connect()
        while True:
            image = driver.get_image(image.id)
            snapshot_id = image.extra['block_device_mapping'][0]['ebs']['snapshot_id']

            if snapshot_id:
                break

        return snapshot_id

    def _generate_dummy_snapshot_object(self, snapshot_id):

        driver = self._connect()

        snapshot_obj = type('', (), {})()
        snapshot_obj.id = snapshot_id
        snapshot = driver.list_snapshots(snapshot=snapshot_obj)

        return snapshot

    def _retry_till_blk_mapping_is_available(self, image):

        while True:
            image = self._connect().get_image(image_id=image.id)
            blk_mapping = image.extra['block_device_mapping']

            if blk_mapping:
                return blk_mapping

    def get_snapshot_from_image(self, image):
        """ Comment goes here """
        if isinstance(image, str):
            image_id = image
            image = self._connect().get_image(image_id)

        blk_mapping = image.extra['block_device_mapping']
        if not blk_mapping:
            blk_mapping = self._retry_till_blk_mapping_is_available(image)

        snapshot_id = blk_mapping[0]['ebs']['snapshot_id']
        if snapshot_id is None:
            snapshot_id = self._retry_till_snapshot_is_available(image)

        snapshot = self._generate_dummy_snapshot_object(snapshot_id)[0]

        return snapshot

    def get_volume_type_from_image(self, image):
        if isinstance(image, str):
            image_id = image
            image = self._connect().get_image(image_id)

        blk_mapping = image.extra['block_device_mapping']
        if not blk_mapping:
            blk_mapping = self._retry_till_blk_mapping_is_available(image)

        return blk_mapping[0]['ebs']['volume_type']

    def get_virt_type_from_image(self, image):
        return 'hvm'

    def publish_images(self, region_image_mapping=None):
        """ Comment goes here """

        published_images = []
        if region_image_mapping is None:
            return published_images

        for region, image_id in region_image_mapping:
            self.set_region(region)

            log.info('Publish image (%s) in %s started' % (image_id, region))
            image = self._connect().get_image(image_id=image_id)
            is_image_public = self._retry_till_image_is_public(image)
            log.info('Publish image (%s) in %s completed' % (image_id, region))

            log.info('Publish snaphsot for image (%s) in %s started' % (image_id, region))
            snapshot = self.get_snapshot_from_image(image)
            log.info('Fetched snapshot for image (%s): %s' % (image_id, snapshot.id))
            is_snapshot_public = self._retry_till_snapshot_is_public(snapshot)
            log.info('Publish snaphsot for image (%s) in %s completed' % (image_id, region))

            volume_type = self.get_volume_type_from_image(image)
            virt_type = self.get_virt_type_from_image(image)

            if self.push_notifications:
                fedimg.messenger.notify(
                    topic='image.publish',
                    msg=dict(
                        image_name=image.name,
                        destination=self.region,
                        service=self.service,
                        compose=self.compose_id,
                        extra=dict(
                            id=image.id,
                            virt_type=virt_type,
                            vol_type=volume_type
                        )
                    )
                )

            published_images.append({
                'image_id': image.id,
                'is_image_public': is_image_public,
                'snapshot_id': snapshot.id,
                'is_snapshot_public': is_snapshot_public,
                'regions': self.region
            })

        return published_images

    def copy_images_to_regions(self, image_id=None, base_region=None, regions=None):
        """ Comment goes here """

        if (image_id is None) or (regions is None) or (base_region is None):
            return

        counter = 0
        copied_images = []

        self.set_region(base_region)
        image = self._connect().get_image(image_id=image_id)
        if not image:
            return []

        for region in regions:
            log.info('Copy %s to %s started' % (image_id, region))
            self.set_region(region)
            self.image_name = get_image_name_from_ami_name(image.name, region)

            while True:
                if counter > 0:
                    self.image_name = re.sub(
                        '\d(?!\d)',
                        lambda x: str(int(x.group(0))+1),
                        self.image_name
                    )
                try:
                    copied_image = self._connect().copy_image(
                        source_region=base_region,
                        image=image,
                        name=self.image_name,
                        description=self.image_description)

                    virt_type = image.extra['virtualization_type']
                    volume_type = image.extra['block_device_mapping'][0]['ebs']['volume_type']

                    if self.push_notifications:
                        fedimg.messenger.notify(
                            topic='image.copy',
                            msg=dict(
                                image_name=copied_image.name,
                                destination=self.region,
                                service=self.service,
                                compose_id=self.compose_id,
                                extra=dict(
                                    id=copied_image.id,
                                    virt_type=virt_type,
                                    vol_type=volume_type,
                                    source_image_id=image.id
                                )
                            )
                        )

                    log.info('Copy %s to %s is completed.' % (image_id, region))
                    copied_images.append({
                        'region': region,
                        'copied_image_id': copied_image.id
                    })
                    break

                except Exception as e:
                    log.info('Could not register '
                             'with name: %r' % self.image_name)
                    if 'InvalidAMIName.Duplicate' in str(e):
                        counter = counter + 1
                    else:
                        log.info('Failed')
                        break

        return copied_images

    def deprecate_images(self, image_ids=None, snapshot_perm='all'):
        raise NotImplementedError

    def delete_images(self, image_ids=None, snapshot_perm='all'):
        raise NotImplementedError
