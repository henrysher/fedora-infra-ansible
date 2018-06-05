"""
Copyright (c) 2018 Red Hat, Inc
All rights reserved.

This software may be modified and distributed under the terms
of the BSD license. See the LICENSE file for details.
"""
from copy import deepcopy
import re


# Negative regex used to exclude characters that are not allowed
# in naming a kubernetes resource
INVALID_KUBERNETES_NAME_CHARS = re.compile(r'[^a-z0-9\.-]+')


class FilterModule(object):
    def filters(self):
        return {'with_isolated_workers': do_with_isolated_workers}


def do_with_isolated_workers(reactor_configs):
    """Generate reactor configs for each worker cluster

    :param reactor_configs: list<dict>, each dict should contain a name and
    a data key. The value of name key is used to name the config map object
    and the value of data key is a reactor config

    :return: a new list of reactor configs that contains new reactor configs
    for each worker cluster in addition to the original reactor configs
    """
    all_configs = list(reactor_configs)

    for config in reactor_configs:
        clusters = config.get('data', {}).get('clusters', {})
        for arch, workers_info in clusters.items():
            for worker_info in workers_info:
                worker_info = deepcopy(worker_info)
                worker_info['enabled'] = True

                worker_config = deepcopy(config)

                name = _clean_kubernetes_name(config['name'] + '-' + worker_info['name'])
                worker_config['name'] = name

                worker_config['data']['clusters'] = {arch: [worker_info]}

                all_configs.append(worker_config)

    return all_configs


def _clean_kubernetes_name(name):
    name = name.lower()
    name = INVALID_KUBERNETES_NAME_CHARS.sub('-', name)
    return name
