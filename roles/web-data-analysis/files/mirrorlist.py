#!/usr/bin/python

# This file is part of Fedora Project Infrastructure Ansible
# Repository.
#
# Fedora Project Infrastructure Ansible Repository is free software:
# you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation,
# either version 3 of the License, or (at your option) any later
# version.
#
# Fedora Project Infrastructure Ansible Repository is distributed in
# the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License
# along with Fedora Project Infrastructure Ansible Repository.  If
# not, see <http://www.gnu.org/licenses/>.

import sys
import re
import optparse
import os
import string


'''

Mirror list will go through the file given as an argument and parse
out which releases and architectures were looked for, and by how much.

'''

log_line = [
    r"(?P<host>([\d\.]+|[0-9a-fA-F\:]+))\s",
    r"(?P<identity>\S*)\s",
    r"(?P<user>\S*)\s",
    r"\[(?P<time>.*?)\]\s",
    r'"(?P<request>.*?)"\s',
    r"(?P<status>\d+)\s",
    r"(?P<bytes>\S*)\s",
    r'"(?P<referrer>.*?)"\s',
    r'"(?P<user_agent>.*?)"\s*',
]
pattern = re.compile("".join(log_line))


repo_dict = {
    "epel4" : "epel4",
    "epel4.0" : "epel4",
    "epel4.1" : "epel4",
    "epel4.2" : "epel4",
    "epel4.3" : "epel4",
    "epel4.4" : "epel4",
    "epel4.5" : "epel4",
    "epel4.6" : "epel4",
    "epel4.7" : "epel4",
    "epel4.8" : "epel4",
    "epel4.9" : "epel4",
    "epel4.10" : "epel4",
    "epel4.11" : "epel4",
    "epel4.12" : "epel4",
    "epel4.13" : "epel4",
    "epel4.14" : "epel4",
    "epel4.15" : "epel4",
    "epel4.16" : "epel4",
    "epel4.17" : "epel4",
    "epel4.18" : "epel4",
    "epel4.19" : "epel4",
    "epel4.20" : "epel4",
    "epel5" : "epel5",
    "epel5.0" : "epel5",
    "epel5.1" : "epel5",
    "epel5.2" : "epel5",
    "epel5.3" : "epel5",
    "epel5.4" : "epel5",
    "epel5.5" : "epel5",
    "epel5.6" : "epel5",
    "epel5.7" : "epel5",
    "epel5.8" : "epel5",
    "epel5.9" : "epel5",
    "epel5.10" : "epel5",
    "epel5.11" : "epel5",
    "epel5.12" : "epel5",
    "epel5.13" : "epel5",
    "epel5.14" : "epel5",
    "epel5.15" : "epel5",
    "epel5.16" : "epel5",
    "epel5.17" : "epel5",
    "epel5.18" : "epel5",
    "epel5.19" : "epel5",
    "epel5.20" : "epel5",
    "epel6" : "epel6",
    "epel6.0" : "epel6",
    "epel6.1" : "epel6",
    "epel6.2" : "epel6",
    "epel6.3" : "epel6",
    "epel6.4" : "epel6",
    "epel6.5" : "epel6",
    "epel6.6" : "epel6",
    "epel6.7" : "epel6",
    "epel6.8" : "epel6",
    "epel6.9" : "epel6",
    "epel6.10" : "epel6",
    "epel6.11" : "epel6",
    "epel6.12" : "epel6",
    "epel6.13" : "epel6",
    "epel6.14" : "epel6",
    "epel6.15" : "epel6",
    "epel6.16" : "epel6",
    "epel6.17" : "epel6",
    "epel6.18" : "epel6",
    "epel6.19" : "epel6",
    "epel6.20" : "epel6",
    "epel7" : "epel7",
    "epel7.0" : "epel7",
    "epel7.1" : "epel7",
    "epel7.2" : "epel7",
    "epel7.3" : "epel7",
    "epel7.4" : "epel7",
    "epel7.5" : "epel7",
    "epel7.6" : "epel7",
    "epel7.7" : "epel7",
    "epel7.8" : "epel7",
    "epel7.9" : "epel7",
    "epel7.10" : "epel7",
    "epel7.11" : "epel7",
    "epel7.12" : "epel7",
    "epel7.13" : "epel7",
    "epel7.14" : "epel7",
    "epel7.15" : "epel7",
    "epel7.16" : "epel7",
    "epel7.17" : "epel7",
    "epel7.18" : "epel7",
    "epel7.19" : "epel7",
    "epel7.20" : "epel7",
    "epel8" : "epel8",
    "epel8.0" : "epel8",
    "epel8.1" : "epel8",
    "epel8.2" : "epel8",
    "epel8.3" : "epel8",
    "epel8.4" : "epel8",
    "epel8.5" : "epel8",
    "epel8.6" : "epel8",
    "epel8.7" : "epel8",
    "epel8.8" : "epel8",
    "epel8.9" : "epel8",
    "epel8.10" : "epel8",
    "epel8.11" : "epel8",
    "epel8.12" : "epel8",
    "epel8.13" : "epel8",
    "epel8.14" : "epel8",
    "epel8.15" : "epel8",
    "epel8.16" : "epel8",
    "epel8.17" : "epel8",
    "epel8.18" : "epel8",
    "epel8.19" : "epel8",
    "epel8.20" : "epel8",
    "epel9" : "epel9",
    "epel9.0" : "epel9",
    "epel9.1" : "epel9",
    "epel9.2" : "epel9",
    "epel9.3" : "epel9",
    "epel9.4" : "epel9",
    "epel9.5" : "epel9",
    "epel9.6" : "epel9",
    "epel9.7" : "epel9",
    "epel9.8" : "epel9",
    "epel9.9" : "epel9",
    "epel9.10" : "epel9",
    "epel9.11" : "epel9",
    "epel9.12" : "epel9",
    "epel9.13" : "epel9",
    "epel9.14" : "epel9",
    "epel9.15" : "epel9",
    "epel9.16" : "epel9",
    "epel9.17" : "epel9",
    "epel9.18" : "epel9",
    "epel9.19" : "epel9",
    "epel9.20" : "epel9",
    "rawhide" : "rawhide",
    "frawhide" : "rawhide",
    "rawhide-modular" :  "rawhide-modular",
    "3" : "f03",
    "4" : "f04",
    "5" : "f05",
    "6" : "f06",
    "7" : "f07",
    "8" : "f08",
    "9" : "f09",
    "10" : "f10",
    "11" : "f11",
    "12" : "f12",
    "13" : "f13",
    "14" : "f14",
    "15" : "f15",
    "16" : "f16",
    "17" : "f17",
    "18" : "f18",
    "19" : "f19",
    "20" : "f20",
    "21" : "f21",
    "22" : "f22",
    "23" : "f23",
    "24" : "f24",
    "25" : "f25",
    "26" : "f26",
    "27" : "f27",
    "28" : "f28",
    "29" : "f29",
    "30" : "f30",
    "31" : "f31",
    "32" : "f32",
    "33" : "f33",
    "6.89" : "f07",
    "6.90" : "f07",
    "6.91" : "f07",
    "6.92" : "f07",
    "6.93" : "f07",
    "7.89" : "f08",
    "7.90" : "f08",
    "7.91" : "f08",
    "7.92" : "f08",
    "7.93" : "f08",
    "8.90" : "f09",
    "8.91" : "f09",
    "8.92" : "f09",
    "8.93" : "f09",
    "9.90" : "f10",
    "9.90.1" : "f10",
    "9.91" : "f10",
    "9.92" : "f10",
    "9.93" : "f10",
    "10.89" : "f11",
    "10.90" : "f11",
    "10.91" : "f11",
    "10.92" : "f11",
    "10.93" : "f11",
    "11.89" : "f12",
    "11.90" : "f12",
    "11.91" : "f12",
    "11.92" : "f12",
    "11.93" : "f12",
    "12.89" : "f13",
    "12.90" : "f13",
    "12.91" : "f13",
    "12.92" : "f13",
    "12.93" : "f13",
    "f6.89" : "f07",
    "f6.90" : "f07",
    "f6.91" : "f07",
    "f6.92" : "f07",
    "f6.93" : "f07",
    "f7.89" : "f08",
    "f7.90" : "f08",
    "f7.91" : "f08",
    "f7.92" : "f08",
    "f7.93" : "f08",
    "f8.90" : "f09",
    "f8.91" : "f09",
    "f8.92" : "f09",
    "f8.93" : "f09",
    "f9.90" : "f10",
    "f9.90.1" : "f10",
    "f9.91" : "f10",
    "f9.92" : "f10",
    "f9.93" : "f10",
    "f10.89" : "f11",
    "f10.90" : "f11",
    "f10.91" : "f11",
    "f10.92" : "f11",
    "f10.93" : "f11",
    "f11.89" : "f12",
    "f11.90" : "f12",
    "f11.91" : "f12",
    "f11.92" : "f12",
    "f11.93" : "f12",
    "f12.89" : "f13",
    "f12.90" : "f13",
    "f12.91" : "f13",
    "f12.92" : "f13",
    "f12.93" : "f13",
    'f3'       : 'f03',
    'f4'       : 'f04',
    'f5'       : 'f05',
    'f6'       : 'f06',
    'f7'       : 'f07',
    'f8'       : 'f08',
    'f9'       : 'f09',
    'f03'       : 'f03',
    'f04'       : 'f04',
    'f05'       : 'f05',
    'f06'       : 'f06',
    'f07'       : 'f07',
    'f08'       : 'f08',
    'f09'       : 'f09',
    'f10'       : 'f10',
    'f11'       : 'f11',
    'f12'       : 'f12',
    'f13'       : 'f13',
    'f14'       : 'f14',
    'f15'       : 'f15',
    'f16'       : 'f16',
    'f17'       : 'f17',
    'f18'       : 'f18',
    'f19'       : 'f19',
    'f20'       : 'f20',
    'f21'       : 'f21',
    'f22'       : 'f22',
    'f23'       : 'f23',
    'f24'       : 'f24',
    'f25'       : 'f25',
    'f26'       : 'f26',
    'f27'       : 'f27',
    'f28'       : 'f28',
    'f29'       : 'f29',
    'f30'       : 'f30',
    'f31'       : 'f31',
    'f32'       : 'f32',
    'f33'       : 'f33',
    'fedora-modular-27' : 'modular-f27',
    'fedora-modular-28' : 'modular-f28',
    'fedora-modular-29' : 'modular-f29',
    'fedora-modular-30' : 'modular-f30',
    'fedora-modular-31' : 'modular-f31',
    'fedora-modular-32' : 'modular-f32',
    'fedora-modular-33' : 'modular-f33',
    'modular-f27' : 'modular-f27',
    'modular-f28' : 'modular-f28',
    'modular-f29' : 'modular-f29',
    'modular-f30' : 'modular-f30',
    'modular-f31' : 'modular-f31',
    'modular-f32' : 'modular-f32',
    'modular-f33' : 'modular-f33',
    'rhel4'     : 'rhel4',
    'rhel5'     : 'rhel5',
    'rhel6'     : 'rhel6',
    'rhel7'     : 'rhel7',
    'rhel8'     : 'rhel8',
    'rhel9'     : 'rhel9',
}

