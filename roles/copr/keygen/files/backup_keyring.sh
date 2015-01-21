#!/bin/sh

# used as root
# root gpg keychain should have PUBLIC key with `user email` admin@fedoraproject.org

PATH_TO_KEYRING_DIR="/var/lib/copr-keygen"
OUTPUT_FILE="/backup/copr_keygen_keyring.tar.gz.gpg"

tar -cvzf - $PATH_TO_KEYRING_DIR | gpg2 --output $OUTPUT_FILE --encrypt --recipient admin@fedoraproject.org --always-trust -v
