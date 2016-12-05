#!/usr/bin/env python
import sys
sys.path.append('/usr/share/modern-paste/app')
from util.cryptography import get_decid
from database.paste import deactivate_paste

print(deactivate_paste(get_decid(sys.argv[1])))
