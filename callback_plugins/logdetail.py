# (C) 2012, Michael DeHaan, <michael.dehaan@gmail.com>
# based on the log_plays example
# skvidal@fedoraproject.org

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

from __future__ import absolute_impor

import os
import time
import json
import pwd
from ansible import utils

try:
    from ansible.plugins.callback import CallbackBase
except ImportError:
    # Ansible v1 compat
    CallbackBase = object

TIME_FORMAT="%b %d %Y %H:%M:%S"

MSG_FORMAT="%(now)s\t%(count)s\t%(category)s\t%(name)s\t%(data)s\n"

LOG_PATH = '/var/log/ansible'

def getlogin():
    try:
        user = os.getlogin()
    except OSError, e:
        user = pwd.getpwuid(os.geteuid())[0]
    return user

class LogMech(object):
    def __init__(self):
        self.started = time.time()
        self.pid = str(os.getpid())
        self._pb_fn = None
        self._last_task_start = None
        self.play_info = {}
        self.logpath = LOG_PATH
        if not os.path.exists(self.logpath):
            try:
                os.makedirs(self.logpath, mode=0750)
            except OSError, e:
                if e.errno != 17:
                    raise

        # checksum of full playbook?

    @property
    def playbook_id(self):
        if self._pb_fn:
            return os.path.basename(self._pb_fn).replace('.yml', '').replace('.yaml', '')
        else:
            return "ansible-cmd"

    @playbook_id.setter
    def playbook_id(self, value):
        self._pb_fn = value

    @property
    def logpath_play(self):
        # this is all to get our path to look nice ish
        tstamp = time.strftime('%Y/%m/%d/%H.%M.%S', time.localtime(self.started))
        path = os.path.normpath(self.logpath + '/' + self.playbook_id +  '/' + tstamp + '/')

        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError, e:
                if e.errno != 17: # if it is not dir exists then raise it up
                    raise

        return path

    def play_log(self, content):
        # record out playbook.log
        # include path to playbook, checksums, user running playbook
        # any args we can get back from the invocation
        fd = open(self.logpath_play + '/' + 'playbook-' + self.pid + '.info', 'a')
        fd.write('%s\n' % content)
        fd.close()

    def task_to_json(self, task):
        res = {}
        res['task_name'] = task.name
        res['task_module'] = task.module_name
        res['task_args'] = task.module_args
        if self.playbook_id == 'ansible-cmd':
            res['task_userid'] = getlogin()
        for k in ("delegate_to", "environment", "with_first_found",
                  "local_action", "notified_by", "notify",
                  "register", "sudo", "sudo_user", "tags",
                  "transport", "when"):
            v = getattr(task, k, None)
            if v:
                res['task_' + k] = v

        return res

    def log(self, host, category, data, task=None, count=0):
        if not host:
            host = 'HOSTMISSING'

        if type(data) == dict:
            name = data.get('module_name',None)
        else:
            name = "unknown"


        # we're in setup - move the invocation  info up one level
        if 'invocation' in data:
            invoc = data['invocation']
            if not name and 'module_name' in invoc:
                name = invoc['module_name']

            #don't add this since it can often contain complete passwords :(
            del(data['invocation'])

        if task:
            name = task.name
            data['task_start'] = self._last_task_start
            data['task_end'] = time.time()
            data.update(self.task_to_json(task))

        if 'task_userid' not in data:
            data['task_userid'] = getlogin()

        if category == 'OK' and data.get('changed', False):
            category = 'CHANGED'

        if self.play_info.get('check', False) and self.play_info.get('diff', False):
            category = 'CHECK_DIFF:' + category
        elif self.play_info.get('check', False):    
            category = 'CHECK:' + category

        # Sometimes this is None.. othertimes it's fine.  Othertimes it has
        # trailing whitespace that kills logview.  Strip that, when possible.
        if name:
            name = name.strip()

        sanitize_host = host.replace(' ', '_').replace('>', '-')
        fd = open(self.logpath_play + '/' + sanitize_host + '.log', 'a')
        now = time.strftime(TIME_FORMAT, time.localtime())
        fd.write(MSG_FORMAT % dict(now=now, name=name, count=count, category=category, data=json.dumps(data)))
        fd.close()


logmech = LogMech()

