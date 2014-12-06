#!/usr/bin/python
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Copyright 2005 Dan Williams <dcbw@redhat.com> and Red Hat, Inc.


import sys, os, tempfile

OPENSSL_PROG = '/usr/bin/openssl'

def print_usage(prog):
    print "\nUsage:\n"
    print "  %s ca --outdir=<outdir> --name=<name>\n" % prog
    print "  %s normal --outdir=<outdir> --name=<name> --cadir=<cadir> --caname=<ca-name>" % prog
    print ""
    print "        Types:"
    print "           ca       - Build system Certificate Authority key & certificate"
    print "           normal   - Key & certificate that works with the build server and builders"
    print ""
    print "Examples:\n"
    print "    %s ca --outdir=/etc/plague/ca --name=my_ca" % prog
    print "    %s normal --outdir=/etc/plague/server/certs --name=server --cadir=/etc/plague/ca --caname=my_ca" % prog
    print "    %s normal --outdir=/etc/plague/builder/certs --name=builder1 --cadir=/etc/plague/ca --caname=my_ca" % prog
    print "\n"


class CertHelperException:
    def __init__(self, message):
        self.message = message


class CertHelper:
    def __init__(self, prog, outdir, name):
        self._prog = prog
        self._outdir = outdir
        self._name = name

    def dispatch(self, cmd, argslist):
        if cmd.lower() == 'ca':
            self._gencert_ca(argslist)
        elif cmd.lower() == 'normal':
            self._gencert_normal(argslist)
        else:
            print_usage(self._prog)

    def _gencert_ca(self, args):
        # Set up CA directory
        if not os.path.exists(self._outdir):
            os.makedirs(self._outdir)
        try:
            os.makedirs(os.path.join(self._outdir, 'certs'))
            os.makedirs(os.path.join(self._outdir, 'crl'))
            os.makedirs(os.path.join(self._outdir, 'newcerts'))
            os.makedirs(os.path.join(self._outdir, 'private'))
        except:
            pass
        cert_db = os.path.join(self._outdir, "index.txt")
        os.system("/bin/touch %s" % cert_db)
        serial = os.path.join(self._outdir, "serial")
        if not os.path.exists(serial):
            os.system("/bin/echo '01' > %s" % serial)

        cnf = write_openssl_cnf(self._outdir, self._name, {})

        # Create the CA key
        key_file = os.path.join(self._outdir, "private", "cakey.pem")
        cmd = "%s genrsa -out %s 4096" % (OPENSSL_PROG, key_file)
        if os.system(cmd) != 0:
            raise CertHelperException("\n\nERROR: Command '%s' was not successful.\n" % cmd)

        # Make the self-signed CA certificate
        cert_file = os.path.join(self._outdir, "%s_ca_cert.pem" % self._name)
        cmd = "%s req -config %s -new -x509 -days 3650 -key %s -out %s -extensions v3_ca" % (OPENSSL_PROG, cnf, key_file, cert_file)
        if os.system(cmd) != 0:
            raise CertHelperException("\n\nERROR: Command '%s' was not successful.\n" % cmd)

        os.remove(cnf)
        print "Success.  Your Certificate Authority directory is: %s\n" % self._outdir

    def _gencert_normal(self, args):
        cadir = argfind(args, 'cadir')
        if not cadir:
            print_usage(self._prog)
            sys.exit(1)
        caname = argfind(args, 'caname')
        if not caname:
            print_usage(self._prog)
            sys.exit(1)

        cnf = write_openssl_cnf(cadir, caname, self._name, {})

        # Generate key
        key_file = os.path.join(self._outdir, "%s_key.pem" % self._name)
        cmd = "%s genrsa -out %s 4096" % (OPENSSL_PROG, key_file)
        if os.system(cmd) != 0:
            raise CertHelperException("\n\nERROR: Command '%s' was not successful.\n" % cmd)
        print ""

        # Generate the certificate request
        req_file = os.path.join(self._outdir, "%s_req.pem" % self._name)
        cmd = '%s req -config %s -new -nodes -out %s -key %s' % (OPENSSL_PROG, cnf, req_file, key_file)
        if os.system(cmd) != 0:
            raise CertHelperException("\n\nERROR: Command '%s' was not successful.\n" % cmd)
        print ""

        # Sign the request with the CA's certificate and key
        cert_file = os.path.join(self._outdir, "%s_cert.pem" % self._name)
        cmd = '%s ca -config %s -days 3650 -out %s -infiles %s' % (OPENSSL_PROG, cnf, cert_file, req_file)
        if os.system(cmd) != 0:
            raise CertHelperException("\n\nERROR: Command '%s' was not successful.\n" % cmd)
        print ""

        # Cat the normal cert and key together
        key_and_cert = os.path.join(self._outdir, "%s_key_and_cert.pem" % self._name)
        cmd = '/bin/cat %s %s > %s' % (key_file, cert_file, key_and_cert)
        if os.system(cmd) != 0:
            raise CertHelperException("\n\nERROR: Command '%s' was not successful.\n" % cmd)

        # Cleanup: remove the cert, key, and request files
        cmd = "/bin/rm -f %s %s %s" % (key_file, req_file, cert_file)
        if os.system(cmd) != 0:
            raise CertHelperException("\n\nERROR: Command '%s' was not successful.\n" % cmd)

        os.remove(cnf)
        print "Success.  Your certificate and key file is: %s\n" % key_and_cert


