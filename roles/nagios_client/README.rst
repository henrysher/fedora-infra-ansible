===================================
 Nagios 4 Configuration for Fedora
===================================

The Fedora Infrastructure Nagios is built on a set of configurations
originally written for Nagios 2 and then upgraded over time to Nagios
3 and then 4.08. With additional changes made in the 4.2 series of
Nagios this needed a better rewrite as various parts came from
pre-puppet and then various puppet modules added on top. 

In order to get this rewrite done, we will use as much of the original
layout of the Fedora ansible nagios module but with rewrites to better
match current Nagios configurations so that it can be maintained.

Role directory layout
=====================
The original layout branched out from 

  roles/nagios/client/
  roles/nagios/server/

With the usual trees below this. This breaks ansible best practices
and how most new modules are set up so the rewrite uses:

  roles/nagios_client/
  roles/nagios_server/

=====================
 Nagios Client Files
=====================

For the most part the Nagios Client files seem to work from the
original layout to the new site. Changes will only need to be made to
playbooks for the initial changes.