repo_keys = repo_dict.keys()

def breakoutdate(givendate):
    Apache_Months = {
        'Jan' : '01',
        'Feb' : '02',
        'Mar' : '03',
        'Apr' : '04',
        'May' : '05',
        'Jun' : '06',
        'Jul' : '07',
        'Aug' : '08',
        'Sep' : '09',
        'Oct' : '10',
        'Nov' : '11',
        'Dec' : '12', 
    }

    date_part = givendate.split()
    
    try:
        [day, month, year] = givendate.split(":")[0].split('/')
    except:
        # string out of index because date corrupted?
        [day, month, year ] = ['01', '01', '1970'] # epoch
    ret_str = "%s-%s-%s" % (year, Apache_Months[month], day)
    return ret_str

def breakoutrepo(request):
    try:
        parts = request.split()[1].split("?")[1].split("&")
        repo=""
        arch=""
        for i in parts:
            if 'repo=' in i:
                repo = i.split('=')[1]
            if 'arch=' in i:
                arch = i.split('=')[1]
        return (repo,arch)
    except:
        return ("unknown_repo","unknown_arch")


def figureoutrepo(asked_repo):

    global repo_dict
    global repo_keys

    crap_chars = ['/', '$', '!', '#', '%', '&', "'", '"', "(", ")", "*", "+", ",", "_", ":", ";", "<", ">", "=", "?", "@", "[", "^", "|"]

    spew = asked_repo.lower()
    for char in crap_chars:
        if char in spew:
            spew.split(char)[0]

    f_phrases = ["core", "fedora", "extras", "legacy", "fc"]

    for word in f_phrases:
        if word in spew:
            spew = spew.replace(word, "f")

    repo_phrases = [".newkey", "install", "alpha", "beta", "client", "debug", "devel", "info", "optional", "preview", "released", "source", "testing", "updates"]

    for word in repo_phrases:
        if word in spew:
            spew = spew.replace(word, "")

    if "centosplus" in spew:
        spew = spew.replace("centosplus", "centos")

    if "client" in spew:
        spew = re.sub("client.*", "", spew)
    if "cloud" in spew:
        spew = re.sub("cloud.*", "", spew)
    if "server" in spew:
        spew = re.sub("server.*", "", spew)
    if "workstation" in spew:
        spew = re.sub("workstation.*", "", spew)
    if "-" in spew:
        spew = re.sub("-+", "", spew)

    sanitize = spew.strip()

    if sanitize in repo_dict.keys():
        return repo_dict[sanitize]
    else:
        # sys.stderr.write("asked_repo: %s. Thought it was %s\n" % (asked_repo,spew))
        return "unknown_repo"


