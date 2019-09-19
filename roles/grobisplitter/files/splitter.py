#!/bin/python3

# Import libraries needed for application to work

import argparse
import shutil
import gi
import gzip
import librepo
import hawkey
import tempfile
import os
import subprocess
import sys

# Look for a specific version of modulemd. The 1.x series does not
# have the tools we need.
try:
    gi.require_version('Modulemd', '2.0')
    from gi.repository import Modulemd
except:
    print("We require newer vesions of modulemd than installed..")
    sys.exit(0)
    
mmd = Modulemd

# This code is from Stephen Gallagher to make my other caveman code
# less icky.
def _get_latest_streams (mymod, stream):
    """
    Routine takes modulemd object and a stream name.
    Finds the lates stream from that and returns that as a stream
    object. 
    """
    all_streams = mymod.search_streams(stream, 0)
    latest_streams = mymod.search_streams(stream,
                                          all_streams[0].props.version) 
    
    return latest_streams
    
def _get_repoinfo(directory):
    """
    A function which goes into the given directory and sets up the
    needed data for the repository using librepo.
    Returns the LRR_YUM_REPO
    """
    with tempfile.TemporaryDirectory(prefix='elsplit_librepo_') as lrodir:
        h = librepo.Handle()
        h.setopt(librepo.LRO_URLS, ["file://%s" % directory])
        h.setopt(librepo.LRO_REPOTYPE, librepo.LR_YUMREPO)
        h.setopt(librepo.LRO_DESTDIR, lrodir)
        h.setopt(librepo.LRO_LOCAL, True)
        h.setopt(librepo.LRO_IGNOREMISSING, False)
        r = h.perform()
        return r.getinfo(librepo.LRR_YUM_REPO)

def _get_hawkey_sack(repo_info):
    """
    A function to pull in the repository sack from hawkey.
    Returns the sack.
    """
    hk_repo = hawkey.Repo("")
    hk_repo.filelists_fn = repo_info["filelists"]
    hk_repo.primary_fn = repo_info["primary"]
    hk_repo.repomd_fn = repo_info["repomd"]

    primary_sack = hawkey.Sack()
    primary_sack.load_repo(hk_repo, build_cache=False)
    
    return primary_sack

def _get_filelist(package_sack):
    """
    Determine the file locations of all packages in the sack. Use the
    package-name-epoch-version-release-arch as the key.
    Returns a dictionary.
    """
    pkg_list = {}
    for pkg in hawkey.Query(package_sack):
        nevr="%s-%s:%s-%s.%s"% (pkg.name,pkg.epoch,pkg.version,pkg.release,pkg.arch)
        pkg_list[nevr] = pkg.location
    return pkg_list

def _parse_repository_non_modular(package_sack, repo_info, modpkgset):
    """
    Simple routine to go through a repo, and figure out which packages
    are not in any module. Add the file locations for those packages
    so we can link to them.
    Returns a set of file locations.
    """
    sack = package_sack
    pkgs = set()

    for pkg in hawkey.Query(sack):
        if pkg.location in modpkgset:
            continue
        pkgs.add(pkg.location)
    return pkgs

def _parse_repository_modular(repo_info,package_sack):
    """
    Returns a dictionary of packages indexed by the modules they are
    contained in.
    """
    cts = {}
    idx = mmd.ModuleIndex()
    with gzip.GzipFile(filename=repo_info['modules'], mode='r') as gzf:
        mmdcts = gzf.read().decode('utf-8')
        res, failures = idx.update_from_string(mmdcts, True)
        if len(failures) != 0:
            raise Exception("YAML FAILURE: FAILURES: %s" % failures)
        if not res:
            raise Exception("YAML FAILURE: res != True")

    pkgs_list = _get_filelist(package_sack)
    idx.upgrade_streams(2)
    for modname in idx.get_module_names():
        mod = idx.get_module(modname)
        for stream in mod.get_all_streams():
            templ = list()
            for pkg in stream.get_rpm_artifacts():
                if pkg in pkgs_list:
                    templ.append(pkgs_list[pkg])
                else:
                    continue
            cts[stream.get_NSVCA()] = templ
                
    return cts


