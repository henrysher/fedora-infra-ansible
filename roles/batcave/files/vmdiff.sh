#!/bin/bash
dest="/var/log/virthost-lists.out"
output=$(mktemp tmp.XXXXXXXXXX)
diffout=$(mktemp tmp.XXXXXXXXX)
mailto='admin@fedoraproject.org'
source /root/sshagent >>/dev/null
export ANSIBLE_HOST_KEY_CHECKING=False
/srv/web/infra/ansible/scripts/list-vms-per-host.v2 --host=virtservers 2>/dev/null  > "$output"
chmod 644 "$output"
diff -u "$dest" "$output" > $diffout
rc=$?
if [ $rc == 1 ]; then
    cat $diffout | /bin/mail -s "virthosts changed: `date +'%Y-%m-%d %H:%M'`" $mailto
    cp -f $dest ${dest}.last
elif [ $rc == 2 ]; then
    cat $output | /bin/mail -s "virthosts: `date +'%Y-%m-%d %H:%M'`" $mailto
fi
bad=""
bad=`/bin/grep 'shutdown:1' $output`
if [ -n "$bad" ]; then
   echo -e "\n$bad\n" | /bin/mail -s "shutdown virt instances which are set to autorun" $mailto
fi
mv -f "$output" "$dest"
rm -f $diffout
