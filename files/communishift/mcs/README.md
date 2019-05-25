MachineConfig files
-------------------

The files in this directory are used as machineconfig files for communishift.
Note that they're template files: some changes will need to be made before "oc create -f".

Specifically:
- The templates have two "DOBOTH" replacements. You want to create the file twice,
  once with both DOBOTH cases replaced with "master" and once replaced with "worker".
- The mc_firewall.yml.template has a bit FILL_IN_HERE. Run "./to_data.sh firewall.sh",
  and copy the output from that script into the FILL_IN_HERE bit in the MC.
  Then run that MC twice as per the previous point (master and worker).
