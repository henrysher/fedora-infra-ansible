#!/bin/sh
# First check if this server is actually an OpenVPN client
if [ -f /etc/openvpn/client.crt ];
then
	# Now the magic line
	# This first checks whether there is a route, and if there isn't it will:
	# 1. Get the local machine's VPN IP (up to and including awk)
	# 2. Add a new route to 192.168.0.0/16 via that IP addres (from xargs on)
	# 3. Print "Fixed VPN" and exit with code 2 to indicate that it changed
	# Note: I've been told that the grep and awk can be in one command, and I believe that, but I find this clearer.
	(ip route show | grep '192.168.0.0/16') || ((ip route show | grep '192.168.0.' | awk '{print $1}' | xargs ip route add 192.168.0.0/16 via) && echo "Fixed VPN" && exit 2);
fi
