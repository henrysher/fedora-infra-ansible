#!/usr/bin/env python2

from __future__ import unicode_literals, absolute_import, print_function

import os
import sys
import subprocess
import pickle
from optparse import OptionParser
from locale import getpreferredencoding
import yaml

MAILMAN_BIN = subprocess.check_output(["which", "mailman"]).decode("ascii").strip()

from mailman.commands.cli_import import Bouncer
sys.modules["Mailman.Bouncer"] = Bouncer

def call(command):
    print(" ".join(command))
    subprocess.check_call(command, env=os.environ)

def cmdget(command):
    print(" ".join(command))
    out = subprocess.check_output(command, env=os.environ)
    return out.decode(getpreferredencoding()).strip()


class Importer(object):

    def __init__(self, opts, config):
        self.opts = opts
        self.config = config
        self.index_path = self._get_index_path()
        self.existing_lists = [ l.strip() for l in
                cmdget(["sudo", "-u", "mailman",
                MAILMAN_BIN, "lists", "-q"]).split("\n") ]
        self.excluded = opts.exclude.strip().split(",")

    def _get_index_path(self):
        return None
        sys.path.append(self.config["confdir"])
        settings = __import__("settings")
        sys.path.pop()
        return settings.KITTYSTORE_SEARCH_INDEX

    def import_dir(self, mm2libdir):
        all_listnames = [ d for d in os.listdir(
                                os.path.join(mm2libdir, 'lists'))
                          if not d.startswith(".") ]
        all_listnames.sort()
        for index, listname in enumerate(all_listnames):
            listaddr = "%s@%s" % (listname, self.config["domain"])
            if listname in self.excluded or listaddr in self.excluded:
                print("Skipping excluded list %s" % listaddr)
                continue
            print(listaddr, "(%d/%d)" % (index+1, len(all_listnames)))
            confpickle = os.path.join(mm2libdir, 'lists', listname,
                                      'config.pck')
            if not os.path.exists(confpickle):
                print("Missing configuration pickle:", confpickle)
                continue
            list_is_new = bool(listaddr not in self.existing_lists)
            if list_is_new:
                call(["sudo", "-u", "mailman", MAILMAN_BIN, "create", "-d",
                      listaddr])
                call(["sudo", "-u", "mailman", MAILMAN_BIN, "import21",
                      listaddr, confpickle])
            if not self.opts.no_archives:
                archivefile = os.path.join(
                        mm2libdir, "archives", "private",
                        "%s.mbox" % listname, "%s.mbox" % listname)
                archive_policy = bool(pickle.load(open(confpickle, "rb"),
                    encoding="utf-8", errors="ignore").get('archive'))
                if not archive_policy:
                    print("List %s wants no archiving" % listname)
                    continue
                if os.path.exists(archivefile) and \
                        (list_is_new or not self.opts.new_only):
                    call(["sudo", "django-admin", "hyperkitty_import",
                          "--pythonpath", self.config["confdir"],
                          "--settings", "settings", "-l", listaddr,
                          "--no-sync-mailman", archivefile])
                if self.index_path:
                    call(["sudo", "chown", "mailman:apache", "-R", self.index_path])
                    call(["sudo", "chmod", "g+w", self.index_path])
        call(["sudo", "django-admin", "mailman_sync",
              "--pythonpath", self.config["confdir"],
              "--settings", "settings"])



def main():
    parser = OptionParser()
    parser.add_option("-n", "--new-only", action="store_true",
                      help="Only import the archives when the list is new")
    parser.add_option("-A", "--no-archives", action="store_true",
                  help="Don't import the archives, only import the list config")
    parser.add_option("-c", "--config", default="/etc/mailman-migration.conf",
                  help="Configuration file (default: %defaults)")
    parser.add_option("-x", "--exclude", default="",
                  help="Comma-separated list of lists to exclude")
    opts, args = parser.parse_args()
    if len(args) != 1:
        parser.error("Only one arg: the Mailman 2.1 lib dir to import")

    mm2libdir = args[0]
    if not os.path.exists(mm2libdir):
        parser.error("No such directory: %s" % mm2libdir)

    with open(opts.config) as conffile:
        config = yaml.safe_load(conffile)

    importer = Importer(opts, config)
    importer.import_dir(mm2libdir)


if __name__ == "__main__":
    main()
