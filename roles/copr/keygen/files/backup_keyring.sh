#!/bin/sh

# used as root
# root gpg keychain should have PUBLIC key with `user email` infra@fedoraproject.org

PATH_TO_KEYRING_DIR="/var/lib/copr-keygen"
OUTPUT_FILE="/backup/copr_keygen_keyring.tar.gz.gpg"

tar -cvzf - $1 | gpg2 --output $2 --encrypt --recipient infra@fedoraproject.org