class CallbackModule(CallbackBase):
    """
    logs playbook results, per host, in /var/log/ansible/hosts
    """
    CALLBACK_NAME = 'logdetail'
    CALLBACK_TYPE = 'notification'
    CALLBACK_VERSION = 2.0
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        self._task_count = 0
        self._play_count = 0

    def on_any(self, *args, **kwargs):
        pass


    def runner_on_failed(self, host, res, ignore_errors=False):
        category = 'FAILED'
        task = getattr(self,'task', None)
        logmech.log(host, category, res, task, self._task_count)


    def runner_on_ok(self, host, res):
        category = 'OK'
        task = getattr(self,'task', None)
        logmech.log(host, category, res, task, self._task_count)


    def runner_on_error(self, host, res):
        category = 'ERROR'
        task = getattr(self,'task', None)
        logmech.log(host, category, res, task, self._task_count)

    def runner_on_skipped(self, host, item=None):
        category = 'SKIPPED'
        task = getattr(self,'task', None)
        res = {}
        res['item'] = item
        logmech.log(host, category, res, task, self._task_count)

    def runner_on_unreachable(self, host, output):
        category = 'UNREACHABLE'
        task = getattr(self,'task', None)
        res = {}
        res['output'] = output
        logmech.log(host, category, res, task, self._task_count)

    def runner_on_no_hosts(self):
        pass

    def runner_on_async_poll(self, host, res, jid, clock):
        pass

    def runner_on_async_ok(self, host, res, jid):
        pass

    def runner_on_async_failed(self, host, res, jid):
        category = 'ASYNC_FAILED'
        task = getattr(self,'task', None)
        logmech.log(host, category, res, task, self._task_count)

    def playbook_on_start(self):
        pass

    def playbook_on_notify(self, host, handler):
        pass

    def playbook_on_no_hosts_matched(self):
        pass

    def playbook_on_no_hosts_remaining(self):
        pass

    def playbook_on_task_start(self, name, is_conditional):
        logmech._last_task_start = time.time()
        self._task_count += 1

    def playbook_on_vars_prompt(self, varname, private=True, prompt=None, encrypt=None, confirm=False, salt_size=None, salt=None, default=None):
        pass

    def playbook_on_setup(self):
        self._task_count += 1
        pass

    def playbook_on_import_for_host(self, host, imported_file):
        task = getattr(self,'task', None)
        res = {}
        res['imported_file'] = imported_file
        logmech.log(host, 'IMPORTED', res, task)

    def playbook_on_not_import_for_host(self, host, missing_file):
        task = getattr(self,'task', None)
        res = {}
        res['missing_file'] = missing_file
        logmech.log(host, 'NOTIMPORTED', res, task)

    def playbook_on_play_start(self, pattern):
        self._task_count = 0

        play = getattr(self, 'play', None)
        if play:
            # figure out where the playbook FILE is
            path = os.path.abspath(play.playbook.filename)

            # tel the logger what the playbook is
            logmech.playbook_id = path

            # if play count == 0
            # write out playbook info now
            if not self._play_count:
                pb_info = {}
                pb_info['playbook_start'] = time.time()
                pb_info['playbook'] = path
                pb_info['userid'] = getlogin()
                pb_info['extra_vars'] = play.playbook.extra_vars
                pb_info['inventory'] = play.playbook.inventory.host_list
                pb_info['playbook_checksum'] = utils.md5(path)
                pb_info['check'] = play.playbook.check
                pb_info['diff'] = play.playbook.diff
                logmech.play_log(json.dumps(pb_info, indent=4))

            self._play_count += 1
            # then write per-play info that doesn't duplcate the playbook info
            info = {}
            info['play'] = play.name
            info['hosts'] = play.hosts
            info['transport'] = play.transport
            info['number'] = self._play_count
            info['check'] = play.playbook.check
            info['diff'] = play.playbook.diff
            logmech.play_info = info
            logmech.play_log(json.dumps(info, indent=4))


    def playbook_on_stats(self, stats):
        results = {}
        for host in stats.processed.keys():
            results[host] = stats.summarize(host)
            logmech.log(host, 'STATS', results[host])
        logmech.play_log(json.dumps({'stats': results}, indent=4))
        logmech.play_log(json.dumps({'playbook_end': time.time()}, indent=4))
        print 'logs written to: %s' % logmech.logpath_play


