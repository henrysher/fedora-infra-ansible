# Check if we're running on RHEL6 and disable
# `mock --new-chroot` and `rpm-ostree --workdir-tmpfs`
import platform
dist = platform.dist()
rhel6 = dist[0] == 'redhat' and int(float(dist[1])) == 6

config = dict(
    releases={
        'f21-updates': {
            'name': 'f21-updates',
            'repo': 'updates',
            'version': '21',
            'arch': 'x86_64',

            # OSTree treefile configuration
            # https://github.com/projectatomic/rpm-ostree/blob/master/doc/treefile.md
            'tree': 'docker-host',
            'treefile': {
                'include': 'fedora-atomic-docker-host.json',
                'ref': 'fedora-atomic/f21/x86_64/updates/docker-host',
                'repos': ['fedora-21', 'updates'],
            },

            # The name of the mock container to build and maintain
            'mock': 'fedora-21-updates-x86_64',

            # The git branch to use in the `git_repo` for the parent
            # treefile & repo configurations
            'git_branch': 'f21',

            # Add or overwrite yum repository name:urls. This lets you
            # compose trees against your own repositories.
            'repos': {},
        },

        'f21-updates-testing': {
            'name': 'f21-updates-testing',
            'repo': 'updates-testing',
            'version': '21',
            'arch': 'x86_64',
            'tree': 'docker-host',
            'treefile': {
                'include': 'fedora-atomic-docker-host.json',
                'ref': 'fedora-atomic/f21/x86_64/updates-testing/docker-host',
                'repos': ['fedora-21', 'updates', 'updates-testing'],
            },
            'git_branch': 'f21',
            'mock': 'fedora-21-updates-testing-x86_64',
            'repos': {},
        },
    },

    # Package repositories to use in the mock container and ostree compose
    repos={
        'updates': 'https://dl.fedoraproject.org/pub/fedora/linux/updates/{version}/{arch}/',
        'updates-testing': 'https://dl.fedoraproject.org/pub/fedora/linux/updates/testing/{version}/{arch}/',
    },

    # Output directories
    work_dir='/srv/fedora-atomic',
    prod_dir='{work_dir}/production',
    canonical_dir='{prod_dir}/{version}/{arch}/{repo}/{tree}',
    output_dir='{work_dir}/{version}/{arch}/{repo}/{tree}',
    log_dir='{work_dir}/logs/{version}/{arch}/{repo}/{tree}',

    # The git repo containing our parent treefiles and yum repos
    git_repo='https://git.fedorahosted.org/git/fedora-atomic.git',
    git_cache='{work_dir}/fedora-atomic.git',

    # Mock command
    mock_cmd='/usr/bin/mock%s-r {mock}' % (rhel6 and ' ' or ' --new-chroot '),

    # OSTree commands
    ostree_init='/usr/bin/ostree --repo={output_dir} init --mode=archive-z2',
    ostree_compose='/usr/bin/rpm-ostree compose tree' +
            (rhel6 and ' ' or ' --workdir-tmpfs ') + '--repo={output_dir} %s',
    ostree_summary='/usr/bin/ostree --repo={output_dir} summary --update',

    # rsync commands
    rsync_in_objs='/usr/bin/rsync -rvp --ignore-existing {canonical_dir}/objects/ {output_dir}/objects/',
    rsync_in_rest='/usr/bin/rsync -rvp --exclude=objects/ {canonical_dir}/ {output_dir}/',
    rsync_out_objs='/usr/bin/rsync -rvp --ignore-existing {output_dir}/objects/ {canonical_dir}/objects/',
    rsync_out_rest='/usr/bin/rsync -rvp --exclude=objects/ {output_dir}/ {canonical_dir}/',

    map_to_release=('work_dir', 'prod_dir', 'output_dir', 'log_dir',
                    'git_repo', 'git_cache', 'mock_cmd', 'ostree_init',
                    'ostree_compose', 'ostree_summary', 'canonical_dir',
                    'repos', 'rsync_in_1', 'rsync_in_2', 'rsync_out_1',
                    'rsync_out_2'),
)

# Map and expand certain variables to each release
for key in config.get('map_to_release', []):
    for name, release in config['releases'].items():
        if isinstance(config[key], dict):
            release[key] = {}
            for k, v in config[key].items():
                release[key][k] = v.format(**release)
        else:
            release[key] = config[key].format(**release)
