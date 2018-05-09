#!/usr/bin/env python
# encoding: utf-8
# (c) 2012 Red Hat, Inc.
# Authored by Ricky Elrod
# But when it breaks, don't yell at him because that's mean.
# update hook for FI repos -> zodbot.

import os
import sys
import subprocess
import shlex
import socket
import urllib

ZODBOT_SERVER = "value01"
ZODBOT_PORT = 5050

hook = sys.argv[0]
repodir = sys.argv[1]
channel = sys.argv[2]
old = sys.argv[3]
new = sys.argv[4]
branch = sys.argv[5]

# Split on /, nuke empties from the result, use the last nonempty
# element. This lets us not care if there's a trailing slash.
repodir = filter(None, repodir.split('/'))[-1]


def run_command(command):
    """ Run a command and return a hash with the resulting stdout/stderr."""
    escaped = shlex.split(command)
    cmd = subprocess.Popen(escaped,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE)
    stdout, stderr = cmd.communicate()
    return {"stdout": stdout, "stderr": stderr}


def construct_url(slug):
    """ Return a space-padded url to the commit.

    If and only if it is handled by cgit.  Otherwise, return an empty string.
    """

    # Our long url template.
    tmpl = "https://infrastructure.fedoraproject.org/cgit/{repo}/commit/?id={slug}"

    repo = repodir + ".git"

    with open('/etc/cgit-projects-batcave', 'r') as f:
        lines = [line.strip() for line in f.readlines()]

    if repo in lines and slug:
        return " " + tmpl.format(repo=repo, slug=slug)
    else:
        return ""


def parse_commit(commit):
    """
    So we're given a commit in the form of:

    ---
    Ricky Elrod - test-repo:a045150 ---- add some more test files...
    
    A       foobar/asdf/testfile.1
    A       foobar/testfile.2
    ---

    Essentially, we rip out the first line and set it aside.
    Then all the other lines will begin with M/C/R/A/D/U.
    Replace those letters with fancy little symbols (like + for A).
    Combine them together in a list/array.
    Show the first 4 and if more exist, append '...' to the list.
    Lastly, replace the "----" in the original line above with these.
    """
    
    lines = commit.split("\n")
    message = lines.pop(0)
    files = []

    # extract the commit hash from the first line.
    slug = None
    try:
        slug = message.split(' -')[1].strip().split(':')[1]
    except IndexError:
        print "** Couldn't parse slug from git-rev.", message

    # The remaining lines are files changed.
    for changed_file in filter(None, lines):
        status, filename = changed_file.split()
        if status == "M" or status == "R":
            symbol = "*"
        elif status == "C" or status == "A":
            symbol = "+"
        elif status == "D":
            symbol = "-"
        else:
            symbol = "?"

        files.append(symbol + filename)

    # Show the first 4 files changed, and if there are more, add a '...'
    # If no files were changed don't show empty [] because it looks tacky.
    fileslist = ' '.join(files[0:4])
    if len(files):
      fileslist = '[' + fileslist

      if len(files) > 4:
          fileslist += ' ...'

      fileslist += ']'
    else:
      fileslist = '-'

    padded_url = construct_url(slug)

    # Replace the ---- with the files list...
    return message.replace('----', fileslist, 1) + padded_url

# Get a list of commits to report.
if branch == 'master':
    revs = run_command("git rev-list ^%s %s" % (old, new))["stdout"].split("\n")
    revs = filter(None, revs)
    revs.reverse()

    for commit_hash in revs:
        # Get the commit in a format that we can deal with
        commit = run_command(
            "git show --name-status " + commit_hash + " --oneline "
            "--format='%an - " + repodir + ":%h ---- %s'")
        parsed_commit = parse_commit(commit["stdout"])

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ZODBOT_SERVER, ZODBOT_PORT))
        s.sendall(channel+ " " + parsed_commit)
        s.close()
