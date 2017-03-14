<?php

$cfg['cgi_config_file']='/etc/nagios/cgi.cfg';  // location of the CGI config file

$cfg['cgi_base_url']='/{{nagios_srcdir}}/cgi-bin/';

// FILE LOCATION DEFAULTS
$cfg['main_config_file']='/etc/nagios/nagios.cfg';  // default location of the main Nagios config file
$cfg['status_file']='/var/spool/nagios/status.dat'; // default location of Nagios status file
$cfg['state_retention_file']='/var/log/nagios/retention.dat'; // default location of Nagios retention file

// utilities
require_once(dirname(__FILE__).'/includes/utils.inc.php');
