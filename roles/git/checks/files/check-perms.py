#!/usr/bin/python -tt
"""Check permissions of a tree of git repositories, optionally fixing any
problems found.
"""

import os
import re
import sys
import optparse
from stat import *
from subprocess import call, PIPE, Popen

ALL_CHECKS = ['bare', 'shared', 'mail-hook', 'fedmsg-hook', 'perms',
              'post-update-hook', 'update-hook']
DEFAULT_CHECKS = ['bare', 'shared', 'perms', 'post-update-hook']

OBJECT_RE = re.compile('[0-9a-z]{40}')


def error(msg):
    print >> sys.stderr, msg


def is_object(path):
    """Check if a path is a git object."""
    parts = path.split(os.path.sep)
    if 'objects' in parts and len(parts) > 2 and \
            OBJECT_RE.match(''.join(path.split(os.path.sep)[-2:])):
        return True
    return False


def is_bare_repo(gitdir):
    """Check if a git repository is bare."""
    cmd = ['git', '--git-dir', gitdir, 'config', '--bool', 'core.bare']
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    bare, error = p.communicate()
    if bare.rstrip() != 'true' or p.returncode:
        return False
    return True


def is_shared_repo(gitdir):
    """Check if a git repository is shared."""
    cmd = ['git', '--git-dir', gitdir, 'config', 'core.sharedRepository']
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    shared, error = p.communicate()
    sharedmodes = ['1', 'group', 'true', '2', 'all', 'world', 'everybody']
    if shared.rstrip() not in sharedmodes or p.returncode:
        return False
    return True


def uses_version1_mail_hook(gitdir):
    """Check if a git repository uses the old fedora-git-commit-mail-hook."""
    hook = os.path.join(gitdir, 'hooks/update')
    oldpath = '/usr/bin/fedora-git-commit-mail-hook'
    return os.path.realpath(hook) == oldpath


def uses_version2_mail_hook(gitdir):
    """Check if a git repository uses the pre-fedmsg mail-hook setup."""
    hook = os.path.join(gitdir, 'hooks/post-receive')
    oldpath = '/usr/share/git-core/mail-hooks/gnome-post-receive-email'
    return os.path.realpath(hook) == oldpath


def check_post_update_hook(gitdir, fix=False):
    """Check if a repo's post-update hook is setup correctly."""
    hook = os.path.join(gitdir, 'hooks/post-update')
    realpath = os.path.realpath(hook)
    goodpath = '/usr/share/git-core/templates/hooks/post-update.sample'
    badpath = '/usr/bin/git-update-server-info'

    if realpath == goodpath:
        return True

    errmsg = ''
    if realpath == badpath:
        errmsg = '%s: symlinked to %s' % (hook, badpath)
    elif not os.path.exists(hook):
        errmsg = '%s: does not exist' % hook
    elif not os.access(hook, os.X_OK):
        errmsg = '%s: is not executable' % hook
    elif not os.path.islink(hook):
        errmsg = '%s: not a symlink' % hook
    else:
        errmsg = '%s: symlinked to %s' % (hook, realpath)

    error(errmsg)

    if not fix:
        return False

    if not os.path.exists(goodpath):
        error('%s: post-update hook (%s) does not exist.' % (gitdir, goodpath))
        return False

    if os.path.exists(hook):
        try:
            os.rename(hook, '%s~' % hook)
        except (IOError, OSError), err:
            error('%s: Error renaming %s: %s' % (gitdir, hook, err.strerror))
            return False
    try:
        os.symlink(goodpath, hook)
    except (IOError, OSError), err:
        error('%s: Error creating %s symlink: %s' % (gitdir, hook, err.strerror))
        return False

    return True


def set_bare_repo(gitdir):
    """Set core.bare for a git repository."""
    cmd = ['git', '--git-dir', gitdir, 'config', '--bool', 'core.bare', 'true']
    ret = call(cmd)
    if ret:
        return False
    return True


