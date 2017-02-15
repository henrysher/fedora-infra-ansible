import socket

config = {
    # So that the MBS can find it's cert in /etc/fedmsg.d/ssl.py
    'cert_prefix': 'mbs',
    'name': 'mbs-%s' % socket.gethostname(),
}