def write_openssl_cnf(home, ca_name, commonname, opt_dict):
    (fd, name) = tempfile.mkstemp('', 'openssl_cnf_', dir=None, text=True)
    os.write(fd, """
##############################
HOME = %s
RANDFILE = .rand

##############################
[ ca ]
default_ca = CA_default\n

##############################
[ CA_default ]

dir = $HOME
certs = $dir/certs
crl_dir = $dir/crl
database = $dir/index.txt
new_certs_dir = $dir/newcerts

certificate = $dir/cacert.pem
private_key = $dir/private/cakey.pem
serial = $dir/serial
crl = $dir/crl.pem

x509_extensions	= usr_cert

name_opt 	= ca_default
cert_opt 	= ca_default

default_days	= 3650
default_crl_days= 30
default_md	= sha256
preserve	= no

policy		= policy_match

[ policy_match ]
countryName		= match
stateOrProvinceName	= match
organizationName	= match
organizationalUnitName	= optional
commonName		= supplied
emailAddress		= optional

##############################
[ req ]
default_bits		= 4096
default_keyfile 	= privkey.pem
distinguished_name	= req_distinguished_name
attributes		= req_attributes
x509_extensions	= v3_ca	# The extentions to add to the self signed cert

string_mask = MASK:0x2002

[ req_distinguished_name ]
countryName			= Country Name (2 letter code)
countryName_default		= US
countryName_min			= 2
countryName_max			= 2

stateOrProvinceName		= State or Province Name (full name)
stateOrProvinceName_default	= North Carolina

localityName			= Locality Name (eg, city)
localityName_default		= Raleigh

0.organizationName		= Organization Name (eg, company)
0.organizationName_default	= Fedora Project

organizationalUnitName		= Organizational Unit Name (eg, section)
organizationalUnitName_default	= Fedora Builders

commonName			= Common Name (eg, your name or your server\'s hostname)
commonName_default		= %s
commonName_max			= 64

emailAddress			= Email Address
emailAddress_max		= 64
emailAddress_default		= buildsys@fedoraproject.org

[ req_attributes ]
challengePassword		= A challenge password
challengePassword_min		= 4
challengePassword_max		= 20

unstructuredName		= An optional company name

##############################
[ usr_cert ]

basicConstraints=CA:FALSE
nsComment			= "OpenSSL Generated Certificate"
subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid,issuer:always

##############################
[ v3_ca ]

subjectKeyIdentifier=hash
authorityKeyIdentifier=keyid:always,issuer:always
basicConstraints = CA:true

""" % (home, commonname ))

    return name

def argfind(arglist, prefix):
    val = None
    for arg in arglist:
        if arg.startswith('--%s=' % prefix):
            val = arg
            break
    if not val:
        return None
    val = val.replace('--%s=' % prefix, '')
    return val

if __name__ == '__main__':
    prog = sys.argv[0]
    if len(sys.argv) < 3:
        print_usage(prog)
        sys.exit(1)

    outdir = argfind(sys.argv, 'outdir')
    if not outdir:
        print_usage(prog)
        sys.exit(1)

    name = argfind(sys.argv, 'name')
    if not name:
        print_usage(prog)
        sys.exit(1)

    ch = CertHelper(prog, outdir, name)
    try:
        ch.dispatch(sys.argv[1], sys.argv)
    except CertHelperException, e:
        print e.message
        sys.exit(1)

    sys.exit(0)

