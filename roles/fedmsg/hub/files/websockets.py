config = {
    # The presence of this will cause fedmsg-hub to start its own websocket
    # server along with it.
    'moksha.livesocket.websocket.port': 9919,
}

# And... this is a hack to get python-txws to work with python-six on epel7
import six
six.PY2 = not six.PY3
