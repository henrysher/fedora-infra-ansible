module:
	checkmodule -Mmo nagios_hostname.mod nagios_hostname.te
	semodule_package -o nagios_hostname.pp -m nagios_hostname.mod
	rm nagios_hostname.mod
	checkmodule -Mmo nagios_42.mod nagios_42.te
	semodule_package -o nagios_42.pp -m nagios_42.mod
	rm nagios_42.mod
