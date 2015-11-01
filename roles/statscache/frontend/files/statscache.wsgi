# http://stackoverflow.com/questions/8007176/500-error-without-anything-in-the-apache-logs
import logging
import sys
logging.basicConfig(stream=sys.stderr)

import statscache.app
application = statscache.app.app
#application.debug = True  # Nope.  Be careful!
