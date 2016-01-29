# (C) 2012, Michael DeHaan, <michael.dehaan@gmail.com>
# based on the log_plays example
# skvidal@fedoraproject.org
# rbean@redhat.com

# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

import os
import pwd

import fedmsg
import fedmsg.config

try:
    from ansible.plugins.callback import CallbackBase
except ImportError:
    # Ansible v1 compat
    CallbackBase = object

def getlogin():
    try:
        user = os.getlogin()
    except OSError, e:
        user = pwd.getpwuid(os.geteuid())[0]
    return user


class CallbackModule(CallbackBase):
    """ Publish playbook starts and stops to fedmsg. """

    playbook_path = None

    def __init__(self):
        config = fedmsg.config.load_config()
        config.update(dict(
            name='relay_inbound',
            cert_prefix='shell',
            active=True,
        ))
        # It seems like recursive playbooks call this over and over again and
        # fedmsg doesn't like to be initialized more than once.  So, here, just
        # catch that and ignore it.
        try:
            fedmsg.init(**config)
        except ValueError:
            pass


    def playbook_on_play_start(self, pattern):
        # This gets called once for each play.. but we just issue a message once
        # for the first one.  One per "playbook"
        play = getattr(self, 'play', None)
        if play:
            # figure out where the playbook FILE is
            path = os.path.abspath(play.playbook.filename)

            # Bail out early without publishing if we're in --check mode
            if play.playbook.check:
                return

            if not self.playbook_path:
                fedmsg.publish(
                    modname="ansible", topic="playbook.start",
                    msg=dict(
                        playbook=path,
                        userid=getlogin(),
                        extra_vars=play.playbook.extra_vars,
                        inventory=play.playbook.inventory.host_list,
                        playbook_checksum=play.playbook.check,
                        check=play.playbook.check,
                    ),
                )
                self.playbook_path = path

    def playbook_on_stats(self, stats):
        if not self.playbook_path:
            return

        results = dict([(h, stats.summarize(h)) for h in stats.processed])
        fedmsg.publish(
            modname="ansible", topic="playbook.complete",
            msg=dict(
                playbook=self.playbook_path,
                userid=getlogin(),
                results=results,
            ),
        )
