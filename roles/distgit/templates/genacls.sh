#!/bin/bash -e

export GL_BINDIR=/usr/bin
TEMPDIR=`mktemp -d -p /var/tmp genacls.XXXXX`
cd $TEMPDIR

# If this fails, then the -e option will cause the whole script to quit.
/usr/local/bin/genacls.pkgdb > gitolite.conf

# Then create the repos and branches on disk (if we need any new ones)
python /usr/local/bin/pkgdb_sync_git_branches.py

# Leverage gitolite's Alias.pm feature to build backwards compat links
cat /etc/gitolite/RepoAliases.header > RepoAliases.pm
# Get all repos.  Strip off 'rpms/'.  Convert to perl mapping.  Tack it on.
grep rpms/ ./gitolite.conf | \
        sed 's/repo rpms\///g' | \
        sed "s/.*/'&' => 'rpms\/&',/g" \
        >> RepoAliases.pm
echo "};}1;" >> RepoAliases.pm

# With that done, move the files into place and run compile
mv gitolite.conf /etc/gitolite/conf/
chown gen-acls:gen-acls -R /etc/gitolite/conf/
mv RepoAliases.pm /etc/gitolite/RepoAliases.pm
chown gen-acls:gen-acls -R /etc/gitolite/RepoAliases.pm
HOME=/srv/git /usr/bin/gitolite compile

cd /

rm -rf $TEMPDIR
chown root:packager /etc/gitolite/conf/gitolite.conf-compiled.pm
chmod g+r /etc/gitolite/conf/gitolite.conf-compiled.pm