def set_shared_repo(gitdir, value='group'):
    """Set core.sharedRepository for a git repository."""
    mode_re = re.compile('06[0-7]{2}')
    if value in [0, 'false', 'umask']:
        value = 'umask'
    elif value in [1, 'true', 'group']:
        value = 'group'
    elif value in [2, 'all', 'world', 'everybody']:
        value = 'all'
    elif mode_re.match(value):
        pass
    else:
        raise SystemExit('Bogus core.sharedRepository value "%s"' % value)
    cmd = ['git', '--git-dir', gitdir, 'config', 'core.sharedRepository',
            value]
    ret = call(cmd)
    if ret:
        return False
    return True


def set_post_receive_hook_version2(gitdir):
    """Configure a git repository to use the gnome mail hook without fedmsg."""

    # Get recipients from the commit-list file.
    commit_list = os.path.join(gitdir, 'commit-list')
    if not os.path.exists(commit_list):
        error('%s: No commit-list file found' % gitdir)
        return False
    try:
        addrs = open(commit_list).read().strip()
        addrs = ', '.join(addrs.split())
    except:
        error('%s: Unable to read commit-list file' % gitdir)
        return False

    # Set hooks.mailinglist
    if '@' not in addrs:
        addrs = '%s@lists.fedorahosted.org'
    cmd = ['git', '--git-dir', gitdir, 'config', 'hooks.mailinglist', addrs]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if p.returncode:
        error('%s: Error setting hooks.mailinglist: %s' % (gitdir, stderr))
        return False

    # Set hooks.maildomain
    cmd = ['git', '--git-dir', gitdir, 'config', 'hooks.maildomain',
            'fedoraproject.org']
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if p.returncode:
        error('%s: Error setting hooks.maildomain: %s' % (gitdir, stderr))
        return False

    # Symlink mail notification script to post-receive hook
    script = '/usr/share/git-core/mail-hooks/gnome-post-receive-email'
    if not os.path.exists(script):
        error('%s: Mail hook (%s) does not exist.' % (gitdir, script))
        return False

    hook = os.path.join(gitdir, 'hooks', 'post-receive')
    if os.path.exists(hook):
        try:
            os.remove(hook)
        except Exception, e:
            errstr = hasattr(e, 'strerror') and e.strerror or e
            error('%s: Error removing %s: %s' % (gitdir, hook, errstr))
            return False
    try:
        os.symlink(script, hook)
    except Exception, e:
        errstr = hasattr(e, 'strerror') and e.strerror or e
        error('%s: Error creating %s symlink: %s' % (gitdir, hook, errstr))
        return False

    # Clean up commit-list file and old update hook link
    try:
        os.rename(commit_list, '%s~' % commit_list)
    except (IOError, OSError), err:
        error('%s: Unable to backup commit-list: %s' % (gitdir, err.strerror))
        return False
    try:
        oldhook = os.path.join(gitdir, 'hooks/update')
        os.remove(oldhook)
    except (IOError, OSError), err:
        error('%s: Unable to backup commit-list: %s' % (gitdir, err.strerror))
        return False

    # We ran the gauntlet.
    return True


