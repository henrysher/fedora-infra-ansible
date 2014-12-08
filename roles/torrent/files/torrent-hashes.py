#!/usr/bin/python
# by Matt Domsch
# License: BitTorrent
#
# This simply prints the bittorrent hashes for each file
# to stdout or an output file.
# To be used as the whitelist with opentracker

import os
import sys
import hashlib
from optparse import OptionParser
from BitTorrent.bencode import bencode, bdecode
from BitTorrent.btformats import check_message

def torrent_hash(fname):
    f = open(fname, 'rb')
    d = bdecode(f.read())
    f.close()
    check_message(d)
    hash = hashlib.sha1(bencode(d['info'])).hexdigest().upper()
    fn = os.path.basename(fname)
    return '%s - %s' % (hash,fn)

def main():
    parser = OptionParser(usage=sys.argv[0] + " [options] [torrentfiles] ...")
    parser.add_option("-o", "--output", type="string", metavar="FILE",
                      dest="output", default='-',
                      help="write hashes to FILE, default=stdout")
    (options, args) = parser.parse_args()

    outfd = sys.stdout
    if options.output != '-':
        try:
            outfd = open(options.output, 'w')
        except:
            sys.stderr.write("Error: unable to open output file %s\n" % options.output)
            return 1
    
    for a in args:
        try:
            hash = torrent_hash(a)
            outfd.write(hash + '\n')
        except:
            sys.stderr.write("Error reading hash from %s\n" % a)

    return 0

if __name__ == "__main__":
    sys.exit(main())
