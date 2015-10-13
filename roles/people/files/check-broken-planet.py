#!/usr/bin/python
"""
Script to check broken URLs configured on Fedora Planet.
The script check all the .planet files of the users and check if the URL
configured is working or not and generate a report with the broken ones.
Daniel Bruno <dbruno@fedoraproject.org>
"""
import os
import urllib2
import re
import time
import json
import sys

try:
    env = sys.argv[1]
    user = sys.argv[2]
except:
    env = 'prd'

PLANET_FILE = '.planet'
HOME = '/home/fedora'

date = time.strftime("%d_%m_%Y")

# Define environment for dev purposes, to avoid code change only to test
if env == 'prd':
    report_file_name = '/srv/planet/output/reports/brokenplanetreport'+date+'.txt' 
    reporte_list_file_name = '/srv/planet/output/reports/brokenplanetreport'+date+'.json'
elif env == 'dev':
    report_file_name = '/home/fedora/'+user+'/public_html/reports/brokenplanetreport'+date+'.txt' 
    reporte_list_file_name = '/home/fedora/'+user+'/public_html/reports/brokenplanetreport'+date+'.json'
else:
    # For some reason any environment was set
    sys.exit(1)

report_file = open(report_file_name,'w')
report_list_file = open(reporte_list_file_name,'w')
report_list = {}

USER_AGENT = 'Fedora Planet'
headers = { 'User-Agent': USER_AGENT }

http_status = {100: "100 Continue", 101: "101 Switching Protocols",\
 102: "102 Processing (WebDAV; RFC 2518)", 200: "200 OK", 201: "201 Created",\
 202: "202 Accepted", 203: "203 Non-Authoritative Information (since HTTP/1.1)",\
 204: "204 No Content", 205: "205 Reset Content", 206: "206 Partial Content",\
 207: "207 Multi-Status (WebDAV; RFC 4918)", 208: "208 Already Reported (WebDAV; RFC 5842)",\
 226: "226 IM Used (RFC 3229)", 300: "300 Multiple Choices", 301: "301 Moved Permanently",\
 302: "302 Found", 303: "302 Found", 304: "304 Not Modified", 305: "305 Use Proxy",\
 306: "306 Switch Proxy", 307: "307 Temporary Redirect", 308: "307 Temporary Redirect ",\
 400: "400 Bad Request", 401: "401 Unauthorized", 402: "402 Payment Required",\
 403: "403 Forbidden", 404: "404 Not Found", 405: "405 Method Not Allowed",\
 406: "406 Not Acceptable", 407: "407 Proxy Authentication Required",\
 408: "408 Request Timeout", 409: "409 Conflict", 410: "410 Gone",\
 411: "411 Length Required", 412: "412 Precondition Failed",\
 413: "413 Request Entity Too Large", 414: "414 Request-URI Too Long",\
 415: "Unsupported Media Type", 416: "Requested Range Not Satisfiable",\
 417: "Expectation Failed", 418: "I'm a teapot (RFC 2324)",\
 419: "Authentication Timeout (not in RFC 2616)", 420: "Method Failure (Spring Framework)",\
 420: "Enhance Your Calm (Twitter)", 422: "Unprocessable Entity (WebDAV; RFC 4918)",\
 423: "Locked (WebDAV; RFC 4918)", 424: "Failed Dependency (WebDAV; RFC 4918)",\
 426: "Upgrade Required", 428: "Precondition Required (RFC 6585)", 
 429: "Too Many Requests (RFC 6585)", 431: "Request Header Fields Too Large (RFC 6585)",\
 440: "Login Timeout (Microsoft)", 444: "No Response (Nginx)", 449: "Retry With (Microsoft)",\
 450: "Blocked by Windows Parental Controls (Microsoft)", 451: "Unavailable For Legal Reasons",\
 451: "Redirect (Microsoft)", 494: "Request Header Too Large (Nginx)",\
 495: "Cert Error (Nginx)", 496: "No Cert (Nginx)", 497: "HTTP to HTTPS (Nginx)",\
 498: "Token expired/invalid (Esri)", 499: "Client Closed Request (Nginx)",\
 499: "Token required (Esri)", 500: "Internal Server Error", 501: "Not Implemented",\
 502: "Bad Gateway", 503: "Service Unavailable", 504: "Gateway Timeout",\
 505: "HTTP Version Not Supported", 506: "Variant Also Negotiates (RFC 2295)",\
 507: "Insufficient Storage (WebDAV; RFC 4918)", 508: "Loop Detected (WebDAV; RFC 5842)",\
 509: "Bandwidth Limit Exceeded (Apache bw/limited extension)", 510: "Not Extended (RFC 2774)",\
 511: "Network Authentication Required (RFC 6585)", 520: "Origin Error (CloudFlare)",\
 521: "Web server is down (CloudFlare)", 522: "Connection timed out (CloudFlare)",\
 523: "Proxy Declined Request (CloudFlare)", 524: "A timeout occurred (CloudFlare)",\
 598: "Network read timeout error (Unknown)", 599: "Network connect timeout error (Unknown)"}


for user in os.listdir(HOME):
	PLANET_PATH_FILE = HOME+'/'+user+'/'+PLANET_FILE
	error_message = None
	
	# The .planet exists?
	if os.path.isfile(PLANET_PATH_FILE) == True:
		
	 	# considering that the URL isn't in the 1st line, let's find it
	 	for line in open(PLANET_PATH_FILE).readlines():
	 		if re.search(r'\[', line) is not None and\
	 		not line.startswith('#'): # avoid comment lines
	 			planet_url = line.translate(None, '[]').replace('\n', '')

		# begin the test
		try:
			request = urllib2.Request(planet_url, None, headers)
			urllib2.urlopen(request)
		except urllib2.HTTPError, errhttp:
			message = 'User: %s\nURL: %s\nError: %s\n' % (user, planet_url, http_status[errhttp.code])
			
			report_list['user'] = user
			report_list['url'] = planet_url
			report_list['error'] = http_status[errhttp.code]
			
			json.dump(report_list, report_list_file)
			report_list_file.write('\n')
			report_file.write(message)
			report_file.write("\n")
		except urllib2.URLError, errurl:
			message = 'User: %s\nURL: %s\nError: %s\n' % (user, planet_url, errurl.reason)
			
			report_list['user'] = user
			report_list['url'] = planet_url
			report_list['error'] = '%s' % errurl.reason
			
			json.dump(report_list, report_list_file)
			report_list_file.write('\n')
			report_file.write(message)
			report_file.write("\n")
		except Exception, err:
			message = 'User: %s\nURL: %s\nError: %s\n' % (user, planet_url, err)
						
			report_list['user'] = user
			report_list['url'] = planet_url
			report_list['error'] = '%s' % err
			
			json.dump(report_list, report_list_file)
			report_list_file.write('\n')
			report_file.write(message)
			report_file.write("\n")

report_list_file.close()
report_file.close()
