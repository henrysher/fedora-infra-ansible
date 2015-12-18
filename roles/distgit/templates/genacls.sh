#!/bin/bash -e

python /usr/local/bin/pkgdb_sync_git_branches.py

TEMPDIR=`mktemp -d -p /var/tmp genacls.XXXXX`
export GL_BINDIR=/usr/bin

cd $TEMPDIR
# Only replace the acls if genacls completes successfully
if /usr/local/bin/genacls.pkgdb > gitolite.conf ; then
    mv gitolite.conf /etc/gitolite/conf/
    chown gen-acls:gen-acls -R /etc/gitolite/conf/
    HOME=/srv/git /usr/bin/gitolite compile

    # After compiling, we have to stick some magic into the gl-conf files of
    # every repo so that gitolite will understand our symlinks from rpms/
    cd /srv/git/repositories
    for repodir in *.git; do
        glconf=$repodir/gl-conf;

        # Strip off the '.git' on the end.
        repo=${repodir::-4}

        # Check which repo from gitolite.conf won the gitolite race.
        if grep --quiet rpms/ $glconf;  then
            # ...and map things one way
            echo '$one_config{"'$repo'"} = $one_config{"rpms/'$repo'"};' >> $glconf;
            echo '$one_repo{"'$repo'"} = $one_repo{"rpms/'$repo'"};' >> $glconf;
        else
            # or map them the other way
            echo '$one_config{"rpms/'$repo'"} = $one_config{"'$repo'"};' >> $glconf;
            echo '$one_repo{"rpms/'$repo'"} = $one_repo{"'$repo'"};' >> $glconf;
        fi
    done
fi

cd /

rm -rf $TEMPDIR
chown root:packager /etc/gitolite/conf/gitolite.conf-compiled.pm
chmod g+r /etc/gitolite/conf/gitolite.conf-compiled.pm
