import socket

hostname = socket.gethostname().split('.', 1)[0]

config = {
    "name": "koschei.%s" % hostname,
}
