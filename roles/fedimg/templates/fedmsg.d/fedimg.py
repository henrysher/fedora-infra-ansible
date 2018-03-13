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
#           Ralph Bean <rbean@redhat.com>
#           Sayan Chowdhury <sayan@redhat.com>
#

{% if env == 'staging' %}
config = {
    'fedimgconsumer.dev.enabled': False,
    'fedimgconsumer.prod.enabled': False,
    'fedimgconsumer.stg.enabled': True,
}
{% else %}
config = {
    'fedimgconsumer': True,
}
{% endif %}
