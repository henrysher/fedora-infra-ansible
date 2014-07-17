#!/usr/bin/python -t
# Author: Toshio Kuratomi
# Copyright: 2007-2008 Red Hat Software
# License: GPLv2
# This needs a proper license and copyright here
__version__ = '0.3'

import sys
import os
import optparse

import subprocess

import fedmsg

# Do some off-the-bat configuration of fedmsg.
#   1) since this is a one-off script and not a daemon, it needs to connect to
#      the fedmsg-relay process running on another node (or noone will hear it)
#   2) its going to use the 'shell' certificate which only 'sysadmin' has read
#      access to.  Contrast that with the 'scm' certificate which everyone in
#      the 'packager' group has access to.
config = fedmsg.config.load_config([], None)
config['active'] = True
config['endpoints']['relay_inbound'] = config['relay_inbound']
fedmsg.init(name='relay_inbound', cert_prefix='shell', **config)

from fedora.client import FedoraServiceError
from pkgdb2client import PkgDB

GITDIR='/srv/git/rpms'
BASEURL = os.environ.get('PACKAGEDBURL') or 'https://admin.fedoraproject.org/pkgdb/'
MKBRANCH='/usr/local/bin/mkbranch'
SETUP_PACKAGE='/usr/local/bin/setup_git_package'
BRANCHES = {'el4': 'master', 'el5': 'master', 'el6': 'master', 'epel7': 'f19',
        'olpc2': 'f7',
        'olpc3': 'f11',
        'master': None,
        'fc6': 'master',
        'f7': 'master',
        'f8': 'master',
        'f9': 'master',
        'f10': 'master',
        'f11': 'master',
        'f12': 'master',
        'f13': 'master', 'f14': 'master',
        'f15': 'master', 'f16': 'master',
        'f17': 'master', 'f18': 'master',
        'f19': 'master', 'f20': 'master'
        }

# The branch names we get out of pkgdb have to be translated to git
GITBRANCHES = {'el4': 'el4', 'el5': 'el5', 'el6': 'el6', 'epel7': 'epel7',
               'OLPC-2': 'olpc2',
               'FC-6': 'fc6', 'F-7': 'f7', 'F-8': 'f8', 'F-9': 'f9',
               'F-10': 'f10', 'OLPC-3': 'olpc3',
               'F-11': 'f11', 'F-12': 'f12', 'F-13': 'f13', 'f14': 'f14', 'f15': 'f15', 'f16': 'f16', 'f17': 'f17',
               'f18': 'f18', 'f19': 'f19', 'f20': 'f20',
               'devel': 'master'}

# The branch options we get from the CLI have to be translated to pkgdb
BRANCHBYGIT = dict([(v, k) for (k, v) in GITBRANCHES.iteritems()])

class InternalError(Exception):
    pass

class PackageDBError(InternalError):
    pass

class ProcessError(InternalError):
    pass

class ArgumentsError(InternalError):
    pass

class InvalidBranchError(PackageDBError):
    pass

class PackageDBClient(PkgDB):
    def __init__(self, baseURL):
        '''Initialize the connection.

        Args:
        :baseURL: URL from which the packageDB is accessed
        '''
        # We're only performing read operations so we don't need a username
        super(PackageDBClient, self).__init__(baseURL)

    def get_package_branches(self, pkgname):
        '''Return the branches to which a package belongs.

        Args:
        :pkgname: The package to retrieve branch information about
        '''

        data = self.get_package(pkgname)
        return map(lambda x: x['collection']['branchname'], data['packages'])
        
    def get_package_list(self, branchName):
        '''Retrieve all the packages in a specific branch.

        Args:
        :branchName: to return the packages for
        '''
        pkgs = map(lambda l: l['name'], self.get_packages('*', branchName, page=0)['packages'])
        return pkgs