def set_post_receive_hook_version3(gitdir, fix=False):
    """Configure a git repository to use the fedmsg+gnome-mail hooks."""

    # Old folder where we used to place the hooks
    hook_dir = os.path.join(gitdir, 'hooks')
    dest_prefix = os.path.join(hook_dir, 'post-receive-chained.d')

    # Remove the old hooks
    hooks = [
        os.path.join(dest_prefix, 'post-receive-email'),
        os.path.join(dest_prefix, 'post-receive-fedmsg'),
        os.path.join(dest_prefix, 'post-receive-alternativearch'),
        # These two hooks are setup by pagure but are already part of the
        # main post-receive hook
        os.path.join(hook_dir, 'post-receive.default'),
        os.path.join(hook_dir, 'post-receive.pagure'),
    ]

    for hook in hooks:
        if os.path.exists(hook):
            if not fix:
                error('%s should be removed' % hook)
            else:
                os.unlink(hook)

    if os.path.exists(dest_prefix):
        if not fix:
            error('%s should be removed' % dest_prefix)
        else:
            os.rmdir(dest_prefix)

    # Symlink the post-receive-chained to post-receive hook
    scripts = {
        # This one kicks off all the others.
        '/usr/share/git-core/post-receive-chained':
            os.path.join(gitdir, 'hooks', 'post-receive'),
    }

    for script, hook in scripts.items():
        if not os.path.exists(script):
            error('%s: Hook (%s) does not exist.' % (gitdir, script))
            return False
        if not fix:
            if not os.path.exists(hook):
                error('%s: Hook (%s) not installed.' % (gitdir, hook))
                return False

        if not os.path.islink(hook) \
                or (os.path.islink(hook) and os.path.realpath(hook) != script):
            if os.path.exists(hook) \
                    or (os.path.islink(hook) and os.path.realpath(hook) != script):
                try:
                    if not fix:
                        error('%s should be removed' % hook)
                    else:
                        os.remove(hook)
                except Exception, e:
                    errstr = hasattr(e, 'strerror') and e.strerror or e
                    error('%s: Error removing %s: %s' % (gitdir, hook, errstr))
                    return False
            try:
                if not fix:
                    error('link from %s to %s should be created' % (script, hook))
                else:
                    os.symlink(script, hook)
            except Exception, e:
                errstr = hasattr(e, 'strerror') and e.strerror or e
                error('%s: Error creating %s symlink: %s' % (gitdir, hook, errstr))
                return False

    # We ran the gauntlet.
    return True


def list_checks():
    print 'Available checks: %s' % ', '.join(ALL_CHECKS)
    print 'Default checks: %s' % ', '.join(DEFAULT_CHECKS)


def check_git_perms(path, fix=False):
    """Check if permissions on a git repo are correct.

    If fix is true, problems found are corrected.
    """
    object_mode = S_IRUSR | S_IRGRP | S_IROTH
    oldmode = mode = S_IMODE(os.lstat(path)[ST_MODE])
    errors = []
    if os.path.isdir(path):
        newmode = mode | S_ISGID
        if mode != newmode:
            msg = 'Not SETGID (should be "%s")' % oct(newmode)
            errors.append(msg)
            mode = newmode
    elif is_object(path) and mode ^ object_mode:
        msg = 'Wrong object mode "%s" (should be "%s")' % (
                oct(mode), oct(object_mode))
        errors.append(msg)
        mode = object_mode
    if mode & S_IWUSR and not is_object(path):
        newmode = mode | S_IWGRP
        exempt = \
                any(map(path.endswith, ['commit-list', 'gl-conf'])) or \
                any(map(path.__contains__, ['/hooks/']))

        if mode != newmode and not exempt:
            msg = 'Not group writable (should be "%s")' % oct(newmode)
            errors.append(msg)
            mode = newmode
    if mode != oldmode and not os.path.islink(path):
        errmsg = '%s:' % path
        errmsg += ', '.join(['%s' % e for e in errors])
        error(errmsg)
        if not fix:
            return False
        try:
            os.chmod(path, mode)
            return True
        except Exception, e:
            errstr = hasattr(e, 'strerror') and e.strerror or e
            mode = oct(mode)
            error('%s: Error setting "%s" mode on %s: %s' % (gitdir,
                    mode, path, errstr))
            return False
    return True


def check_gitolite_update_hook(gitdir, fix=False):
    """Check our update hooks

    This ensures that the Git repository at `gitdir` is set up with the proper
    update hook for Gitolite.

    If it isn't, and if `fix` is True, this actually fixes the problem.
    """
    gitolite_hook = '/etc/gitolite/hooks/common/update'
    update_hook = os.path.join(gitdir, 'hooks', 'update')

    if not os.path.exists(update_hook):
        if fix:
            os.symlink(gitolite_hook, update_hook)
            return

        raise ValueError('No update hook set up')

    if os.path.realpath(update_hook) != gitolite_hook:
        if fix:
            os.unlink(update_hook)
            os.symlink(gitolite_hook, update_hook)
            return

        raise ValueError('Update hook does not point to the Gitolie one')


