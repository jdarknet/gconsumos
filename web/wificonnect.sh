#!/bin/bash
echo ${Iniciando conexion ... }

sudo wpa_supplicant -B -iwlan0 -c/etc/wpa_supplicant/wpa_supplicant.conf -Dwext
sudo dhclient wlan0