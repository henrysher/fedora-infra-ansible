#! /bin/bash

. /home/copr/cloud/keystonerc_proper_tenant

set -e

arch=$1

die() { echo "$*" >&2 ; exit 1 ; }

case $arch in
    ppc64le) playbook=/home/copr/provision/builderpb_nova_ppc64le.yml ;;
    x86_64)  playbook=/home/copr/provision/builderpb_nova.yml ;;
    *) die "bad architecture '$arch'" ;;
esac

logfile="/tmp/prepare-image-os-$arch.log"

ansible_options=( -e prepare_base_image=1 )
test -z "$2" || ansible_options+=( -e image_name="$2" )

ansible-playbook "$playbook" "${ansible_options[@]}" |& tee "$logfile"

vm_name=$(sed -n 's/.*vm_name=\(\w\+\).*/\1/p' "$logfile" | head -1)
test -n "$vm_name"
ip=$(sed -n 's/.*VM_IP=\([0-9\.]\+\).*/\1/p' "$logfile" | head -1)
test -n "$ip"

fedora=$(ssh "root@$ip" 'rpm --eval %fedora')

new_volume_name="copr-builder-$arch-f$fedora-$(date +"%Y%m%d_%H%M%S")"

# we can not just do
# $ nova-3 image-create "$vm_name" "$new_volume_name" --poll
# because it throws error:
# ERROR (ClientException): The server has either erred or is incapable of
# performing the requested operation. (HTTP 500) (Request-ID:...)

nova-3 stop "$vm_name"

cat <<EOF
Please go to https://fedorainfracloud.org/ page, log-in and find the instance

    $vm_name

Check that it is in SHUTOFF state.  Create a snapshot from that instance, name
it "$new_volume_name".  Once snapshot is saved, run:

    $ copr-image-fixup-snapshot-os.sh $new_volume_name

And continue with
https://docs.pagure.org/copr.copr/how_to_upgrade_builders.html#how-to-upgrade-builders
EOF
