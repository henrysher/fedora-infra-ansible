import re
import datetime
import socket
from optparse import OptionParser
from urlparse import urljoin

import resultsdb_api

# taken from http://docs.resultsdb20.apiary.io
OKAYISH = ["PASSED", "INFO"]
FAILISH = ["FAILED", "NEEDS_INSPECTION"]


def main(resultsdb_url, frontend_url, timeparam):
    """
    Download results from resultdb for selected time span, return them
    prettyprinted in string.

    :param str resultsdb_url: URL of resultsdb instance
    :param str frontend_url: URL of resultsdb frontend
    :param str timeparam: two ISO 8601 values separated by commas for time span
    :return: prettyprinted summary of checks
    """
    api = resultsdb_api.ResultsDBapi(resultsdb_url)

    results = []
    page = 0
    r = api.get_results(since=timeparam, page=page)
    while len(r["data"]) != 0:
        results.extend(r["data"])
        page += 1
        r = api.get_results(since=timeparam, page=page)

    passed = 0
    passed_types = {}
    failed = 0
    failed_types = {}
    together = {}
    for result in results:
        test_case = result["testcase"]["name"]
        if result["outcome"] in OKAYISH:
            passed += 1
            passed_types[test_case] = passed_types.get(test_case, 0) + 1
        else:
            failed += 1
            failed_types[test_case] = failed_types.get(test_case, 0) + 1
        together[test_case] = together.get(test_case, 0) + 1

    output = "libtaskotron results\n====================\n"
    output += "Generated on: " + socket.gethostname() + "\n"
    [from_time, to_time] = timeparam.split(",")
    output += "From:         " + from_time + "\n"
    output += "To:           " + to_time + "\n\n"
    output += "Executed checks:\n----------------\n"
    for check in sorted(together.keys()):
        failed_count = failed_types.get(check, 0)
        failed_percent = int(round((failed_count * 100.0) / together[check]))
        output += "%s: %d (%d %% failed)\n" % (check, together[check], failed_percent)
    output += "\nTotal: %d executed, %d failed\n\n" % (passed + failed, failed)
    output += "Links to failed checks:\n-----------------------\n"
    for failed_check in sorted(failed_types.keys()):
        limit = min(failed_types[failed_check], 1000)
        url = urljoin(frontend_url, "results?outcome=%s&since=%s,%s&testcase_name=%s&limit=%d" %
                      (",".join(FAILISH), from_time, to_time, failed_check, limit))
        output += "%s: %s\n" % (failed_check, url)
    return output


if __name__ == "__main__":
    parser = OptionParser(usage="usage: %prog -u [URL] -f [FRONTEND] "
                                "-t [TIMESPAN]")
    parser.add_option("-u", "--url", dest="resultsdb_url",
                      help="url of resultsdb instance")
    parser.add_option("-f", "--frontend", dest="frontend_url",
                      help="url of resultsdb frontend")
    parser.add_option("-t", "--time", dest="time", help="time span - either "
                            "one number or time and date in ISO 8601 format. "
                            "When given simple number X, it generates report "
                            "for last X hours, starting from now. When given "
                            "one ISO 8601 formatted time, it generates report "
                            "starting from that time on. For time span, use "
                            "two ISO 8601 formatted times, separated by comma.")
    (opts, _) = parser.parse_args()
    if not opts.resultsdb_url or not opts.time or not opts.frontend_url:
        parser.error("resultsdb url, frontend url and time span arguments"
                     " required")

    iso_regex = re.compile(
        r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}(:\d{2}(\.\d+)?)?)?$")
    m = re.search(r"^(?P<first>.*),(?P<second>.*)$", opts.time)
    if m:  # both values (from and to) as arguments
        if not re.match(iso_regex, m.group('first')):
            parser.error("First time string not in YYYY-MM-DDTHH:MM:SS format")
        if not re.match(iso_regex, m.group('second')):
            parser.error("Second time string not in YYYY-MM-DDTHH:MM:SS format")
        time_span = opts.time
    else:
        time_now = datetime.datetime.now()
        if re.match(r"^\d+$", opts.time):  # only last X hours as argument
            time_param = time_now - datetime.timedelta(hours=int(opts.time))
            time_span = time_param.isoformat() + "," + time_now.isoformat()
        else:  # one ISO 8601 time argument
            if not re.match(iso_regex, opts.time):
                parser.error("First time string not in YYYY-MM-DDTHH:MM:SS "
                             "format")
            time_span = opts.time + "," + time_now.isoformat()

    output = main(opts.resultsdb_url, opts.frontend_url, time_span)
    print output,
