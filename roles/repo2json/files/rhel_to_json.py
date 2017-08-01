#!/usr/bin/env python2

"""
This script extracts the content of the primary.sqlite databases used by
RHEL and generates a big JSON out of it so that we can easily check which
packages already are in RHEL and on which arch.

requires:
 sqlalchemy
 lzma (only if there are .xz compressed primary.sqlite db)

"""

# These two lines are needed to run on EL6
__requires__ = ['SQLAlchemy >= 0.7']
import pkg_resources


import contextlib
import json
import os
import shutil
import sys
import tempfile


# Database related part

from sqlalchemy import Column, ForeignKey, Integer, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


BASE = declarative_base()


class Package(BASE):
    ''' Maps the packages table in the primary.sqlite database from
    repodata to a python object.
    '''
    __tablename__ = 'packages'
    pkgKey = Column(Integer, primary_key=True)
    name = Column(Text)
    rpm_sourcerpm = Column(Text)
    version = Column(Text)
    epoch = Column(Text)
    release = Column(Text)
    arch = Column(Text)

    @property
    def basename(self):
        ''' Return the base package name using the rpm_sourcerpms info. '''
        return self.rpm_sourcerpm.rsplit('-', 2)[0]


# Here below we tell the script where to look for the repodata, we could
# point it to the top level, but then we would miss the differences between
# el5, 6 and 7.
# I tried to create some rhel5 and rhel6 folders in which I sym-linked the
# respective el5/6 folder from the level above. The problem was that
# os.path.walk() doesn't follow links, so it would not find any repodata.

PATHS = {
    'el7': [
        '/mnt/fedora/app/fi-repo/rhel/rhel7/x86_64/rhel-7-server-extras-rpms',
        '/mnt/fedora/app/fi-repo/rhel/rhel7/x86_64/rhel-7-server-optional-rpms',
        '/mnt/fedora/app/fi-repo/rhel/rhel7/x86_64/rhel-7-server-rpms',
        '/mnt/fedora/app/fi-repo/rhel/rhel7/x86_64/rhel-ha-for-rhel-7-server-rpms',
        '/mnt/fedora/app/fi-repo/rhel/rhel7/ppc64/rhel-7-server-extras-rpms',
        '/mnt/fedora/app/fi-repo/rhel/rhel7/ppc64/rhel-7-server-optional-rpms',
        '/mnt/fedora/app/fi-repo/rhel/rhel7/ppc64/rhel-7-server-rpms',
        '/mnt/fedora/app/fi-repo/rhel/rhel7/ppc64/rhel-ha-for-rhel-7-server-rpms',
        '/mnt/fedora/app/fi-repo/rhel/rhel7/ppc64le/rhel-7-server-optional-rpms',
        '/mnt/fedora/app/fi-repo/rhel/rhel7/ppc64le/rhel-7-server-rpms',
        '/mnt/fedora/app/fi-repo/rhel/rhel7/ppc64le/rhel-ha-for-rhel-7-server-rpms',
    ],
    'el6': [
        '/mnt/fedora/app/fi-repo/rhel/rhel-i386-server-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-i386-server-fastrack-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-i386-server-ha-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-i386-server-ha-fastrack-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-i386-server-lb-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-i386-server-lb-fastrack-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-i386-server-optional-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-i386-server-optional-fastrack-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-ppc64-server-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-ppc64-server-fastrack-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-ppc64-server-ha-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-ppc64-server-ha-fastrack-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-ppc64-server-lb-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-ppc64-server-lb-fastrack-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-ppc64-server-optional-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-ppc64-server-optional-fastrack-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-x86_64-server-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-x86_64-server-fastrack-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-x86_64-server-ha-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-x86_64-server-ha-fastrack-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-x86_64-server-lb-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-x86_64-server-lb-fastrack-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-x86_64-server-optional-6',
        '/mnt/fedora/app/fi-repo/rhel/rhel-x86_64-server-optional-fastrack-6',
    ],
    'el5': [
        '/mnt/fedora/app/fi-repo/rhel/rhel-i386-server-5/',
        '/mnt/fedora/app/fi-repo/rhel/rhel-i386-server-fastrack-5/',
        '/mnt/fedora/app/fi-repo/rhel/rhel-i386-server-productivity-5/',
        '/mnt/fedora/app/fi-repo/rhel/rhel-i386-server-vt-5/',
        '/mnt/fedora/app/fi-repo/rhel/rhel-ppc-server-5/',
        '/mnt/fedora/app/fi-repo/rhel/rhel-ppc-server-fastrack-5/',
        '/mnt/fedora/app/fi-repo/rhel/rhel-ppc-server-productivity-5/',
        '/mnt/fedora/app/fi-repo/rhel/rhel-ppc-server-vt-5/',
        '/mnt/fedora/app/fi-repo/rhel/rhel-x86_64-server-5/',
        '/mnt/fedora/app/fi-repo/rhel/rhel-x86_64-server-fastrack-5/',
        '/mnt/fedora/app/fi-repo/rhel/rhel-x86_64-server-productivity-5/',
        '/mnt/fedora/app/fi-repo/rhel/rhel-x86_64-server-vt-5/',
    ],
}


