#! /usr/bin/env python
import os
import re
import collections

# constants
PING_HOST_RESPONSE = 0
PING_COMMAND = "ping -c 1 -W 1 {0} > /dev/null 2>&1"
ZONE_REGEX = "(\S+)\s+IN\s+([A-Z]+)\s+(\S+)"
DNS_REGEX = "([a-z0-9._-]+)$"

ZONE_FILENAMES = [
	"master/125.5.10.in-addr.arpa",
	"master/126.5.10.in-addr.arpa",
	"master/127.5.10.in-addr.arpa",
	"master/phx2.fedoraproject.org"
]

AddressRecord = collections.namedtuple('AddressRecord', 'host, type, value')

def get_host_dict(fp, prefix):
	hosts = dict()

	# get the hostnames from the file
	pattern = re.compile(ZONE_REGEX)
	for line in fp:
		m = pattern.match(line)
		if m:
			full_host = prefix.format(m.group(1))
			if full_host[0] <> ';':
				hosts[full_host] = AddressRecord._make( [full_host, m.group(2), m.group(3)] )
	return hosts

def check_zones_match(fwd_hosts, rev_hosts):
	results = {}
	results["correct"] = []
	results["mismatch"] = []
	results["missing"] = []

	for record in fwd_hosts.values():
		if record.type is 'A':
			try:
				rev_record = rev_hosts[record.value]
				if record.host == rev_record.value:
					results["correct"].append( (record, rev_record) )
				else:
					results["mismatch"].append( (record, rev_record) )
			except KeyError:
				results["missing"].append( (record, None) )
	return results

# ping each host and record the result
def ping(hosts):
	results = {}
	for record in hosts.values():
		results[record] = os.system(PING_COMMAND.format(record.host) )
	return results

def build_dns_suffix(filename, reverse=False):
	m = re.search(DNS_REGEX, filename)
	if m:
		suffix = m.group(1)
		if reverse:
			parts = suffix.split(".")
			return parts[2]+"."+parts[1]+"."+parts[0]+".{0}"
		else:
			return "{0}."+m.group(1)+"."

def main(filenames, check_dns=True, ping_hosts=True, print_stats=False):
	rev_hosts = {}
	fwd_hosts = {}

	for filename in filenames:
		is_reverse = filename.endswith(".in-addr.arpa")
		suffix = build_dns_suffix(filename, is_reverse)
		host_dict = get_host_dict(open(filename, "r"), suffix)

		type_dict = rev_hosts if is_reverse else fwd_hosts
		type_dict.update(host_dict)

	if check_dns:
		check_results = check_zones_match(fwd_hosts, rev_hosts)

		if print_stats:
			print("reverse dns records")
			print("records correct: {0}".format(len(check_results["correct"])))
			print("records incorrect: {0}".format(len(check_results["mismatch"])))
			print("records missing: {0}".format(len(check_results["missing"])))

		for (fwd, rev) in check_results["mismatch"]:
			print ("mismatched record: {0} -> {1} -> {2}".format(fwd.host, fwd.value, rev.value))

		for (fwd, rev) in check_results["missing"]:
			print ("missing record: {0} -> {1}").format(fwd.host, fwd.value)

	if ping_hosts:
		results = ping(fwd_hosts)

		# print all the non-zero (error) results
		for (host, result) in results.items():
			if result is not 0:
				print ("ping failed: {0} (err {1})").format(host.host[:-1], result)

main(ZONE_FILENAMES)
