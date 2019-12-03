#! /bin/bash

# Automatically create an updated virtual machine in OpenStack or AWS so we can
# later create a snapshot (builder image) from it.  See
# https://docs.pagure.org/copr.copr/how_to_upgrade_builders.html

. /home/copr/cloud/keystonerc_proper_tenant

set -e

parse_first_argument()
{
    old_IFS=$IFS
    IFS=:
    set -- $1
    if test -z $2; then
        # cloud not specified, default to openstack
        cloud=os
        arch=$1
    else
        cloud=$1
        arch=$2
    fi
    IFS=$old_IFS
}

parse_first_argument "$1"

die() { echo "$*" >&2 ; exit 1 ; }

case $cloud:$arch in
    os:ppc64le) playbook=/home/copr/provision/builderpb_nova_ppc64le.yml ;;
    os:x86_64)  playbook=/home/copr/provision/builderpb_nova.yml ;;
    aws:x86_64) playbook=/home/copr/provision/builderpb-aws-x86_64.yml ;;
    aws:aarch64) playbook=/home/copr/provision/builderpb-aws-aarch64.yml ;;
    *) die "bad cloud ($cloud) or architecture ($arch)" ;;
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

if test $cloud = os; then
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
elif test $cloud = aws; then
    instance_id=$(aws ec2 describe-instances \
        --query "Reservations[].Instances[].InstanceId" \
        --filter Name=tag-key,Values=Name,Name=tag-value,Values="$vm_name" \
        --output text
    )

    # search results can be empty, and that would be error
    test -n "$instance_id"

    image_id=$(aws ec2 create-image \
        --instance-id "$instance_id" \
        --name "$new_volume_name" \
        --output text
    )

    # This makes the web-UI nicer (first field of AMI list)
    aws ec2 create-tags \
        --resources "$image_id" \
        --tags Key=Name,Value="$new_volume_name"

    # This is required so fedora infra people won't delete the images
    # automatically
    aws ec2 create-tags \
        --resources "$image_id" \
        --tags Key=FedoraGroup,Value=copr
fi
