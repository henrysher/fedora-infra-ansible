set -xe

iptables -N fedora-block-ports
iptables -A fedora-block-ports -p tcp --dport 111 -j REJECT
iptables -A fedora-block-ports -p udp --dport 111 -j REJECT
iptables -A fedora-block-ports -p tcp --dport 22623 --src 38.145.48.42 -j ACCEPT
iptables -A fedora-block-ports -p tcp --dport 22623 --src 38.145.48.43 -j ACCEPT
iptables -A fedora-block-ports -p tcp --dport 22623 -j REJECT

iptables -I INPUT 1 -j fedora-block-ports
