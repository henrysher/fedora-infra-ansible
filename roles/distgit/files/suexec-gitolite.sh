#!/bin/bash
#
# Suexec wrapper for gitolite-shell
#

export GIT_PROJECT_ROOT="/srv/git/repositories"
export PAGURE_CONFIG=/etc/pagure/pagure_hook.cfg
export HOME=/srv/git
export GITOLITE_HTTP_HOME=/srv/git

# Hacky workaround because we set ScriptAlias more specific
export PATH_INFO="$SCRIPT_URL"

if [ -z "$REMOTE_USER" ];
then
    # Fall back to default user
    export REMOTE_USER="anonymous"
fi

exec /usr/share/gitolite3/gitolite-shell
