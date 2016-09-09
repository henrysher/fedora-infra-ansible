# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import copy
import json
import glob
import time
import shutil
import logging
import tempfile
import traceback
import subprocess
import pkg_resources

from datetime import datetime
from mako.template import Template


class AtomicComposer(object):
    """An atomic ostree composer"""

    def compose(self, release):
        release = copy.deepcopy(release)
        release['tmp_dir'] = tempfile.mkdtemp()
        release['timestamp'] = time.strftime('%y%m%d.%H%M')
        try:
            self.setup_logger(release)
            self.log.debug(release)
            self.update_configs(release)
            self.generate_mock_config(release)
            self.init_mock(release)
            self.sync_in(release)
            self.ostree_init(release)
            self.generate_repo_files(release)
            self.ostree_compose(release)
            self.update_ostree_summary(release)
            self.sync_out(release)
            release['result'] = 'success'
            self.cleanup(release)
        except:
            if hasattr(self, 'log'):
                self.log.exception('Compose failed')
            else:
                traceback.print_exc()
            release['result'] = 'failed'
        return release

    def setup_logger(self, release):
        name = '{name}-{timestamp}'.format(**release)
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        log_dir = release['log_dir']
        log_file = os.path.join(log_dir, name)
        release['log_file'] = log_file
        if not os.path.isdir(log_dir):
            os.makedirs(log_dir)
        stdout = logging.StreamHandler()
        handler = logging.FileHandler(log_file)
        log_format = ('%(asctime)s -  %(levelname)s - %(filename)s:'
                      '%(lineno)d - %(message)s')
        formatter = logging.Formatter(log_format)
        handler.setFormatter(formatter)
        handler.setLevel(logging.DEBUG)
        stdout.setFormatter(formatter)
        stdout.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        logger.addHandler(stdout)
        self.log = logger

    def cleanup(self, release):
        """Cleanup any temporary files after the compose"""
        shutil.rmtree(release['tmp_dir'])

    def update_configs(self, release):
        """ Update the fedora-atomic.git repositories for a given release """
        git_repo = release['git_repo']
        git_cache = release['git_cache']
        if not os.path.isdir(git_cache):
            self.call(['git', 'clone', '--mirror', git_repo, git_cache])
        else:
            self.call(['git', 'fetch', '--all', '--prune'], cwd=git_cache)
        git_dir = release['git_dir'] = os.path.join(release['tmp_dir'],
                                                    os.path.basename(git_repo))
        self.call(['git', 'clone', '-b', release['git_branch'],
                   git_cache, git_dir])

        if release['delete_repo_files']:
            for repo_file in glob.glob(os.path.join(git_dir, '*.repo')):
                self.log.info('Deleting %s' % repo_file)
                os.unlink(repo_file)

    def mock_cmd(self, release, *cmd):
        """Run a mock command in the chroot for a given release"""
        self.call('{mock_cmd} --configdir={mock_dir}'.format(**release).split()
                  + list(cmd))

    def init_mock(self, release):
        """Initialize/update our mock chroot"""
        root = '/var/lib/mock/%s' % release['mock']
        if not os.path.isdir(root):
            self.mock_cmd(release, '--init')
            self.log.info('mock chroot initialized')
        else:
            if release.get('mock_clean'):
                self.mock_cmd(release, '--clean')
                self.mock_cmd(release, '--init')
                self.log.info('mock chroot cleaned & initialized')
            else:
                self.mock_cmd(release, '--update')
                self.log.info('mock chroot updated')

    def generate_mock_config(self, release):
        """Dynamically generate our mock configuration"""
        mock_tmpl = pkg_resources.resource_string(__name__, 'templates/mock.mako')
        mock_dir = release['mock_dir'] = os.path.join(release['tmp_dir'], 'mock')
        mock_cfg = os.path.join(release['mock_dir'], release['mock'] + '.cfg')
        os.mkdir(mock_dir)
        for cfg in ('site-defaults.cfg', 'logging.ini'):
            os.symlink('/etc/mock/%s' % cfg, os.path.join(mock_dir, cfg))
        with file(mock_cfg, 'w') as cfg:
            mock_out = Template(mock_tmpl).render(**release)
            self.log.debug('Writing %s:\n%s', mock_cfg, mock_out)
            cfg.write(mock_out)

    def mock_chroot(self, release, cmd):
        """Run a commend in the mock container for a release"""
        self.mock_cmd(release, '--chroot', cmd)

    def generate_repo_files(self, release):
        """Dynamically generate our yum repo configuration"""
        repo_tmpl = pkg_resources.resource_string(__name__, 'templates/repo.mako')
        repo_file = os.path.join(release['git_dir'], '%s.repo' % release['repo'])
        with file(repo_file, 'w') as repo:
            repo_out = Template(repo_tmpl).render(**release)
            self.log.debug('Writing repo file %s:\n%s', repo_file, repo_out)
            repo.write(repo_out)
        self.log.info('Wrote repo configuration to %s', repo_file)

    def ostree_init(self, release):
        """Initialize the OSTree for a release"""
        out = release['output_dir'].rstrip('/')
        base = os.path.dirname(out)
        if not os.path.isdir(base):
            self.log.info('Creating %s', base)
            os.makedirs(base, mode=0755)
        if not os.path.isdir(out):
            self.mock_chroot(release, release['ostree_init'])

    def ostree_compose(self, release):
        """Compose the OSTree in the mock container"""
        start = datetime.utcnow()
        treefile = os.path.join(release['git_dir'], 'treefile.json')
        cmd = release['ostree_compose'] % treefile
        with file(treefile, 'w') as tree:
            json.dump(release['treefile'], tree)
        self.mock_chroot(release, cmd)
        self.log.info('rpm-ostree compose complete (%s)',
                      datetime.utcnow() - start)

    def update_ostree_summary(self, release):
        """Update the ostree summary file and return a path to it"""
        self.log.info('Updating the ostree summary for %s', release['name'])
        self.mock_chroot(release, release['ostree_summary'])
        return os.path.join(release['output_dir'], 'summary')

    def sync_in(self, release):
        """Sync the canonical repo to our local working directory"""
        tree = release['canonical_dir']
        if os.path.exists(tree) and release.get('rsync_in_objs'):
            out = release['output_dir']
            if not os.path.isdir(out):
                self.log.info('Creating %s', out)
                os.makedirs(out)
            self.call(release['rsync_in_objs'])
            self.call(release['rsync_in_rest'])

    def sync_out(self, release):
        """Sync our tree to the canonical location"""
        if release.get('rsync_out_objs'):
            tree = release['canonical_dir']
            if not os.path.isdir(tree):
                self.log.info('Creating %s', tree)
                os.makedirs(tree)
            self.call(release['rsync_out_objs'])
            self.call(release['rsync_out_rest'])

    def call(self, cmd, **kwargs):
        """A simple subprocess wrapper"""
        if isinstance(cmd, basestring):
            cmd = cmd.split()
        self.log.info('Running %s', cmd)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, **kwargs)
        out, err = p.communicate()
        if out:
            self.log.info(out)
        if err:
            self.log.error(err)
        if p.returncode != 0:
            self.log.error('returncode = %d' % p.returncode)
            raise Exception
        return out, err, p.returncode
