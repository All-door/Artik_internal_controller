modprobe -r dhd
modprobe dhd op_mode=0
ifconfig wlan0 up
dhclient -r
if [ -f "/usr/lib/systemd/system/wpa_supplicant.service" ]; then
  systemctl restart wpa_supplicant
fi
pkill hostapd
ifconfig wlan0 down

systemctl restart wpa_supplicant
ifconfig wlan0 up
dhclient wlan0