def main():
    usage = '%prog [options] [gitroot]'
    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-f', '--fix', action='store_true', default=False,
                      help='Correct any problems [%default]')
    parser.add_option('-l', '--list-checks', action='store_true',
                      help='List default checks')
    parser.add_option('-c', '--check', dest='checks', action='append',
                      default=[], metavar='check',
                      help='Add a check, may be used multiple times')
    parser.add_option('-s', '--skip', action='append', default=[],
                      metavar='check',
                      help='Skip a check, may be used multiple times')
    parser.add_option('-r', '--repo', default=None,
                      help="Check only a certain repo, not all of them.")
    opts, args = parser.parse_args()

    # Check options
    if opts.list_checks:
        list_checks()
        raise SystemExit

    if opts.checks:
        checks = set(opts.checks)
        bad_check_opts = checks.difference(set(ALL_CHECKS))
        if bad_check_opts:
            msg = 'Bad check(s): %s' % ', '.join(sorted(bad_check_opts))
            msg += '\nAvailable checks: %s' % ', '.join(ALL_CHECKS)
            raise SystemExit(msg)
    else:
        bad_skip_opts = set(opts.skip).difference(set(ALL_CHECKS))
        if bad_skip_opts:
            msg = 'Bad skip option(s): %s' % ', '.join(sorted(bad_skip_opts))
            msg += '\nAvailable checks: %s' % ', '.join(ALL_CHECKS)
            raise SystemExit(msg)
        checks = set()
        for check in DEFAULT_CHECKS:
            if check not in opts.skip:
                checks.add(check)

    # Check args
    if len(args) > 1:
        raise SystemExit(parser.get_usage().strip())

    gitroot = args and args[0] or '/git'

    if not os.path.isdir(gitroot):
        raise SystemExit('%s does not exist or is not a directory' % gitroot)

    if opts.repo:
        gitdirs = ['/'.join([gitroot, opts.repo])]
    else:
        gitdirs = []
        for path, dirs, files in os.walk(gitroot):
            if path in gitdirs:
                continue
            if 'description' in os.listdir(path):
                gitdirs.append(path)

    problems = []
    for gitdir in sorted(gitdirs):
        if 'bare' in checks and not is_bare_repo(gitdir):
            error('%s: core.bare not true' % gitdir)
            if not opts.fix or not set_bare_repo(gitdir):
                problems.append(gitdir)
        if 'shared' in checks and not is_shared_repo(gitdir):
            error('%s: core.sharedRepository not set' % gitdir)
            if not opts.fix or not set_shared_repo(gitdir):
                problems.append(gitdir)

        if 'mail-hook' in checks and uses_version1_mail_hook(gitdir):
            error('%s: uses old mail hook' % gitdir)
            if not opts.fix or not set_post_receive_hook_version2(gitdir):
                problems.append(gitdir)

        if 'fedmsg-hook' in checks:
            if not set_post_receive_hook_version3(gitdir, fix=opts.fix):
                problems.append(gitdir)

        if 'post-update-hook' in checks and not check_post_update_hook(gitdir,
                opts.fix):
            problems.append(gitdir)

        if 'perms' in checks:
            paths = []
            for path, dirs, files in os.walk(gitdir):
                for d in dirs:
                    d = os.path.join(path, d)
                    if d not in paths:
                        paths.append(d)
                for f in files:
                    f = os.path.join(path, f)
                    if f not in paths:
                        paths.append(f)
            for path in paths:
                if not check_git_perms(path, fix=opts.fix):
                    problems.append(path)

        if 'update-hook' in checks:
            try:
                check_gitolite_update_hook(gitdir, fix=opts.fix)

            except Exception as e:
                error('%s: %s' % (gitdir, e))
                problems.append(gitdir)

    if problems:
        raise SystemExit('%d problems remain unfixed' % len(problems))

    raise SystemExit()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit('\nExiting on user cancel (Ctrl-C)')
