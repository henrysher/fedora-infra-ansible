#!/usr/bin/bash

systemctl stop copr-dist-git


cd /var/lib/dist-git/
mkdir -p backup
tar --selinux --acls --xattrs -czf tmp.backup.tar.gz /var/lib/dist-git/cache /var/lib/dist-git/git /var/lib/dist-git/gitolite /var/lib/dist-git/web
mv -f tmp.backup.tar.gz backup/copr_dist_git.tar.gz

systemctl start copr-dist-git
