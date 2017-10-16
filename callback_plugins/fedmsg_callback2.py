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

try:
    from ansible.utils.hashing import secure_hash
except ImportError:
    from ansible.utils import md5 as secure_hash

def getlogin():
    try:
        user = os.getlogin()
    except OSError, e:
        user = pwd.getpwuid(os.geteuid())[0]
    return user


class CallbackModule(CallbackBase):
    """ Publish playbook starts and stops to fedmsg. """

    CALLBACK_NAME = 'fedmsg_callback2'
    CALLBACK_TYPE = 'notification'
    CALLBACK_VERSION = 2.0
    CALLBACK_NEEDS_WHITELIST = True

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
        self.play = None
        self.playbook = None

        super(CallbackModule, self).__init__()

    def set_play_context(self, play_context):
        self.play_context = play_context

    def v2_playbook_on_start(self, playbook):
        self.playbook = playbook

    def v2_playbook_on_play_start(self, play):
        # This gets called once for each play.. but we just issue a message once
        # for the first one.  One per "playbook"
        if self.playbook:
            # figure out where the playbook FILE is
            path = os.path.abspath(self.playbook._file_name)

            # Bail out early without publishing if we're in --check mode
            if self.play_context.check_mode:
                return

            if not self.playbook_path:
                fedmsg.publish(
                    modname="ansible", topic="playbook.start",
                    msg=dict(
                        playbook=path,
                        userid=getlogin(),
                        extra_vars=play._variable_manager.extra_vars,
                        inventory=play._variable_manager._inventory._sources,
                        playbook_checksum=secure_hash(path),
                        check=self.play_context.check_mode,
                    ),
                )
                self.playbook_path = path

    def v2_playbook_on_stats(self, stats):
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