def figureoutarch(asked_arch):
    arch_dict = {
        'i386' : 'i386',
        'i486' : 'i386',
        'i586' : 'i386',
        'i686' : 'i386',
        'athlon' : 'i386',
        'pentium' : 'i386',
        'pentium3' : 'i386',
        'pentium4' : 'i386',
        'pentium5' : 'i386',
        'ia32' : 'i386',
        'x86_32' : 'i386',
        'x86_64' : 'x86_64',
        'amd64' : 'x86_64',
        'aarch64' : 'aarch64',
        'alpha' : 'alpha',
        'arm' : 'arm',
        'arm64' : 'aarch64',
        'armhfp' : 'arm',
        'armv3l' : 'arm',
        'armv5tel' : 'arm',
        'armv7hl' : 'arm',
        'ia64' : 'ia64',
        'mips' : 'mips',
        'mips64' : 'mips64',
        'mips64el' : 'mips64',
        'powepc' : 'ppc',
        'ppc' : 'ppc',
        'ppc32' : 'ppc',
        'ppc64' : 'ppc64',
        'ppc64le' : 'ppc64le',
        's390' : 's390',
        's390x' : 's390',
        'sparc' : 'sparc',
        'sparc64' : 'sparc64',
        'tilegx' : 'tilegx',
    }
    spew = asked_arch.split("/")[0]
    spew = spew.split("!")[0]
    spew = spew.split("#")[0]
    spew = spew.split("%")[0]
    spew = spew.split("&")[0]
    spew = spew.split("'")[0]
    spew = spew.split("(")[0]
    spew = spew.split("*")[0]
    spew = spew.split("+")[0]
    spew = spew.split(",")[0]
    spew = spew.split("-")[0]
    spew = spew.split(".")[0]
    spew = spew.split(":")[0]
    spew = spew.split(";")[0]
    spew = spew.split("<")[0]
    spew = spew.split("=")[0]
    spew = spew.split(">")[0]
    spew = spew.split("?")[0]
    spew = spew.split("@")[0]
    spew = spew.split("[")[0]
    spew = spew.split("]")[0]
    spew = spew.split("^")[0]
    spew = spew.split('"')[0]
    spew = spew.split('\\')[0]
    spew = spew.split('|')[0]
    spew = spew.split('$')[0]
    sanitize = spew.lower()

    if sanitize in arch_dict.keys():
        return arch_dict[sanitize]
    else:
        #sys.stderr.write("asked_arch: %s\n" % asked_arch)
        return "unknown_arch"

