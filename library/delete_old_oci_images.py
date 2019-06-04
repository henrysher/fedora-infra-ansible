#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# delete_old_oci_images.py - Ansible module that returns old images from a container registry
#
# Copyright (C) 2019 Red Hat, Inc.
# SPDX-License-Identifier: GPL-2.0+
#
DOCUMENTATION = """
---
author:
  - "Clément Verna <cverna@fedoraproject.org>"
module: delete_old_oci_images
short_description: Check for old OCI images in a registry and delete them.
description:
  - Look for OCI images tag in a registry that are older than "days".
  - Delete the OCI images tag from these old images.
options:
  registry:
    description:
      - URL of the registry to use.
    required: False
    default: "https://candidate-registry.fedoraproject.org"
  days:
    description:
      - Number of days used to check if we want to delete or keep and image tag.
    required: True
  username:
    description:
      - Username uses to login against the registry.
    required: True
  password:
    description:
      - Password used to login against the registry.
    required: True
"""

EXAMPLES = """
- delete_old_oci_images:
    days: 30
    username: "{{ secret_username }}"
    password: "{{ secret_password }}"

- delete_old_oci_images:
    registry: "https://candidate-registry.stg.fedoraproject.org"
    days: 10
    username: "{{ secret_stg_username }}"
    password: "{{ secret_stg_password }}"
"""

from ansible.module_utils.basic import *
from datetime import datetime, timedelta


def main():
    """
    Ensure that images that are at least 'days' old are deleted
    from the registry.
    """
    module_args = dict(
        registry=dict(
            type="str", required=False, default="https://candidate-registry.fedoraproject.org"
        ),
        days=dict(type="int", required=True),
        username=dict(type="str", required=True),
        password=dict(type="str", required=True, no_log=True),
    )

    module = AnsibleModule(argument_spec=module_args, supports_check_mode=True)

    try:
        import requests

        headers = {
            "Accept": "application/vnd.docker.distribution.manifest.v2+json, application/vnd.oci.image.index.v1+json, application/vnd.oci.image.manifest.v1+json"
        }
    except ImportError:
        module.fail_json(msg="the requests python module not found on the target system")

    result = {"failed": False, "stdout_lines": []}
    check_mode = module.check_mode
    registry = module.params["registry"]
    days = module.params["days"]
    username = module.params["username"]
    password = module.params["password"]

    # Prepare the requests session
    s = requests.Session()

    # Retry in case of failed connection
    adapter = requests.adapters.HTTPAdapter(max_retries=5)
    s.mount("http://", adapter)
    s.mount("https://", adapter)

    # Set the correct headers
    s.headers.update(headers)
    # Set the authentication
    s.auth = (username, password)

    # Get the list of repositories in the registry (Assume we have less than 500)
    resp = s.get("{}/v2/_catalog?n=500".format(registry))
    if not resp.ok:
        result["stdout_lines"].append("Failed to get the list of images on the {}".format(registry))
        result["failed"] = True
        module.fail_json(**result)

    repositories = resp.json().get("repositories")

    # For each repository found get all the tags
    for repo in repositories:
        resp = s.get("{}/v2/{}/tags/list".format(registry, repo))
        if not resp.ok:
            result["stdout_lines"].append("Failed to get the list of tags for {}".format(repo))

        # For each tag get the maninfest
        image = resp.json()
        for tag in image["tags"]:
            resp = s.get("{}/v2/{}/manifests/{}".format(registry, repo, tag))
            if not resp.ok:
                result["stdout_lines"].append(
                    "Failed to get the manifest for {}:{}".format(repo, tag)
                )

            # For each tag get the blobs
            config = resp.json().get("config")
            if config is not None:
                digest = config.get("digest")
                resp = s.get("{}/v2/{}/blobs/{}".format(registry, repo, digest))
                if not resp.ok:
                    result["stdout_lines"].append(
                        "Failed to get the blob for {}:{}".format(repo, digest)
                    )

                # Find when a blob was created
                age = resp.json().get("created")
                # Check if the blob is older than "days"
                if datetime.strptime(age[:10], "%Y-%m-%d") <= datetime.now() - timedelta(days=days):
                    if not check_mode:
                        # Delete the tag
                        resp = s.get("{}/v2/{}/manifests/{}".format(registry, repo, tag))
                        digest = resp.headers["Docker-Content-Digest"]
                        resp = s.delete("{}/v2/{}/manifests/{}".format(registry, repo, digest))
                        if resp.ok:
                            result["changed"] = True
                        else:
                            module.fail_json(
                                msg="Failed to delete {}:{} with the error : {}".format(
                                    repo, tag, resp.text
                                ),
                                failed=True,
                            )
                    else:
                        result["stdout_lines"].append("would delete {}:{}".format(repo, tag))
                        result["changed"] = True

    module.exit_json(**result)


main()
