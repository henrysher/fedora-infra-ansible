#!/bin/bash
dest=/etc/motd

cat << EOF > $dest
================================== ATTENTION ==================================

        This is a PRIVATE computer system, unauthorized access is
        strictly prohibited.

This system is to be used for Fedora Project and related purposes only.  This
is not your personal computing system.  Users who are unsure whether or not
they have access to this system, don't have it and should log off immediately.

There is no expectation of privacy of any kind on this system.  All questions
concerning access should be directed to admin@fedoraproject.org

===============================================================================

This system is ansible managed!  Local changes may be overwritten.

EOF
notesurl="http://infrastructure.fedoraproject.org/infra/hosts/$(/bin/hostname)/notes"
hasnotes=`/usr/bin/wget --tries=1 --timeout=3 -q -O /dev/null "$notesurl"`
if [ "$?" == 0 ]; then
   echo -e "\nnotes available from:\n $notesurl\n\n" >> $dest
   /usr/bin/wget --tries=1 --timeout=3 -q -O- $notesurl >> $dest
else
   echo -e "\n\n********\nNo notes found for this server! Please add some in the infra-hosts repository\n********\n" >> $dest
fi

