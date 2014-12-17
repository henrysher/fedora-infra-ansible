#!/usr/bin/python
#
# Copyright (c) 2013 Dell, Inc.
#  by Matt Domsch <Matt_Domsch@dell.com>
# Licensed under the MIT/X11 license

# Environment Variables setable via Apache SetEnv directive:
# geoip_city.noreverseproxy
#  if set (to anything), do not look at X-Forwarded-For headers.  This
#  is used in environments that do not have a Reverse Proxy (HTTP
#  accelerator) in front of the application server running this WSGI,
#  to avoid looking "behind" the real client's own forward HTTP proxy.

from string import zfill, atoi, strip, replace
from paste.wsgiwrappers import *
import GeoIP
import json

global gi
gi = GeoIP.open("/usr/share/GeoIP/GeoLiteCity.dat", GeoIP.GEOIP_STANDARD)
gi.set_charset(GeoIP.GEOIP_CHARSET_UTF8)


def real_client_ip(xforwardedfor):
    """Only the last-most entry listed is the where the client
    connection to us came from, so that's the only one we can trust in
    any way."""
    return xforwardedfor.split(',')[-1].strip()

def get_client_ip(environ, request):
    client_ip = None
    request_data = request.GET

    if 'ip' in request_data:
        client_ip = strip(request_data['ip'])
    elif 'X-Forwarded-For' in request.headers and 'geoip_city.noreverseproxy' not in environ:
        client_ip = real_client_ip(strip(request.headers['X-Forwarded-For']))
    else:
        client_ip = request.environ['REMOTE_ADDR']

    client_ip = unicode(client_ip, 'utf8', 'replace')
    return client_ip

def application(environ, start_response):
    request = WSGIRequest(environ)
    response = WSGIResponse()
    code = 500

    try:
        client_ip = get_client_ip(environ, request)
        if client_ip is None:
            code = 400
            raise Exception
        results =  gi.record_by_addr(client_ip)
        if results is None:
            code = 404
            raise Exception
    except: 
        response.status_code=code
        return response(environ, start_response)

    results['ip'] = client_ip
    results = json.dumps(results)
    response.headers['Content-Length'] = str(len(results))
    response.write(results)
    return response(environ, start_response)


if __name__ == '__main__':
    from paste import httpserver
    httpserver.serve(application, host='127.0.0.1', port='8090')
