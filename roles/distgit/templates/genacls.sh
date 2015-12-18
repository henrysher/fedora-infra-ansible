#!/bin/bash -e

export GL_BINDIR=/usr/bin
TEMPDIR=`mktemp -d -p /var/tmp genacls.XXXXX`
cd $TEMPDIR

# If this fails, then the -e option will cause the whole script to quit.
/usr/local/bin/genacls.pkgdb > gitolite.conf

# Then create the repos and branches on disk (if we need any new ones)
python /usr/local/bin/pkgdb_sync_git_branches.py

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

cd /

rm -rf $TEMPDIR
chown root:packager /etc/gitolite/conf/gitolite.conf-compiled.pm
chmod g+r /etc/gitolite/conf/gitolite.conf-compiled.pm
