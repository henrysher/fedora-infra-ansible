#!/usr/bin/env bash
for iface in `ls /etc/sysconfig/network-scripts/ifcfg-* | sed 's/.*\-//g'`; do
  # Ignore local interface
  [[ "$iface" == "lo" ]] && continue

  correct_mac="$(ip a show dev $iface | grep 'link/ether' | awk '{print $2}')"
  current_mac="$(grep HWADDR /etc/sysconfig/network-scripts/ifcfg-$iface | cut -d= -f2 | sed 's/"//g')"

  [[ "$correct_mac" == "$current_mac" ]] && continue

  sed -i "s/$current_mac/$correct_mac/" /etc/sysconfig/network-scripts/ifcfg-$iface
done

service network restart
service NetworkManager restart
