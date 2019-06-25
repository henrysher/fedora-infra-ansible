#!/bin/bash
HOMEDIR=/mnt/fedora/app/fi-repo/rhel/rhel8
BINDIR=/usr/local/bin

ARCHES="aarch64 ppc64le s390x x86_64"
DATE=$(date -Ih | sed 's/+.*//')

DATEDIR=${HOMEDIR}/koji/${DATE}

if [ -d ${DATEDIR} ]; then
    echo "Directory already exists. Please remove or fix"
    exit
else
mkdir -p ${DATEDIR}
fi

for ARCH in ${ARCHES}; do
    # The archdir is where we daily download updates for rhel8
    ARCHDIR=${HOMEDIR}/${ARCH}
    if [ ! -d ${ARCHDIR} ]; then
	echo "Unable to find ${ARCHDIR}"
	exit
    fi

    # We consolidate all of the default repositories and remerge them
    # in a daily tree. This allows us to point koji at a particular
    # day if we have specific build concerns.
    OUTDIR=${DATEDIR}/${ARCH}
    mkdir -vp ${OUTDIR}
    if [ ! -d ${OUTDIR} ]; then
	echo "Unable to find ${ARCHDIR}"
	exit
    else
	cd ${OUTDIR}
    fi

    # Begin splitting the various packages into their subtrees
    ${BINDIR}/splitter.py --action hardlink --target RHEL-8-001 ${ARCHDIR}/rhel-8-for-${ARCH}-baseos-rpms/ --only-defaults &> /dev/null
    if [ $? -ne 0 ]; then
	echo "splitter ${ARCH} baseos failed"
	exit
    fi
    ${BINDIR}/splitter.py --action hardlink --target RHEL-8-002 ${ARCHDIR}/rhel-8-for-${ARCH}-appstream-rpms/ --only-defaults &> /dev/null
    if [ $? -ne 0 ]; then
	echo "splitter ${ARCH} appstream failed"
	exit
    fi
    ${BINDIR}/splitter.py --action hardlink --target RHEL-8-003 ${ARCHDIR}/codeready-builder-for-rhel-8-${ARCH}-rpms/ &> /dev/null
    if [ $? -ne 0 ]; then
	echo "splitter ${ARCH} codeready failed"
	exit
    fi

    # Copy the various module trees into RHEL-8-001 where we want them
    # to work.
    echo "Moving data to ${ARCH}/RHEL-8-001"
    cp -anlr RHEL-8-002/* RHEL-8-001
    cp -anlr RHEL-8-003/* RHEL-8-001
    # Go into the main tree
    pushd RHEL-8-001

    # Mergerepo didn't work so lets just createrepo in the top directory.
    createrepo_c .  &> /dev/null
    popd

    # Cleanup the trash 
    rm -rf RHEL-8-002 RHEL-8-003
#loop to the next
done

## Set up the builds so they are pointing to the last working version
cd ${HOMEDIR}/koji/
if [[ -e staged ]]; then
    if [[ -h staged ]]; then
	rm -f staged
    else
	echo "Unable to remove staged. it is not a symbolic link"
	exit
    fi
else
    echo "No staged link found"
fi

echo "Linking ${DATE} to staged"
ln -s ${DATE} staged


for ARCH in ${ARCHES}; do
    pushd latest/
    mkdir -p $ARCH
    dnf --disablerepo=\* --enablerepo=RHEL-8-001 --repofrompath=RHEL-8-001,https://infrastructure.fedoraproject.org/repo/rhel/rhel8/koji/staged/${ARCH}/RHEL-8-001/ reposync -a ${ARCH} -a noarch -p ${ARCH} --newest --delete  &> /dev/null
    cd RHEL-8-001
    createrepo_c .  &> /dev/null
    popd
done