def _get_modular_pkgset(mod):
    """
    Takes a module and goes through the moduleset to determine which
    packages are inside it. 
    Returns a list of packages
    """
    pkgs = set()

    for modcts in mod.values():
        for pkg in modcts:
            pkgs.add(pkg)

    return list(pkgs)

def _perform_action(src, dst, action):
    """
    Performs either a copy, hardlink or symlink of the file src to the
    file destination.
    Returns None
    """
    if action == 'copy':
        try:
            shutil.copy(src, dst)
        except FileNotFoundError:
            # Missing files are acceptable: they're already checked before
            # this by validate_filenames.
            pass
    elif action == 'hardlink':
        os.link(src, dst)
    elif action == 'symlink':
        os.symlink(src, dst)

def validate_filenames(directory, repoinfo):
    """
    Take a directory and repository information. Test each file in
    repository to exist in said module. This stops us when dealing
    with broken repositories or missing modules.
    Returns True if no problems found. False otherwise.
    """
    isok = True
    for modname in repoinfo:
        for pkg in repoinfo[modname]:
            if not os.path.exists(os.path.join(directory, pkg)):
                isok = False
                print("Path %s from mod %s did not exist" % (pkg, modname))
    return isok


def get_default_modules(directory):
    """
    Work through the list of modules and come up with a default set of
    modules which would be the minimum to output. 
    Returns a set of modules 
    """
    directory = os.path.abspath(directory)
    repo_info = _get_repoinfo(directory)

    provides = set()
    contents = set()
    if 'modules' not in repo_info:
        return contents
    idx = mmd.ModuleIndex()
    with gzip.GzipFile(filename=repo_info['modules'], mode='r') as gzf:
        mmdcts = gzf.read().decode('utf-8')
        res, failures = idx.update_from_string(mmdcts, True)
        if len(failures) != 0:
            raise Exception("YAML FAILURE: FAILURES: %s" % failures)
        if not res:
            raise Exception("YAML FAILURE: res != True")

    idx.upgrade_streams(2)

    # OK this is cave-man no-sleep programming. I expect there is a
    # better way to do this that would be a lot better. However after
    # a long long day.. this is what I have.

    # First we oo through the default streams and create a set of
    # provides that we can check against later.
    for modname in idx.get_default_streams():
        mod = idx.get_module(modname)
        # Get the default streams and loop through them.
        stream_set = mod.get_streams_by_stream_name(
            mod.get_defaults().get_default_stream())
        for stream in stream_set:
            tempstr = "%s:%s" % (stream.props.module_name,
                                 stream.props.stream_name)
            provides.add(tempstr)


    # Now go through our list and build up a content lists which will
    # have only modules which have their dependencies met
    tempdict = {}
    for modname in idx.get_default_streams():
        mod = idx.get_module(modname)
        # Get the default streams and loop through them.
        # This is a sorted list with the latest in it. We could drop
        # looking at later ones here in a future version. (aka lines
        # 237 to later)
        stream_set = mod.get_streams_by_stream_name(
            mod.get_defaults().get_default_stream())
        for stream in stream_set:
            ourname = stream.get_NSVCA()
            tmp_name = "%s:%s" % (stream.props.module_name,
                                 stream.props.stream_name)
            # Get dependencies is a list of items. All of the modules
            # seem to only have 1 item in them, but we should loop
            # over the list anyway.
            for deps in stream.get_dependencies():
                isprovided = True # a variable to say this can be added.
                for mod in deps.get_runtime_modules():
                    tempstr=""
                    # It does not seem easy to figure out what the
                    # platform is so just assume we will meet it.
                    if mod != 'platform':
                        for stm in deps.get_runtime_streams(mod):
                            tempstr = "%s:%s" %(mod,stm)
                            if tempstr not in provides:
                                # print( "%s : %s not found." % (ourname,tempstr))
                                isprovided = False
                    if isprovided:
                        if tmp_name in tempdict:
                            # print("We found %s" % tmp_name)
                            # Get the stream version we are looking at
                            ts1=ourname.split(":")[2]
                            # Get the stream version we stored away
                            ts2=tempdict[tmp_name].split(":")[2]
                            # See if we got a newer one. We probably
                            # don't as it is a sorted list but we
                            # could have multiple contexts which would
                            # change things.
                            if ( int(ts1) > int(ts2) ):
                                # print ("%s > %s newer for %s", ts1,ts2,ourname)
                                tempdict[tmp_name] = ourname
                        else:
                            # print("We did not find %s" % tmp_name)
                            tempdict[tmp_name] = ourname
    # OK we finally got all our stream names we want to send back to
    # our calling function. Read them out and add them to the set.
    for indx in tempdict:
        contents.add(tempdict[indx])

    return contents


