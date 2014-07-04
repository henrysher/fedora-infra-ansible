# General Utility Functions used in our Git scripts
#
# Copyright (C) 2008  Owen Taylor
# Copyright (C) 2009  Red Hat, Inc
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, If not, see
# http://www.gnu.org/licenses/.

import os
import sys
from subprocess import Popen
import tempfile
import time

def die(message):
    print >>sys.stderr, message
    sys.exit(1)

# This cleans up our generation code by allowing us to use the same indentation
# for the first line and subsequent line of a multi-line string
def strip_string(str):
    start = 0
    end = len(str)
    if len(str) > 0 and str[0] == '\n':
        start += 1
    if len(str) > 1 and str[end - 1] == '\n':
        end -= 1

    return str[start:end]

# How long to wait between mails (in seconds); the idea of waiting
# is to try to make the sequence of mails we send out in order
# actually get delivered in order. The waiting is done in a forked
# subprocess and doesn't stall completion of the main script.
EMAIL_DELAY = 5

# Some line that can never appear in any email we send out
EMAIL_BOUNDARY="---@@@--- gnome-git-email ---@@@---\n"

# Run in subprocess
def _do_send_emails(email_in):
    email_files = []
    current_file = None
    last_line = None

    # Read emails from the input pipe and write each to a file
    for line in email_in:
        if current_file is None:
            current_file, filename = tempfile.mkstemp(suffix=".mail", prefix="gnome-post-receive-email-")
            email_files.append(filename)

        if line == EMAIL_BOUNDARY:
            # Strip the last line if blank; see comment when writing
            # the email boundary for rationale
            if last_line.strip() != "":
                os.write(current_file, last_line)
            last_line = None
            os.close(current_file)
            current_file = None
        else:
            if last_line is not None:
                os.write(current_file, last_line)
            last_line = line

    if current_file is not None:
        if last_line is not None:
            os.write(current_file, last_line)
        os.close(current_file)

    # We're done interacting with the parent process, the rest happens
    # asynchronously; send out the emails one by one and remove the
    # temporary files
    for i, filename in enumerate(email_files):
        if i != 0:
            time.sleep(EMAIL_DELAY)

        f = open(filename, "r")
        process = Popen(["/usr/sbin/sendmail", "-t"],
                        stdout=None, stderr=None, stdin=f)
        process.wait()
        f.close()

        os.remove(filename)

email_file = None

# Start a new outgoing email; returns a file object that the
# email should be written to. Call end_email() when done
def start_email():
    global email_file
    if email_file is None:
        email_pipe = os.pipe()
        pid = os.fork()
        if pid == 0:
            # The child

            os.close(email_pipe[1])
            email_in = os.fdopen(email_pipe[0])

            # Redirect stdin/stdout/stderr to/from /dev/null
            devnullin = os.open("/dev/null", os.O_RDONLY)
            os.close(0)
            os.dup2(devnullin, 0)

            devnullout = os.open("/dev/null", os.O_WRONLY)
            os.close(1)
            os.dup2(devnullout, 1)
            os.close(2)
            os.dup2(devnullout, 2)
            os.close(devnullout)

            # Fork again to daemonize
            if os.fork() > 0:
                sys.exit(0)

            try:
                _do_send_emails(email_in)
            except Exception:
                import syslog
                import traceback

                syslog.openlog(os.path.basename(sys.argv[0]))
                syslog.syslog(syslog.LOG_ERR, "Unexpected exception sending mail")
                for line in traceback.format_exc().strip().split("\n"):
                    syslog.syslog(syslog.LOG_ERR, line)

            sys.exit(0)

        email_file = os.fdopen(email_pipe[1], "w")
    else:
        # The email might not end with a newline, so add one. We'll
        # strip the last line, if blank, when emails, so the net effect
        # is to add a newline to messages without one
        email_file.write("\n")
        email_file.write(EMAIL_BOUNDARY)

    return email_file

# Finish an email started with start_email
def end_email():
    global email_file
    email_file.flush()
