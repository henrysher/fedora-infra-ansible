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

"""

import os
import subprocess

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

{% if env == 'staging' %}
PKGDB_URL = 'https://admin.stg.fedoraproject.org/pkgdb'
{% else %}
PKGDB_URL = 'https://admin.fedoraproject.org/pkgdb'
{% endif %}

GIT_FOLDER = '/srv/git/rpms/'
MKBRANCH = '/usr/local/bin/mkbranch'
SETUP_PACKAGE = '/usr/local/bin/setup_git_package'

VERBOSE = False


class InternalError(Exception):
    pass


class ProcessError(InternalError):
    pass


def _invoke(program, args):
    '''Run a command and raise an exception if an error occurred.

    :arg program: The program to invoke
    :args: List of arguments to pass to the program

    raises ProcessError if there's a problem.
    '''
    cmdLine = [program]
    cmdLine.extend(args)
    if VERBOSE:
        print ' '.join(cmdLine)

    if VERBOSE:
        program = subprocess.Popen(
            cmdLine, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    else:
        program = subprocess.Popen(cmdLine, stderr=subprocess.STDOUT)

    retCode = program.wait()
    if retCode != 0:
        e = ProcessError()
        e.returnCode = retCode
        e.cmd = ' '.join(cmdLine)
        if VERBOSE:
            output = program.stdout.read()
            e.message = 'Error, "%s" returned %s: %s' % (
                e.cmd, e.returnCode, output)
            print e.message
        else:
            e.message = 'Error, "%s" returned %s' % (e.cmd, e.returnCode)
        raise e


def _create_branch(pkgname, branch):
    '''Create a specific branch for a package.

    :arg pkgname: Name of the package to branch
    :arg branch: Name of the branch to create

    '''
    if branch == 'master':
        print 'ERROR: Proudly refusing to create master branch. Invalid repo?'
        print 'INFO: Please check %s repo' % pkgname
        return

    branchpath = os.path.join(
        GIT_FOLDER, '%s.git' % pkgname, 'refs/heads', branch)
    if not os.path.exists(branchpath):
        try:
            _invoke(MKBRANCH, [branch, pkgname])
        except ProcessError, e:
            if e.returnCode == 255:
                # This is a warning, not an error
                return
            raise
        finally:
            fedmsg.publish(
                topic='branch',
                modname='git',
                msg=dict(
                    agent='pkgdb',
                    name=pkgname,
                    branch=branch,
                ),
            )
    elif VERBOSE:
            print 'Was asked to create branch %s of package %s, but it '\
                'already exists' % (pkgname, branch)


def pkgdb_pkg_branch():
    """ Queries pkgdb information about VCS and return a dictionnary of
    which branches are available for which packages.

    :return: a dict[pkg_name] = [pkg_branches]
    :rtype: dict
    """
    url = '%s/api/vcs' % PKGDB_URL
    req = requests.get(url, params={'format': 'json'})
    data = req.json()

    output = {}
    for pkg in data['packageAcls']:
        if pkg in output:
            if VERBOSE:
                print 'Strange package: %s, it is present twice in the ' \
                    'pkgdb output' % pkg
            output[pkg].updated(data['packageAcls'][pkg].keys())
        else:
            output[pkg] = set(data['packageAcls'][pkg].keys())

    return output


def get_git_branch(pkg):
    """ For the specified package name, check the local git and return the
    list of branches found.
    """
    git_folder = os.path.join(GIT_FOLDER, '%s.git' % pkg)
    if not os.path.exists(git_folder):
        print 'Could not find %s' % git_folder
        return set()

    head_folder = os.path.join(git_folder, 'refs', 'heads')
    return set(os.listdir(head_folder))


def branch_package(pkgname, branches):
    '''Create all the branches that are listed in the pkgdb for a package.

    :arg pkgname: The package to create branches for
    :arg branches: The branches to creates

    '''
    if VERBOSE:
        print 'Fixing package %s for branches %s' % (pkgname, branches)

    # Create the devel branch if necessary
    if not os.path.exists(
            os.path.join(GIT_FOLDER, '%s.git/refs/heads/master' % pkgname)):
        _invoke(SETUP_PACKAGE, [pkgname])
        if 'master' in branches:
            branches.remove('master')  # SETUP_PACKAGE creates master
            fedmsg.publish(
                topic='branch',
                modname='git',
                msg=dict(
                    agent='pkgdb',
                    name=pkgname,
                    branch='master',
                ),
             )

    # Create all the required branches for the package
    # Use the translated branch name until pkgdb falls inline
    for branch in branches:
        _create_branch(pkgname, branch)


def main():
    """ For each package found via pkgdb, check the local git for its
    branches and fix inconsistencies.
    """

    local_pkgs = set(os.listdir(GIT_FOLDER))
    local_pkgs = set([it.replace('.git', '') for it in local_pkgs])

    pkgdb_info = pkgdb_pkg_branch()

    pkgdb_pkgs = set(pkgdb_info.keys())

    ## Commented out as we keep the git of retired packages while they won't
    ## show up in the information retrieved from pkgdb.

    #if (local_pkgs - pkgdb_pkgs):
        #print 'Some packages are present locally but not on pkgdb:'
        #print ', '.join(sorted(local_pkgs - pkgdb_pkgs))

    if (pkgdb_pkgs - local_pkgs):
        print 'Some packages are present in pkgdb but not locally:'
        print ', '.join(sorted(pkgdb_pkgs - local_pkgs))

    tofix = set()
    for pkg in sorted(pkgdb_info):
        pkgdb_branches = pkgdb_info[pkg]
        git_branches = get_git_branch(pkg)
        diff = (pkgdb_branches - git_branches)
        if diff:
            print '%s missing: %s' % (pkg, ','.join(sorted(diff)))
            tofix.add(pkg)
            branch_package(pkg, diff)

    if tofix:
        print 'Packages fixed (%s): %s' % (
            len(tofix), ', '.join(sorted(tofix)))


if __name__ == '__main__':
    import sys
    sys.exit(main())
