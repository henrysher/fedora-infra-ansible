#!/usr/bin/env python2
# -*- coding: utf-8 -*-

"""
This script does a few things:
- It iterates over all the spec files found in the given directory
- For each of these files it finds all the lines starting with `ExclusiveArch`
  or `ExcludesArch`
- It thus builds a dictionnary of filenames -> list of lines of interest
- If it ran before and this ``RESULTS`` file is found, it compares the
  current list of packages with the old one and report:
    - Packages that are now restricting their build arch where they weren't
    - Packages that changes their build arch constraints
    - Packages that no longer restrict their build arch
- Finally it prints anyway the entire list of packages restricting their
  build arch and save it in JSON in ``RESULTS`` (cf line 33)

To run it:

  python alternative_arch_report.py /srv/git_seed/rpm-specs > output

"""


import itertools
import json
import sys
import os

from multiprocessing import Pool, Manager


RESULTS = '/srv/cache/lookaside/excluding_arches.json'


def parse_folder(arg):
    """ This function does something important in parallel but where we
    want to centralize the output, thus using the queue
    """
    filename, foldername, myq = arg

    with open(os.path.join(foldername, filename)) as stream:
        data = stream.read()

    cnt = data.count('ExclusiveArch') + data.count('ExcludesArch')

    lines = []
    if cnt > 0:
        data = data.split('\n')
        for line in data:
            if line.startswith(('ExclusiveArch', 'ExcludesArch')):
                lines.append(line)
            if len(lines) == cnt:
                break

    if lines:
        name = filename.replace('.spec', '')
        myq.put((name, lines))
        myq.task_done()

def main():
    ''' For a specified folder, check all the sub-folder for spec files
    and report if any of them is excluding some arches.
    '''
    if len(sys.argv) == 1:
        print 'alternative_arch_report.py /path/to/folder/with/spec'
        return 1

    foldername = sys.argv[1]
    if not os.path.isdir(foldername):
        print '%s must be a folder' % foldername
        return 2

    files = os.listdir(foldername)
    m = Manager()
    q = m.Queue()
    p = Pool(5)
    p.map(parse_folder, itertools.product(files, [foldername], [q]))

    excluding_arches = {}
    while q.qsize():
        item = q.get()
        excluding_arches[item[0]] = item[1]
    q.join()

    previous_data = None
    if os.path.exists(RESULTS):
        with open(RESULTS) as stream:
            previous_data = json.load(stream)

    new = {}
    changed = {}
    removed = []
    if previous_data:
        prev_pkgs = set(previous_data)
        cur_pkgs = set(excluding_arches)
        new = dict((pkg, excluding_arches[pkg]) for pkg in cur_pkgs - prev_pkgs)
        removed = prev_pkgs - cur_pkgs
        changed = [pkg for pkg in cur_pkgs.intersection(prev_pkgs)
            if sorted(previous_data[pkg]) != sorted(excluding_arches[pkg])]

    def _fmt_output(pkg, data):
        print ' - %s\n      %s' % (
                pkg,
                '\n      '.join(data[pkg])
            )

    if new:
        print 'New package excluding arches (%s)' % len(new)
        print '============================\n'
        for pkg in sorted(new):
            _fmt_output(pkg, excluding_arches)
        print '\n'

    if changed:
        print 'Package that edited their arches constraints (%s)' % len(changed)
        print '=============================================\n'
        for pkg in sorted(changed):
            print ' - %s' % pkg
            print '   was   %s' % '\n         '.join(previous_data[pkg])
            print '    is   %s' % '\n         '.join(excluding_arches[pkg])
            print '\n'

    if removed:
        print 'Package no longer excluding arches (%s)'  % len(removed)
        print '==================================\n'
        for pkg in sorted(removed):
            print ' - %s' % pkg
            print '\n'

    print 'List of packages currently excluding arches (%s)' % len(excluding_arches)
    print '===========================================\n'
    for pkg in sorted(excluding_arches):
        _fmt_output(pkg, excluding_arches)

    with open(RESULTS, 'w') as stream:
        json.dump(excluding_arches, stream)

    return 0


if __name__ == '__main__':
    sys.exit(main())
