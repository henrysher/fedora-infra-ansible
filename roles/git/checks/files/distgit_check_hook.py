#!/usr/bin/python

"""
This script goes through all the git repos in dist-git and adjust their
git post-receive hook so they are always as desired.

"""

import argparse
import os
import sys


_base_path = '/srv/git/repositories/'
_target_link = '/usr/share/git-core/post-receive-chained'
_target_link_forks = '/usr/share/git-core/post-receive-chained-forks'

namespaces = ['rpms', 'container', 'forks', 'modules', 'tests']


def parse_args():
    """ Parses the command line arguments. """
    parser = argparse.ArgumentParser(
        description='Check the git hook situation for all repos in dist-git')
    parser.add_argument(
        'target', nargs='?', help='git repo to check')
    parser.add_argument(
        '--namespace', default=None,
        help='Only check the git hooks, do not fix them')
    parser.add_argument(
        '--check', default=False, action="store_true",
        help='Only check the git hooks, do not fix them')

    return parser.parse_args()


def fix_link(hook, target_link):
    """ Remove the existing hook and replace it with a symlink to the desired
    one.
    """
    if os.path.exists(hook):
        os.unlink(hook)
    os.symlink(target_link, hook)


def is_valid_hook(hook, target_link):
    """ Simple utility function checking if the specified hook is valid. """
    output = True
    if not os.path.islink(hook):
        print('%s is not a symlink' % hook)
        output = False
    else:
        target = os.readlink(hook)
        if target != target_link:
            print('%s is not pointing to the expected target: %s' % (
                hook, target_link))
            output = False
    return output


def main():
    """ This is the main method of the program.
    It parses the command line arguments. If a specific repo was specified
    it will only check and adjust that repo.
    Otherwise, it will check and adjust all the repos.
    """

    args = parse_args()
    if args.target:
        # Update on repo
        print('Processing: %s' % args.target)

        target_link = _target_link
        if 'forks' in args.target:
            target_link = _target_link_forks

        path = os.path.join(_base_path, args.target)
        if not path.endswith('.git'):
            path += '.git'

        if not os.path.isdir(path):
            print('Git repo: %s not found on disk' % path)

        hook = os.path.join(path, 'hooks', 'post-receive')
        if not is_valid_hook(hook, target_link) and not args.check:
            fix_link(hook, target_link)

    else:
        # Check all repos
        for namespace in namespaces:
            target_link = _target_link
            if namespace == 'forks':
                target_link = _target_link_forks

            print('Processing: %s' % namespace)
            path = os.path.join(_base_path, namespace)
            if not os.path.isdir(path):
                continue

            for dirpath, dirnames, filenames in os.walk(path):
                # Don't go down the .git repos
                if dirpath.endswith('.git'):
                    continue

                for repo in dirnames:
                    repo_path = os.path.join(dirpath, repo)
                    if not repo_path.endswith('.git'):
                        continue
                    print('Checking %s' % repo_path)

                    hook = os.path.join(repo_path, 'hooks', 'post-receive')
                    if not is_valid_hook(hook, target_link) and not args.check:
                        fix_link(hook, target_link)


if __name__ == '__main__':
    sys.exit(main())
