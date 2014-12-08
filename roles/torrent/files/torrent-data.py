#!/usr/bin/python -tt

import os
import sys
import  BitTorrent
import BitTorrent.bencode
import simplejson

# grab bttrack.dat
# dump out, per torrent stats:
# total completed downloads
# active number of downloaders
# active number of seeds

class TorrentObj(object):
    def __init__(self, fn, encode_name, name):
        self.fn = fn
        self.encode_name = encode_name
        self.name = name
        self.downloaders = 0
        self.seeds = 0
        self.size = 0L
        self.completed = 0
    
    def __cmp__(self, other):
        return cmp(self.name, other.name)
    
    def json_obj(self):
        obj = {'size':self.size, 
                 'completed':self.completed, 
                 'seeds':self.seeds, 
                 'downloaders':self.downloaders, 
                 'name':self.name}
        return obj
        
    
def main(args):
    bttrack = args[0]
    outputfile = args[1]
    
    if not os.path.exists(bttrack):
        print "Data file %s does not exist" % bttrack
        sys.exit(1)

    bt = BitTorrent.bencode.bdecode(open(bttrack, 'rb').read())
    torrents = []
    
    for encode_name in bt['allowed'].keys():
        tor = bt['allowed'][encode_name]
        torobj = TorrentObj(tor['file'], encode_name, tor['name'])
        torobj.size = tor['length']

        if bt['completed'].has_key(torobj.encode_name):
            torobj.completed = int(bt['completed'][torobj.encode_name])
        
        if bt['peers'].has_key(torobj.encode_name):
            peers = bt['peers'][torobj.encode_name]
            for peer_dict in peers.values():
                if peer_dict['left'] == 0:
                    torobj.seeds += 1
                else:
                    torobj.downloaders += 1
                
        torrents.append(torobj)
        
    # write out to outputfile
    # torrent-name: size, finished, downloaders, seeds

    of = open(outputfile, 'w')
    #of.write('#torrentname:size:completed:downloaders:seeders\n')
    json_torrents = [ tor.json_obj() for tor in torrents ]
    #for tor in sorted(torrents):
        #of.write('%s:%s:%s:%s:%s\n' % (tor.name, tor.size, tor.completed, 
        #                          tor.downloaders, tor.seeds))
    simplejson.dump(json_torrents, of)
        
    
    of.close()
    
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print "usage: torrent-data.py bttrack.dat output_filename"
        sys.exit(1)
    main(sys.argv[1:])
    
    