def perform_split(repos, args, def_modules):
    for modname in repos:
        if args.only_defaults and modname not in def_modules:
            continue
        
        targetdir = os.path.join(args.target, modname)
        os.mkdir(targetdir)

        for pkg in repos[modname]:
            _, pkgfile = os.path.split(pkg)
            _perform_action(
                os.path.join(args.repository, pkg),
                os.path.join(targetdir, pkgfile),
                args.action)


def create_repos(target, repos,def_modules, only_defaults):
    """
    Routine to create repositories. Input is target directory and a
    list of repositories.
    Returns None
    """
    for modname in repos:
        if only_defaults and modname not in def_modules:
            continue
        subprocess.run([
            'createrepo_c', os.path.join(target, modname),
            '--no-database'])


def parse_args():
    """
    A standard argument parser routine which pulls in values from the
    command line and returns a parsed argument dictionary.
    """
    parser = argparse.ArgumentParser(description='Split repositories up')
    parser.add_argument('repository', help='The repository to split')
    parser.add_argument('--action', help='Method to create split repos files',
                        choices=('hardlink', 'symlink', 'copy'),
                        default='hardlink')
    parser.add_argument('--target', help='Target directory for split repos')
    parser.add_argument('--skip-missing', help='Skip missing packages',
                        action='store_true', default=False)
    parser.add_argument('--create-repos', help='Create repository metadatas',
                        action='store_true', default=False)
    parser.add_argument('--only-defaults', help='Only output default modules',
                        action='store_true', default=False)
    return parser.parse_args()


def setup_target(args):
    """
    Checks that the target directory exists and is empty. If not it
    exits the program.  Returns nothing.
    """
    if args.target:
        args.target = os.path.abspath(args.target)
        if os.path.exists(args.target):
            if not os.path.isdir(args.target):
                raise ValueError("Target must be a directory")
            elif len(os.listdir(args.target)) != 0:
                raise ValueError("Target must be empty")
        else:
            os.mkdir(args.target)

def parse_repository(directory):
    """
    Parse a specific directory, returning a dict with keys module NSVC's and
    values a list of package NVRs.
    The dict will also have a key "non_modular" for the non-modular packages.
    """
    directory = os.path.abspath(directory)
    repo_info = _get_repoinfo(directory)

    # Get the package sack and get a filelist of all packages.
    package_sack = _get_hawkey_sack(repo_info)
    _get_filelist(package_sack)

    # If we have a repository with no modules we do not want our
    # script to error out but just remake the repository with
    # everything in a known sack (aka non_modular).
     
    if 'modules' in repo_info:
        mod = _parse_repository_modular(repo_info,package_sack)
        modpkgset = _get_modular_pkgset(mod)
    else:
        mod = dict()
        modpkgset = set()

    non_modular = _parse_repository_non_modular(package_sack,repo_info, 
                                  modpkgset) 
    mod['non_modular'] = non_modular

    ## We should probably go through our default modules here and
    ## remove them from our mod. This would cut down some code paths.

    return mod

def main():
    # Determine what the arguments are and 
    args = parse_args()

    # Go through arguments and act on their values.
    setup_target(args)

    repos = parse_repository(args.repository)

    if args.only_defaults:
        def_modules = get_default_modules(args.repository)
    else:
        def_modules = set()
    def_modules.add('non_modular')        
    
    if not args.skip_missing:
        if not validate_filenames(args.repository, repos):
            raise ValueError("Package files were missing!")
    if args.target:
        perform_split(repos, args, def_modules)
        if args.create_repos:
            create_repos(args.target, repos,def_modules,args.only_defaults)

if __name__ == '__main__':
    main()
