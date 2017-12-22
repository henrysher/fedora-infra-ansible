#!/bin/sh

# used as root
# root gpg keychain should have PUBLIC key with `user email` admin@fedoraproject.org

PATH_TO_KEYRING_DIR="/var/lib/copr-keygen"
OUTPUT_FILE="/backup/copr_keygen_keyring.tar.gz.gpg"

tar --exclude="*agent*" -czPf - $PATH_TO_KEYRING_DIR |
  gpg2 --output $OUTPUT_FILE.tmp --encrypt --recipient admin@fedoraproject.org --always-trust &&
  mv $OUTPUT_FILE.tmp $OUTPUT_FILE
