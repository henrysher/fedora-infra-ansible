#!/usr/bin/python3
# Regenerate dist repos that are missing or will be deleted soon.
# Author: Mikolaj Izdebski <mizdebsk@fedoraproject.org>


# config: max age of dist repo in seconds before it is regenerated
# TODO: move it to config file
max_age = 5*24*60*60


import koji

conf_location = '/etc/fedmsg.d/tag2distrepo.py'
with open(conf_location) as f:
    code = compile(f.read(), conf_location, 'exec')
vars = {}
exec(code, vars)
config = vars['config']
#assert config['tag2distrepo.enabled']

for koji_env in config['tag2distrepo.tags'].keys():
    koji_config = config['tag2distrepo.tags'][koji_env]
    koji_session = koji.ClientSession(koji_config['url'], koji_config['options'])
    assert koji_config['authmethod'] == 'kerberos'
    kwargs = {}
    for opt in ('principal', 'keytab', 'ccache'):
        if opt in koji_config:
            kwargs[opt] = koji_config[opt]
    koji_session.krb_login(**kwargs)
    event = koji_session.getLastEvent()

    tags = sorted(koji_config['tags'].keys())
    koji_session.multicall = True
    for tag in tags:
        koji_session.getRepo(tag, event=event['id'], dist=True)
    repos = koji_session.multiCall(strict=True)

    koji_session.multicall = True
    for tag, [repo] in zip(tags, repos):
        if not repo:
            print('Tag {}: dist repo not available'.format(tag))
        elif repo['state'] == koji.REPO_INIT:
            print('Tag {}: dist repo is being generated right now'.format(tag))
            continue
        elif repo['state'] in (koji.REPO_READY, koji.REPO_EXPIRED):
            age = event['ts'] - repo['create_ts']
            if age > max_age:
                print('Tag {}: dist repo is present, but older than defined threshold (age: {} seconds)'.format(tag, age))
            else:
                print('Tag {}: dist repo is present and it is fresh enough (age: {} seconds)'.format(tag, age))
                continue
        elif repo['state'] == koji.REPO_DELETED:
            print('Tag {}: dist repo was already deleted from disk'.format(tag))
        elif repo['state'] == koji.REPO_PROBLEM:
            print('Tag {}: dist repo is broken'.format(tag))
        else:
            assert None
        koji_session.getTag(tag)
    tag_infos = koji_session.multiCall(strict=True)

    koji_session.multicall = True
    for [tag_info] in tag_infos:
        opts = {
            'arch': (tag_info['arches'] or '').split(),
            'comp': None,
            'delta': [],
            'event': None,
            'inherit': False,
            'latest': True,
            'multilib': False,
            'skip_missing_signatures': False,
            'allow_missing_signatures': False
        }

        keys = koji_config['tags'][tag_info['name']]
        koji_session.distRepo(tag_info['id'], keys, **opts)
    task_ids = koji_session.multiCall(strict=True)
        
    for [tag_info], [task_id] in zip(tag_infos, task_ids):
        print('Tag {}: new dist-repo requested (task ID: {})'.format(tag_info['name'], task_id))
