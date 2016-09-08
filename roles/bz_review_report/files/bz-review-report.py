#!/usr/bin/env python
#
# Copyright 2008, 2009 Rakesh Pandit <rakesh@fedoraproject.org>
# Addions by Brennan Ashton <bashton@brennanashton.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with translate; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import sys
import os
import time
import datetime
import xmlrpclib
import tempfile
import socket

from optparse import OptionParser
from bugzilla import Bugzilla
from ConfigParser import ConfigParser


def checkdateInBetween(date, start_date, end_date):
    """ """
    date_string = date.__str__()
    date = datetime.datetime(*(time.strptime(date_string, "%Y%m%dT%H:%M:%S")[0:5]))
    if date >= start_date and date < end_date:
        return True
    return False


def getDateTime(date_string):
    """ """
    try:
        if "/" in date_string:
            date_format = "%d/%m/%Y"
        else:
            date_format = "%Y-%m-%d"
        return datetime.datetime(*time.strptime(date_string, date_format)[0:5])
    except ValueError:
        print "Error: Date string", date_string, "is wrong. Please check."
        exit(1)


def getBugInfo(bz, bug_id, flag, start, end):
    """ """
    result = {}
    bug = bz.getbug(bug_id)

    result["summary"] = bug.summary
    if flag == "new":
        result["who"] = bug.creator
        result["date"] = True
    else:
        history = bug.get_history()
        dict_changes = history["bugs"][0]["history"]
        for record in dict_changes:
            when = record["when"]
            who = record["who"]
            for each_change in record["changes"]:
                added = each_change["added"]
                if flag in added:
                    result["who"] = who
                    result["date"] = checkdateInBetween(when, start, end)
                    return result
    return result


def getComments(bz, bug_list, start, end):
    """ """
    if not bz.logged_in:
        print >> sys.stderr, "Authentication is required to fetch the comments."
        exit(1)

    com_result = {}
    bug_com_list = []

    for bug in bug_list:
        c_id = 0
        for comment in bug.getcomments():
            author = comment['author']
            if checkdateInBetween(comment['time'], start, end) and author != bug.creator and author != bug.assigned_to\
                    and (author != "updates@fedoraproject.org"):
                link = "https://bugzilla.redhat.com/show_bug.cgi?id=%s#c%s" %(str(bug.id), c_id)
                if author not in com_result:
                    com_result[author] = [(bug.id, link)]
                else:
                    com_result[author].append((bug.id, link))
                if bug not in bug_com_list:
                    bug_com_list.append(bug)
            c_id = c_id + 1

    author_list = []
    link_info_list = []

    for author in com_result:
        author_list.append(author)
        link_info = com_result[author]
        dictionary = {}
        for link in link_info:
            if str(link[0]) in dictionary:
                dictionary[str(link[0])].append(link[1])
            else:
                dictionary[str(link[0])] = [link[1]]
        link_info_list.append(dictionary)

    com_result_final = {}

    index = 0
    for author in author_list:
        com_result_final[author] = []
        k_index = 0
        for k in link_info_list[index]:
            com_result_final[author].append([k])
            for link in link_info_list[index][k]:
                com_result_final[author][k_index].append(link)
            k_index = k_index + 1
        index = index + 1

    return com_result_final, bug_com_list


def getReportDict(bz, bug_list, flag, start, end):
    """ """
    result = {}
    rr = 0
    mr = 0

    try:
        if verbose:
            if flag[-1] == "+":
                print "Computing data for completed reviews against reviewers."
            else:
                print "Computing data for incomplete reviews against reviewers."
        number = 1
        total_number = len(bug_list)
        for bug in bug_list:
            if verbose:
                print "Getting bug number:", number, " report <bug #", bug.bug_id, "> -", round((float(number)*100.0/float(total_number)), 3), " %"
            number = number + 1

            report_data = []
            summary_list = []

            return_data = getBugInfo(bz, bug.bug_id, flag, start, end)
            summary_list = return_data["summary"].split()

            pkg_name = None

            if summary_list[2] != ':':
                pkg_name = summary_list[2]
            else:
                pkg_name = summary_list[3]

            if return_data["date"]:
                if "Review Request" in return_data["summary"]:
                    rr = rr + 1
                elif "Merge Review" in return_data["summary"]:
                    mr = mr + 1
                if (result.has_key(return_data["who"])):
                    result[return_data["who"]].append((bug.bug_id, pkg_name))
                else:
                    result[return_data["who"]] = [(bug.bug_id, pkg_name)]
        print "Results in a dictionary:"
        return result, rr, mr
    except KeyboardInterrupt:
        print
        print "Interrupting ...."
        if len(result.keys()) == 0:
            print "No computation done.. Exiting."
            exit(0)
        print "Results till now in a dictionary:"
        return result, rr, mr


