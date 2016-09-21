modprobe -r dhd
modprobe dhd op_mode=2
ifconfig wlan0 192.168.2.1 up
dnsmasq -C /etc/dnsmasq.conf

sysctl net.ipv4.ip_forward=1
iptables --flush
iptables -t nat --flush
iptables --delete-chain
iptables -t nat --delete-chain
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A FORWARD -i wlan0 -j ACCEPT

hostapd /etc/hostapd/hostapd.conf -B
