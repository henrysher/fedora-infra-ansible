#!/usr/bin/env python

import os
import sys
import subprocess
import pickle
from optparse import OptionParser
import yaml


def call(command):
    print "PYTHONPATH=%s" % os.environ["PYTHONPATH"], " ".join(command)
    subprocess.check_call(command, env=os.environ)

def cmdget(command):
    print "PYTHONPATH=%s" % os.environ["PYTHONPATH"], " ".join(command)
    out = subprocess.check_output(command, env=os.environ)
    return out.strip()


class Importer(object):

    def __init__(self, opts, config):
        self.opts = opts
        self.config = config
        self.existing_lists = [ l.strip() for l in
                cmdget(["sudo", "-u", "mailman",
                "mailman3", "lists", "-q"]).split("\n") ]
        self.index_path = self._get_index_path()

    def _get_index_path(self):
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
            print listaddr, "(%d/%d)" % (index+1, len(all_listnames))
            confpickle = os.path.join(mm2libdir, 'lists', listname,
                                      'config.pck')
            if not os.path.exists(confpickle):
                print "Missing configuration pickle:", confpickle
                continue
            list_is_new = bool(listaddr not in self.existing_lists)
            if list_is_new:
                call(["sudo", "-u", "mailman", "mailman3", "create", "-d",
                      listaddr])
                call(["sudo", "-u", "mailman", "mailman3", "import21",
                      listaddr, confpickle])
            if not self.opts.no_archives:
                archivefile = os.path.join(
                        mm2libdir, "archives", "private",
                        "%s.mbox" % listname, "%s.mbox" % listname)
                archive_policy = bool(pickle.load(
                                      open(confpickle)).get('archive'))
                if not archive_policy:
                    print "List %s wants no archiving" % listname
                    continue
                if os.path.exists(archivefile) and \
                        (list_is_new or not self.opts.new_only):
                    call(["sudo", "kittystore-import", "-p",
                         self.config["confdir"], "-s", "settings_admin",
                         "-l", listaddr, "--continue", "--no-refresh",
                         archivefile])
                if self.index_path:
                    call(["sudo", "chown", "mailman:apache", "-R", self.index_path])
                    call(["sudo", "chmod", "g+w", self.index_path])
        if self.opts.no_archives:
            call(["sudo", "kittystore-refresh-cache", "-p",
                 self.config["confdir"], "-s", "settings_admin"])
        else:
            call(["sudo", "kittystore-refresh-cache", "-p",
                 self.config["confdir"], "-s", "settings_admin", "-f"])



def main():
    parser = OptionParser()
    parser.add_option("-n", "--new-only", action="store_true",
                      help="Only import the archives when the list is new")
    parser.add_option("-A", "--no-archives", action="store_true",
                  help="Don't import the archives, only import the list config")
    parser.add_option("-c", "--config", default="/etc/mailman-migration.conf",
                  help="Configuration file (default: %defaults)")
    opts, args = parser.parse_args()
    if len(args) != 1:
        parser.error("Only one arg: the Mailman 2.1 lib dir to import")

    mm2libdir = args[0]
    if not os.path.exists(mm2libdir):
        parser.error("No such directory: %s" % mm2libdir)

    with open(opts.config) as conffile:
        config = yaml.safe_load(conffile)

    sys.path.append(config["mm21codedir"])
    # set the env var to propagate to subprocesses
    os.environ["PYTHONPATH"] = config["mm21codedir"]

    importer = Importer(opts, config)
    importer.import_dir(mm2libdir)


if __name__ == "__main__":
    main()
