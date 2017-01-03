#!/usr/bin/env python
import sys
sys.path.append('/usr/share/modern-paste/app')
from util.cryptography import get_decid
from database.paste import get_paste_by_id

paste_id = get_decid(sys.argv[1])
paste = get_paste_by_id(paste_id)

print('Decrypted ID: ' + str(paste_id))
print('Title       : ' + paste.title)
print('Language    : ' + paste.language)
print('Views       : ' + str(paste.views))
print('Contents    : \n' + paste.contents)
