#!/bin/bash

if [[ "$1" == "org.fedoraproject.prod.buildsys.repo.done" && "$3" == "{{ kojitag }}" ]];then
    # Let us know when the repo finishes rebuilding, so that we can install *all*
    # documents (based on a slightly fragile match)
    echo "Repo_done::start topic=$1; name=$2; instance=$3 " >> /tmp/fedwatch_{{ kojitag }}.log
    echo "* Calling on yum to install all outstanding docs *" >> /tmp/fedwatch{{ kojitag }}.log
    yum --disablerepo=\* --enablerepo={{ kojitag }} clean all 2>&1 >> /tmp/fedwatch_{{ kojitag }}.log
    yum -y --disablerepo=\* --enablerepo={{ kojitag }} install \*-web-[a-z][a-z]\*-[A-Z][A-Z]\*.noarch 2>&1 >> /tmp/fedwatch{{ kojitag }}.log
    echo "Repo_done::end" >> /tmp/fedwatch_{{ kojitag }}.log
elif [[ "$1" == "org.fedoraproject.prod.buildsys.tag" && "$2" == "el6-docs" ]]; then
    # Let us know when packages have been tagged into the {{ kojitag }} tag, just for
    # informational purposes.  We can't install based on this trigger, as we have to wait
    # for the createrepo process to finish
    echo "Tagged::info topic=$1; tag=$2; name=$3; version=$4; release=$5; user=$6" >> /tmp/fedwatch_{{ kojitag }}.log
elif [[ "$1" == "org.fedoraproject.prod.buildsys.untag" ]]; then
    echo "Untagged::start topic=$1; name=$2; version=$3; release=$4; user=$5" >> /tmp/fedwatch_{{ kojitag }}.log
    # fedwatch isn't telling us which repo/tag/target the package is being untagged from, so we have to
    # resort to silly shell games in order to make sure it's really a Publican document
    if [[ $(locale -a | sed -e 's/_/-/' | grep -c $(echo "$2-$3-$4" | sed -r 's/.*-web-([a-z]{2,3}-[A-Z]{2})-.*/\1/')) -gt 0 ]]; then
        if [[ "$5" == "oscar" ]]; then
            # Do not do any removals that are triggered by "oscar", who is the
            # garbage collector in Koji
            echo "* Skipping the removal of $2-$3-$4, because of garbage collection *" >> /tmp/fedwatch{{ kojitag }}.log
        else
            echo "* Calling on yum to remove $3-$4 *" >> /tmp/fedwatch{{ kojitag }}.log
            yum -y remove $3-$4 2>&1 >> /tmp/fedwatch{{ kojitag }}.log
        fi
    else
        echo "* Skipping removal of $2-$3-$4, because it doesn't appear to be a docs package *" >> /tmp/fedwatch{{ kojitag }}.log
    fi
    echo "Untagged::end" >> /tmp/fedwatch{{ kojitag }}.log
else
    # Uncomment this next line for more debugging info
    echo "Unknown::info topic=$1; 2=$2; 3=$3; 4=$4; 5=$5; 6=$6; 7=$7" >> /tmp/fedwatch{{ kojitag }}.log
fi