if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)

    # Verbose progress
    parser.add_option("-v", action="store_true", dest="verbose", default=False, \
    help="Make a lot of noise [false by default]")
    # Report
    parser.add_option("-r", "--report", action="store", dest="report", default=False, \
    help="Values can be - 'rev-com' - Review complete (against reviewer), 'rev-incom' - Review incomplete - (against reviewer), \
         'cvs-com' - CVS complete (against reviewer), 'cvs-incom' - CVS incomplete - (against reviewer), \
         'new' - New packages - (against reporter), 'com' - comm data")
    # Start date
    parser.add_option("-s", "--start", action="store", dest="start_date", \
    help="Start date for report. Format: d/m/Y or Y-m-d")
    # End date
    parser.add_option("-e", "--end", action="store", dest="end_date", \
    help="End date for report generation. Format: d/m/Y or Y-m-d")
    # Bug ids
    parser.add_option("-u", action="store_true", dest="report_urls", default=False, \
    help="Get bugzilla URLs.  [false by default]")

    parser.add_option("-m", "--email", action="store", dest="email_address",
    help="If specified, send results to the given email address instead of generating 'output.txt' file.")

    parser.add_option("-f", "--email-from", action="store", dest="email_from",
    help="Optional. If specified, then this address will be used for From: field")

    parser.add_option("-n", "--username", action="store", dest="username", help="BZ username")
    parser.add_option("-p", "--password", action="store", dest="password", help="BZ password")

    options = {}
    args = []
    (options, args) = parser.parse_args()

    verbose = options.verbose
    report = options.report
    report_urls = options.report_urls
    username = options.username
    passwd = options.password

    if not report or (report not in ["rev-com", "rev-incom", "cvs-com", "cvs-incom", "new", "com"]):
        print "Check ./bugzillaReport -h or --help for details."
        print "Error: Either wrong report arg value or not supplied."
        print "Values can be: 'rev-com', 'rev-incom', 'new', 'com'"
        exit(1)

    if not options.start_date and options.end_date:
        print "Error: No start date specified."
        exit(1)

    # Decide on timespan for report
    if options.start_date and not options.end_date:
        start = getDateTime(options.start_date)
        end = datetime.datetime.now()
        difference = end - start
        print "Report for ", difference.days, " days."

    elif not options.start_date and not options.end_date:
        end = datetime.datetime.now()
        # Default: 1 week timespan
        interval = datetime.timedelta(seconds=0, minutes=0, hours=0, days=7)
        start = end - interval
        print "Report for ", interval.days, " days."

    elif options.start_date and options.end_date:
        start = getDateTime(options.start_date)
        end = getDateTime(options.end_date)
        difference = end - start
        print "Report for ", difference.days, " days."

    url = "https://bugzilla.redhat.com/xmlrpc.cgi"
    query_dict = {"product": "Fedora",
                  "component": "Package Review",
                  "chfieldfrom": str(start),
                  "field0-0-0": "flagtypes.name",
                  "type0-0-0": "equals"}

    bz = Bugzilla(url=url, user=username, password=passwd, cookiefile=None, tokenfile=None)
    if verbose:
        print "Getting all package review bugs (be patient, this may take a while) ...."

    bug_list_query = {}
    flag = None

    if report == "new":
        flag = "new"
        bug_list_query = {"bug_status": "NEW"}
    elif report == "rev-com":
        flag = "fedora-review+"
        bug_list_query = {"value0-0-0": "fedora-review+"}
    elif report == "rev-incom":
        flag = "fedora-review?"
        bug_list_query = {"value0-0-0": "fedora-review?"}
    elif report == "cvs-com":
        flag = "fedora-cvs+"
        bug_list_query = {"value0-0-0": "fedora-cvs+"}
    elif report == "cvs-incom":
        flag = "fedora-cvs?"
        bug_list_query = {"value0-0-0": "fedora-cvs?"}
    elif report == "com":
        flag = "com"


    bug_list_query.update(query_dict)
    # Get bug list
    bug_list = []
    if verbose:
        print "Bugzilla Query: ", bug_list_query
    bug_list = bz.query(bug_list_query)
    #bug_list = [bz.getbug(518317), bz.getbug(598553), bz.getbug(578759)]
    #bug_list = [bz.getbug(597709), bz.getbug(598138)]
    if verbose:
        print "Total number of Package Reviews:", len(bug_list)

    result = {}
    rr = 0
    mr = 0

    if flag != "com":
        # Result will have name as keys and number of bugs as value.
        result, rr, mr = getReportDict(bz, bug_list, flag, start, end)
    else:
        result, bug_com_list = getComments(bz, bug_list, start, end)
        print "Writing output to output.txt"
        bug_sum = {}
        for bug in bug_com_list:
            bug_sum[str(bug.id)] = bug.summary

        def cmp(x, y):
            """ """
            if len(result[x]) == len(result[y]):
                return 0
            elif len(result[x]) > len(result[y]):
                return -1
            else:
                return 1
        list_of_names = result.keys()
        list_of_names.sort()
        list_of_names.sort(cmp)

        file = open("output.txt", "w")
        file.write("Start Date: " + str(start) + "\n")
        file.write("End Date: " + str(end) + "\n")
        file.write("\n")

        for i in range(0, list_of_names.__len__()):
            name = list_of_names[i]
            file.write(list_of_names[i].encode("utf-8") + " : " + str(len(result[name])))
            file.write("\n")
            if report_urls:
                file.write("\n")
                for comment in result[name]:
                    summary = bug_sum[str(comment[0])]
                    summary_list = summary.split()
                    pkg_name = None

                    if summary_list[2] != ':':
                        pkg_name = summary_list[2]
                    else:
                        pkg_name = summary_list[3]

                    file.write("\n\t" + pkg_name + "\n")
                    for i in range(1, len(comment)):
                        file.write("\t\t" + comment[i] + "\n")

                file.write("\n")
                file.write("\n")

        file.close()
        sys.exit()

    print "Merge Reviews: ", mr
    print "Review Requests: ", rr

    list_of_names = result.keys()


    def cmp(x, y):
        """ """
        if len(result[x]) == len(result[y]):
            return 0
        elif len(result[x]) > len(result[y]):
            return -1
        else:
            return 1

    # To sort based on alphabets
    list_of_names.sort()

    # To sort based on names
    list_of_names.sort(cmp)

    if options.email_address:
        output_path = tempfile.mkstemp()[1] # temporary file to be emailed and deleted afterwards
    else:
        output_path = "output.txt"

    file = open(output_path, "w")
    file.write("Start Date: " + str(start) + "\n")
    file.write("End Date: " + str(end) + "\n")
    file.write("\n")

    # Variable to hold total number of reviews
    total_reviews = 0

    # Bugzilla bug url part
    bugzilla_url = "https://bugzilla.redhat.com/show_bug.cgi?id="

    for i in range(0, list_of_names.__len__()):
        name = list_of_names[i]
        file.write(list_of_names[i].encode("utf-8") + " : " + str(len(result[name])))
        file.write("\n")
        if report_urls:
            file.write("\n")
            for bug in result[name]:
                file.write("\t" + bugzilla_url + str(bug[0]) + "\t" + str(bug[1]))
                file.write("\n")
            file.write("\n")
            file.write("\n")
        total_reviews = total_reviews + len(result[name])

    #file.write("\nMerge Reviews: " + str(mr))
    if report == "rev-com":
        file.write("\nCompleted Review Requests: " + str(rr))
    else:
        file.write("\nTotal reviews modified: " + str(total_reviews))
        file.write("\nReview Requests: " + str(rr))
    file.write("\nThis report was generated by %s." % os.path.basename(sys.argv[0]))
    file.write("\nThe original source is available at: %s" % "https://git.fedorahosted.org/cgit/triage.git/tree/scripts/bzReviewReport.py")
    file.close()
    # File ends here

    if options.email_address:
        import smtplib
        from email.mime.text import MIMEText

        file = open(output_path, "r")
        msg = MIMEText(file.read())
        file.close()

        subject = "Reviews Weekly"
        if options.email_from:
            me = options.email_from
        else:
            me = socket.gethostname()
        you = options.email_address

        msg['Subject'] = subject
        msg['From'] = me
        msg['To'] = you

        # Send the message via our own SMTP server, but don't include the
        # envelope header.
        s = smtplib.SMTP('localhost')
        s.sendmail(me, [you], msg.as_string())
        s.quit()
        os.remove(output_path)
        print "Calculated results were emailed to %s" % you
    else:
        print "Calculated results are in file output.txt"
