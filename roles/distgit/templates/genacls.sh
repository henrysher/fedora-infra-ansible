#!/bin/bash -e

export GL_BINDIR=/usr/bin
TEMPDIR=`mktemp -d -p /var/tmp genacls.XXXXX`
cd $TEMPDIR

# If this fails, then the -e option will cause the whole script to quit.
/usr/local/bin/genacls.pkgdb > gitolite.conf

# Then create the repos and branches on disk (if we need any new ones)
python /usr/local/bin/pkgdb_sync_git_branches.py

{% if env == 'staging' %}
# Leverage gitolite's Alias.pm feature to build backwards compat links
cat /etc/gitolite/RepoAliases.header > RepoAliases.pm
# Get all repos.  Strip off 'rpms/'.  Convert to perl mapping.  Tack it on.
grep rpms/ ./gitolite.conf | \
        sed 's/repo rpms\///g' | \
        sed "s/.*/'&' => 'rpms\/&',/g" \
        >> RepoAliases.pm
echo "};}1;" >> RepoAliases.pm
{% endif %}

# With that done, move the files into place and run compile
mv gitolite.conf /etc/gitolite/conf/
chown gen-acls:gen-acls -R /etc/gitolite/conf/
{% if env == 'staging' %}
mv RepoAliases.pm /etc/gitolite/RepoAliases.pm
chown gen-acls:gen-acls -R /etc/gitolite/RepoAliases.pm
{% endif %}
HOME=/srv/git /usr/bin/gitolite compile

{% if env != 'staging' %}
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
{% endif %}

cd /

rm -rf $TEMPDIR
chown root:packager /etc/gitolite/conf/gitolite.conf-compiled.pm
chmod g+r /etc/gitolite/conf/gitolite.conf-compiled.pm
