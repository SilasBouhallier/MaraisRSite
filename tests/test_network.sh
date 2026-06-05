#!/bin/sh
# Test de connectivité réseau et résolution DNS
# Ce script vérifie que les conteneurs peuvent communiquer entre eux

echo "Test reseau..."
# ping -c 2 envoie 2 paquets ICMP pour tester la connectivité réseau
# Test la résolution DNS et la connectivité de base avec MariaDB
ping -c 2 mariadb > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "MariaDB PING FAIL"
  exit 1
fi
echo "MariaDB PING OK"

# Test la résolution DNS et la connectivité de base avec Mosquitto
ping -c 2 mosquitto > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "Mosquitto PING FAIL"
  exit 1
fi
echo "Mosquitto PING OK"