def parseline(our_line):

    ##
    ## Figure out if line is something we want to work on more
    global pattern

    if (('/metalink' in our_line) or ('/mirrorlist' in our_line)):
        our_blob = pattern.match(our_line)
        if our_blob:
            our_dict = our_blob.groupdict()
            ip       = our_dict['host']
            time     = breakoutdate(our_dict['time']) 
            r,a      = breakoutrepo(our_dict['request'])
            repo     = figureoutrepo(r)
            arch     = figureoutarch(a)
            return "%s %s %s %s" % (time,ip,repo,arch)
        else:
            return ""
    else:
        return ""


def parselog(our_file, out_file):
    our_file = our_file
    yumclients_set = set()
    output_file = out_file
    try:
        data = open(our_file, "r")
    except:
        sys.stderr.write("Unable to open %s\n" % our_file )
        sys.exit(-1)

    for line in data:
        parsed = parseline(line)
        if parsed == "":
            pass
        else:
            yumclients_set.add(parsed)

    data.close()

    our_list = list(yumclients_set)
    our_list.sort()
    
    try:
        output = open(output_file,"a")
        sys.stderr.write("Outputting data: %s\n" % our_file)
    except:
        sys.stderr.write("Unable to open outputfile\n")
        sys.exit(-1)

    for line in our_list:
        output.write(line + os.linesep)
    output.close()
    return


def main():
    parser = optparse.OptionParser(
        description = "A program to parse Fedora mirrorlist apache common log format files.",
        prog = "mirrorlist.py",
        version = "1.0.2",
        usage = "%prog [-o output-filename] logfile1 [logfile2...]"
    )

    parser.add_option("-o", "--output",
                      default = "output.txt",
                      help = "Sets the name of the output file for the run.",
                      dest = "output")


    (options, args) = parser.parse_args()
    if options.output:
        out_file = options.output
    else:
        out_file = "output.txt"

    for our_file in args:
        parselog(our_file,out_file)


if __name__ == '__main__':
    main()
