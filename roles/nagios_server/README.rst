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
 Nagios Server Files
=====================

The Nagios Server Files require a large layout change. The original
Nagios system used multiple independant modes and files which caused
problems when hosts were removed. The new system will use hosts set up
from the Fedora Ansible Inventory with hostgroups set up to match
groups.

  roles/nagios_server/{files,handlers,tasks,templates}

  r.../n.../files/httpd ==> /etc/httpd/conf.d files
  r.../n.../files/nagios ==> /etc/nagios/ files
  r.../n.../files/nagios/commands      command files
  r.../n.../files/nagios/hosts         host files
  r.../n.../files/nagios/hostgroups    groups made from hosts
  r.../n.../files/nagios/services      services
  r.../n.../files/nagios/servicegroups groups made from services
  r.../n.../files/nagios/contacts      files for people
  r.../n.../files/nagios/contactgroups groups made from contacts
      
  similar layout for templates
  handlers has the ways to restart and check configuration
  tasks has the main rules for building stuff.

===================
Nagios Module Steps
===================

1. Check to see if the nagios user is configured. Someone years ago
   chose that our monitoring uses UID/GID 420. Har Har.
   Setup any other groups and permissions
2. Install the needed packages for the server.
3. Setup the directories on the server
    /etc/nagios/{child}
4. Synchonise over the static files
    /etc/nagios/commands/
    /etc/nagios/services/
    /etc/nagios/servicegroups/
    /etc/nagios/contacts/
    /etc/nagios/contactgroups/
    /usr/lib64/nagios/plugins/
    /usr/local/bin
    /usr/share/nagios/html/
5. Build template files
    /etc/nagios/commands/
    /etc/nagios/hosts/{ansible-inventory, ansible-vars, other}
    /etc/nagios/hostgroups/
6. Fix selinux policy
7. Restart services