def find_primary_sqlite(paths):
    ''' Find all the primary.sqlite files located at or under the given
    path.
    '''
    if not isinstance(paths, list):
        paths = [paths]
    files = []
    for path in paths:
        if not os.path.isdir(path):
            continue
        for (dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                if 'primary.sqlite' in filename:
                    files.append(os.path.join(dirpath, filename))
    return files


def decompress_primary_db(archive, location):
    ''' Decompress the given XZ archive at the specified location. '''
    if archive.endswith('.xz'):
        import lzma
        with contextlib.closing(lzma.LZMAFile(archive)) as stream_xz:
            data = stream_xz.read()
        with open(location, 'wb') as stream:
            stream.write(data)
    elif archive.endswith('.gz'):
        import tarfile
        with tarfile.open(archive) as tar:
            tar.extractall(path=location)
    elif archive.endswith('.bz2'):
        import bz2
        with open(location, 'w') as out:
            bzar = bz2.BZ2File(archive)
            out.write(bzar.read())
            bzar.close()
    elif archive.endswith('.sqlite'):
        with open(location, 'w') as out:
            with open(archive) as inp:
                out.write(inp.read())


def get_pkg_info(session, pkg_name):
    ''' Query the sqlite database for the package specified. '''
    pkg = session.query(Package).filter(Package.name == pkg_name).one()
    return pkg


def main():
    ''' Main function, does the job :) '''
    working_dir = tempfile.mkdtemp(prefix='rhel2json-')
    print 'working dir:', working_dir

    for el in PATHS:

        output = {'packages': {}, 'arches': []}

        dbfiles = find_primary_sqlite(PATHS[el])

        for dbfile_xz in dbfiles:
            cur_fold = os.path.join(*dbfile_xz.rsplit(os.sep, 2)[:-2])
            channel = os.path.basename(cur_fold)
            print '-', cur_fold
            dbfile = os.path.join(working_dir, 'primary_db_%s.sqlite' % el)
            decompress_primary_db(dbfile_xz, dbfile)

            if not os.path.isfile(dbfile):
                print '%s was incorrectly decompressed -- ignoring' % dbfile
                continue

            db_url = 'sqlite:///%s' % dbfile
            db_session = sessionmaker(bind=create_engine(db_url))
            session = db_session()

            cnt = 0
            new = 0
            for pkg in session.query(Package).all():
                if pkg.basename in output['packages']:
                    # Update the list of arches the package has
                    if pkg.arch not in output['packages'][
                            pkg.basename]['arch']:
                        output['packages'][pkg.basename]['arch'].append(
                            pkg.arch)
                    # Adjust the gobal list of all arches in the RHEL
                    if pkg.arch not in output['arches']:
                        output['arches'].append(pkg.arch)
                    # Update the list of channels the package is in
                    if channel not in output['packages'][
                            pkg.basename]['channel']:
                        output['packages'][pkg.basename]['channel'].append(
                            channel)
                    output['packages'][pkg.basename][
                           'channels'][channel].append({
                        'epoch': pkg.epoch,
                        'versions': pkg.version,
                        'release': pkg.release,
                    })

                    # TODO: checks if the evr is more recent or not
                    # (and update if it is)
                else:
                    new += 1
                    output['packages'][pkg.basename] = {
                        'arch': [pkg.arch],
                        'epoch': pkg.epoch,
                        'version': pkg.version,
                        'release': pkg.release,
                        'channel': [channel],
                        'channels': {
                            channel: [{
                                'epoch': pkg.epoch,
                                'version': pkg.version,
                                'release': pkg.release,
                            }]
                        }
                    }
                cnt += 1
            print '%s packages in %s' % (cnt, cur_fold)
            print '%s packages were new packages' % (new)

        print '\n%s packages retrieved in %s' % (len(output['packages']), el)
        print '%s arches for in %s' % (len(output['arches']), el)
        outputfile = 'pkg_%s.json' % el
        with open(outputfile, 'w') as stream:
            stream.write(json.dumps(output))
        print 'Output File: %s\n' % outputfile

    # Drop the temp directory
    shutil.rmtree(working_dir)


if __name__ == '__main__':
    main()
