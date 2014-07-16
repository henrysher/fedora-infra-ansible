config = {
    # Tell fedmsg-gateway where its special outgoing port is.
    'fedmsg.consumers.gateway.port': 9940,

    # Set this number to near, but not quite the fs.file-limit.  Try 160000.
    'fedmsg.consumers.gateway.high_water_mark': 160000,
}
