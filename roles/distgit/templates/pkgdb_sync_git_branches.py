#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

"""
This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


This script is able to query pkgdb and retrieve for all packages which active
branches should be there, browse all the git repos and find out which active
branches are missing.

It even goes one step further but actually adjusting the git repo by adding
the missing branches (or even the missing repo)

Here are the different steps of this script:

1/ Check the local repo in each namespace

2/ For each git repo, verifies if the new branch already exists otherwise
   create it

"""

import copy
import itertools
import multiprocessing.pool
import os
import subprocess
import time

import requests

import fedmsg

# Do some off-the-bat configuration of fedmsg.
#   1) since this is a one-off script and not a daemon, it needs to connect
#      to the fedmsg-relay process running on another node (or noone will
#      hear it)
#   2) its going to use the 'shell' certificate which only 'sysadmin' has
#      read access to.  Contrast that with the 'scm' certificate which
#      everyone in the 'packager' group has access to.

config = fedmsg.config.load_config([], None)
config['active'] = True
config['endpoints']['relay_inbound'] = config['relay_inbound']
fedmsg.init(name='relay_inbound', cert_prefix='shell', **config)

GIT_FOLDER = '/srv/git/repositories/'
NEW_BRANCH = 'f27'

MKBRANCH = '/usr/share/dist-git/mkbranch'
SETUP_PACKAGE = '/usr/share/dist-git/setup_git_package'

THREADS = 20
VERBOSE = False
TEST_ONLY = False


class InternalError(Exception):
    pass


class ProcessError(InternalError):
    pass


def _invoke(program, args, cwd=None):
    '''Run a command and raise an exception if an error occurred.

    :arg program: The program to invoke
    :args: List of arguments to pass to the program

    raises ProcessError if there's a problem.
    '''
    cmdLine = [program]
    cmdLine.extend(args)
    if VERBOSE:
        print ' '.join(cmdLine)
        print '  in', cwd

    program = subprocess.Popen(
        cmdLine, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, cwd=cwd)

    stdout, stderr = program.communicate()

    if program.returncode != 0:
        e = ProcessError()
        e.returnCode = program.returncode
        e.cmd = ' '.join(cmdLine)
        e.cwd = cwd
        e.message = 'Error, "%s" (in %r) returned %s\n  stdout: %s\n  stderr: %s' % (
            e.cmd, e.cwd, e.returnCode, stdout, stderr)
        print e.message
        raise e

    return stdout.strip()


def _create_branch(ns, pkgname, branch, existing_branches):
    '''Create a specific branch for a package.

    :arg pkgname: Name of the package to branch
    :arg branch: Name of the branch to create
    :arg existing_branches: A list of the branches that already exist locally.

    '''
    branch = branch.replace('*', '').strip()
    if branch == 'master':
        print 'ERROR: Proudly refusing to create master branch. Invalid repo?'
        print 'INFO: Please check %s repo' % os.path.join(ns, pkgname)
        return

    if branch in existing_branches:
       print 'ERROR: Refusing to create a branch %s that exists' % branch
       return

    try:
        if VERBOSE:
            print 'Creating branch: %s for package: %s' % (
                branch, os.path.join(ns, pkgname))

        if not TEST_ONLY:
            _invoke(MKBRANCH, [branch, os.path.join(ns, pkgname)])
            fedmsg.publish(
                topic='branch',
                modname='git',
                msg=dict(
                    agent='pkgdb',
                    name=pkgname,
                    branch=branch,
                    namespace=ns,
                ),
            )
    except ProcessError, e:
        if e.returnCode == 255:
            # This is a warning, not an error
            return
        raise


def get_git_branch(el):
    """ For the specified package name, check the local git and return the
    list of branches found.
    """
    ns, pkg = el
    git_folder = os.path.join(GIT_FOLDER, ns, '%s.git' % pkg)
    if not os.path.exists(git_folder):
        if VERBOSE:
            print 'Could not find %s' % git_folder
        return set()

    branches = [
       lclbranch.replace('*', '').strip()
       for lclbranch in _invoke('git', ['branch'], cwd=git_folder).split('\n')
    ]
    return set(branches)


def branch_package(ns, pkgname, requested_branches, existing_branches):
    '''Create all the branches that are listed in the pkgdb for a package.

    :arg ns: The namespace of the package
    :arg pkgname: The package to create branches for
    :arg requested_branches: The branches to creates
    :arg existing_branches: A list of existing local branches

    '''
    if VERBOSE:
        print 'Fixing package %s for branches %s' % (pkgname, requested_branches)

    # Create the devel branch if necessary
    new_place = os.path.join(GIT_FOLDER, ns, '%s.git' % pkgname)
    exists = os.path.exists(new_place)
    if not exists or 'master' not in existing_branches:
        if not TEST_ONLY:
            _invoke(SETUP_PACKAGE, [os.path.join(ns, pkgname)])
            if ns == 'rpms':
                old_place = os.path.join(GIT_FOLDER, '%s.git' % pkgname)
                if not os.path.exists(old_place):
                    os.symlink(new_place, old_place)
            # SETUP_PACKAGE creates master
            if 'master' in requested_branches:
                requested_branches.remove('master')
            fedmsg.publish(
                topic='branch',
                modname='git',
                msg=dict(
                    agent='pkgdb',
                    name=pkgname,
                    branch='master',
                    namespace=ns,
                ),
            )

    # Create all the required branches for the package
    # Use the translated branch name until pkgdb falls inline
    for branch in requested_branches:
        _create_branch(ns, pkgname, branch, existing_branches)


def main():
    """ For each package found via pkgdb, check the local git for its
    branches and fix inconsistencies.
    """

    for ns in ['rpms', 'modules', 'container']:

        local_pkgs = set(os.listdir(os.path.join(GIT_FOLDER, namespace)))
        local_pkgs = set([it.replace('.git', '') for it in local_pkgs])
        if VERBOSE:
            print "Found %i local packages (namespace: %s)" % (
                len(local_pkgs), ns)


        if VERBOSE:
            print "Finding the lists of local branches for local repos."
        start = time.time()
        if THREADS == 1:
            git_branch_lookup = map(get_git_branch,
                itertools.product([namespace], sorted(local_pkgs)))
        else:
            threadpool = multiprocessing.pool.ThreadPool(processes=THREADS)
            git_branch_lookup = threadpool.map(get_git_branch,
                itertools.product([namespace], sorted(local_pkgs)))

        # Zip that list of results up into a lookup dict.
        git_branch_lookup = dict(zip(sorted(local_pkgs), git_branch_lookup))

        if VERBOSE:
            print "Found all local git branches in %0.2fs" % (time.time() - start)

        tofix = set()
        for pkg in sorted(local_pkgs):
            git_branches = git_branch_lookup[pkg]
            diff = (git_branches - set([NEW_BRANCH]))
            if diff:
                print '%s missing: %s' % (pkg, ','.join(sorted(diff)))
                tofix.add(pkg)
                #branch_package(namespace, pkg, diff, git_branches)

        if tofix:
            print 'Packages fixed (%s): %s' % (
                len(tofix), ', '.join(sorted(tofix)))
        else:
            if VERBOSE:
                print 'Didn\'t find any packages to fix.'


if __name__ == '__main__':
    import sys
    sys.exit(main())
