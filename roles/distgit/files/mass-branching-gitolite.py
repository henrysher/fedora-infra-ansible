#!/usr/bin/python

"""
This script is meant to be run in pkgs01.stg or pkgs02 (ie the dist-git
servers) and will be adding the specified new git branch to the gitolite
configuration so users can push to that branch.

Basically the script takes two inputs, the new branch name (for example
f28, f29, epel8....) and a file containing the namespace/name of all the
git repositories for which the gitolite configuration should be updated.

"""
from __future__ import print_function

import argparse
import os
import sys

_base_path = '/srv/git/'
_branch_from = 'master'


def _get_arguments():
    """ Set and retrieve the command line arguments. """
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'gitbranch',
        help='The new git branch to create')
    parser.add_argument(
        'inputfile',
        help='The input file listing the repositories to update')
    parser.add_argument(
        '--output',
        help='File where to write the new config (It may be a good idea to '
            'not over-write the current configuration file so you can diff '
            'the current with the new one')

    return parser.parse_args()


def main():
    """ Main function of the program. """

    print(
        'Did you stop the service `pagure_gitolite_worker` to ensure '
        'nothing touches this file while we work on it?')
    answer = raw_input('[y/N] ')
    if answer.lower() != 'y':
        print('You said no, so you know what to do ;-)')
        return 1

    args = _get_arguments()

    if not os.path.isfile(args.inputfile):
        print('%s does not appear to be a file' % args.inputfile)
        return 1

    repos = None
    with open(args.inputfile) as stream:
        repos = [row.strip() for row in stream]

    if not repos:
        print('%s appears to be empty' % args.inputfile)
        return 1

    config_file = os.path.join(
        _base_path, '.gitolite', 'conf', 'gitolite.conf')

    if not os.path.isfile(config_file):
        print('%s does not appear to be a file or to exist' % config_file)
        return 1

    config = None
    with open(config_file) as stream:
        config = [row.rstrip() for row in stream]

    if not data:
        print('%s appears to be empty' % config_file)
        return 1

    output = []
    process = False
    for row in config:
        if row.strip().startswith('repo '):
            name = row.strip().split()[-1]

            if name.startswith('rpm/'):
                name = 'rpms/%s' % name[4:]
            elif name.startswith('module/'):
                name = 'modules/%s' % name[7:]

            if name in repos:
                process = True
            else:
                process = False
        if process and row.strip().startswith('RWC   master ='):
            new_row = row
            new_row = new_row.replace(' master =', ' {} ='.format(args.branch), 1)
            output.append(new_row)
        output.append(row)

    print(
        'Done updating the config, writing the new content to {}'.format(
            args.output))

    with open(args.output, 'w') as stream:
        stream.write('\n'.join(output))

    print(
        'Now put the new configuration file in place (if it needs to be) '
        'then run `` sudo -u pagure HOME=/srv/git gitolite compile `` '
        'followed by `` sudo -u pagure HOME=/srv/git gitolite compile `` '
        'and finally, restart the `pagure_gitolite_worker` service.')

    return 0


if __name__ == '__main__':
    sys.exit(main())
