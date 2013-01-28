#!/bin/bash
echo ${Iniciando conexion ... }

/sbin/wpa_supplicant -B -iwlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf -Dwext

/sbin/dhclient wlan0