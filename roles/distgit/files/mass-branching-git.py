#!/usr/bin/python

"""
This script is meant to be run in pkgs01.stg or pkgs02 (ie the dist-git
servers) and will be adding the specified new git branch to the specified
git repositories.

Basically the script takes two inputs, the new branch name (for example
f28, f29, epel8....) and a file containing the namespace/name of all the
git repositories for which that branch should be created.

"""
from __future__ import print_function

import argparse
import os
import subprocess
import sys

_base_path = '/srv/git/repositories'
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

    return parser.parse_args()


def create_git_branch(path, gitbranch):
    """ Create the specified git branch in the specified git repository. """
    cmd = ['git', 'branch', gitbranch, _branch_from]
    return subprocess.check_output(
        cmd, stderr=subprocess.STDOUT, shell=False, cwd=path)


def main():
    """ Main function of the program. """

    args = _get_arguments()

    if not os.path.isfile(args.inputfile):
        print('%s does not appear to be a file' % args.inputfile)
        return 1

    with open(args.inputfile) as stream:
        data = [row.strip() for row in stream]

    if not data:
        print('%s appears to be empty' % args.inputfile)
        return 1

    for entry in sorted(data):
        if entry.startswith('rpm/'):
            entry = 'rpms/%s' % entry[4:]
        elif entry.startswith('module/'):
            entry = 'modules/%s' % entry[7:]

        path = os.path.join(_base_path, '%s.git' % entry)
        print('Processing %s' % path)
        try:
            create_git_branch(path, args.gitbranch)
        except subprocess.CalledProcessError as err:
            print(
                '  ERROR: %s failed to branch, return code: %s\n      %s' % (
                    err.returncode, err.output))

    return 0


if __name__ == '__main__':
    sys.exit(main())