class Brancher(object):
    ''' Make branches in the GIT Repository.'''

    def __init__(self, pkgdburl, cache, verbose):
        # Connect to the package database
        self.verbose = verbose
        self.client = PackageDBClient(BASEURL)

    def _invoke(self, program, args):
        '''Run a command and raise an exception if an error occurred.
        
        Args:
        :program: The program to invoke
        :args: List of arguments to pass to the program

        raises ProcessError if there's a problem.
        '''
        cmdLine = [program]
        cmdLine.extend(args)
        print ' '.join(cmdLine)

        stdoutfd = subprocess.PIPE
        if self.verbose:
            program = subprocess.Popen(cmdLine, stderr=subprocess.STDOUT)
        else:
            program = subprocess.Popen(cmdLine, stdout=subprocess.PIPE,
                     stderr=subprocess.STDOUT)
        retCode = program.wait()
        if retCode != 0:
            e = ProcessError()
            e.returnCode = retCode
            e.cmd = ' '.join(cmdLine)
            if self.verbose:
                output = program.stdout.read()
                e.message = 'Error, "%s" returned %s: %s' % (e.cmd, e.returnCode, output)
            else:
                e.message = 'Error, "%s" returned %s' % (e.cmd, e.returnCode)
            raise e

    def _create_branch(self, pkgname, branch):
        '''Create a specific branch for a package.
        
        Args:
        :pkgname: Name of the package to branch
        :branch: Name of the branch to create

        raises InvalidBranchError if a branchname is unknown.

        Will ignore a branch which is EOL.
        '''
        try:
            branchFrom = '%s/master' % BRANCHES[branch]
        except KeyError:
            raise InvalidBranchError(
                    'PackageDB returned an invalid branch %s for %s' %
                    (branch, pkgname))

        # Add the master to the branch
        # No longer add this after the new branching setup.
        #branch = '%s/master' % branch
        # If branchFrom is None, this is an EOL release
        # If the directory already exists, no need to invoke mkbranch
        if branchFrom:
            # Fall back to branching from master.
            frombranchpath = os.path.join(GITDIR, '%s.git' % pkgname,
                                          'refs/heads', branchFrom)
            if not os.path.exists(frombranchpath):
                branchFrom = 'master'

            branchpath = os.path.join(GITDIR, '%s.git' % pkgname,
                                      'refs/heads', branch)
            if not os.path.exists(branchpath):
                try:
                    self._invoke(MKBRANCH, ['-s', branchFrom, branch, pkgname])
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
                            agent=os.getlogin(),
                            name=pkgname,
                            branch=branch,
                        ),
                    )

    def branch_package(self, pkgname):
        '''Create all the branches that are listed in the pkgdb for a package.

        Args:
        :pkgname: The package to create branches for

        Note: this will ignore branches which are EOL.

        raises PackageDBError if the package is not present in the Package
        Database.
        '''
        # Retrieve branch information
        try:
            branches = self.client.get_package_branches(pkgname)
        except FedoraServiceError, e:
            raise PackageDBError(
                    'Unable to retrieve information about %s: %s' %
                    (pkgname, str(e)))

        # Create the devel branch if necessary
        if not os.path.exists(os.path.join(GITDIR,
                                           '%s.git' % pkgname)):
            self._invoke(SETUP_PACKAGE, [pkgname])
        # Create all the required branches for the package
        # Use the translated branch name until pkgdb falls inline
        for branch in branches:
            if branch == 'devel':
                continue
            if not branch in GITBRANCHES.keys():
                print 'Skipping unknown branch %s' % branch
                continue
            self._create_branch(pkgname, GITBRANCHES[branch])

    def mass_branch(self, branchName):
        '''Make sure all packages listed for a specific branch in the PackageDB
        have a CVS branch.
        
        Args:
        :branchName: The branch to ensure.
        '''
        fedmsg.publish(
            topic='mass_branch.start',
            modname='git',
            msg=dict(agent=os.getlogin()),
        )
        # Retrieve all the packages in this branch
        pkglist = self.client.get_package_list(branchName)
        pkglist.sort()
        for pkg in pkglist:
            # Create a branch for this release for each of them
            # Use the translated branch name until pkgdb falls inline
            self._create_branch(pkg, GITBRANCHES[branchName])

        fedmsg.publish(
            topic='mass_branch.complete',
            modname='git',
            msg=dict(agent=os.getlogin()),
        )
        
def parse_commands():
    parser = optparse.OptionParser(version=__version__, usage='''pkgdb2branch.py [options] PACKAGENAME [packagename, ...] [-]
       pkgdb2branch.py [options] --branchfor BRANCH

pkgdb2branch reads package information from the packagedb and creates branches
on the git server based on what branches are listed there.  pkgdb2branch can
read the list of packages from stdin if you specify '-' as an argument.

pkgdb2branch has two modes of operation.  In the first mode, you specify which
packages you want to branch.  This mode is more efficient for a small number
of packages.

In the second mode, pkgdb2branch will find every package lacking a BRANCH and
will create one if the pkgdb says it's needed.  This mode is very efficient for
mass branching.  This implies --cache-branches.

For those with a moderate number of packages, using a list of packages and
--cache-branches may be fastest.''')
    parser.add_option('-b', '--branch-for',
        dest='branchFor',
        action='store',
        help='Make sure all the packages have been branched for BRANCHFOR. Implies -c.')
    parser.add_option('-c', '--cache-branches',
        dest='enableCache',
        action='store_true',
        help='Download a complete cache of packages')
    parser.add_option('--verbose',
        dest='verbose',
        action='store_true',
        help='Enable verbose output')
    (opts, args) = parser.parse_args()

    if opts.branchFor:
        if args:
            raise ArgumentsError('Cannot specify packages with --branchFor')
        opts.enableCache = True

    if '-' in args:
        opts.fromStdin = True
        del (args[args.index('-')])
    else:
        opts.fromStdin = False

    if not (args or opts.fromStdin or opts.branchFor):
        raise ArgumentsError('You must list packages to operate on')

    return opts, args
    
if __name__ == '__main__':
    try:
        options, packages = parse_commands()
    except ArgumentsError, e:
        print e
        sys.exit(1)

    branchedPackages, unbranchedPackages = [], []
    brancher = Brancher(BASEURL, options.enableCache, options.verbose)
    fedmsg.publish(
        topic='pkgdb2branch.start',
        modname='git',
        msg=dict(agent=os.getlogin()),
    )

    if options.branchFor:
        try:
            unbranchedPackages = \
                        brancher.mass_branch(BRANCHBYGIT[options.branchFor])
        except PackageDBError, e:
            print 'Unable contact the PackageDB. Error: %s' % str(e)
            sys.exit(1)
    else:
        # Process packages specified on the cmdline
        for pkgname in packages:
            try:
                brancher.branch_package(pkgname)
                branchedPackages.append(pkgname)
            except InternalError, e:
                print str(e)
                unbranchedPackages.append(pkgname)

        # Process packages from stdin
        if options.fromStdin:
            for pkgname in sys.stdin:
                pkgname = pkgname.strip()
                try:
                    brancher.branch_package(pkgname)
                    branchedPackages.append(pkgname)
                except InternalError, e:
                    print str(e)
                    unbranchedPackages.append(pkgname)

    fedmsg.publish(
        topic='pkgdb2branch.complete',
        modname='git',
        msg=dict(
            agent=os.getlogin(),
            branchedPackages=branchedPackages,
            unbranchedPackages=unbranchedPackages,
        ),
    )

    if unbranchedPackages:
        print 'The following packages were unbranched:'
        print '\n'.join(unbranchedPackages)
        sys.exit(100)

    sys.exit(0)
