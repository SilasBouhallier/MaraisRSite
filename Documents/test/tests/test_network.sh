#!/bin/sh
# Test de connectivité réseau et résolution DNS
# Ce script vérifie que les conteneurs peuvent communiquer entre eux

echo "Test reseau..."
# ping -c 2 envoie 2 paquets ICMP pour tester la connectivité réseau
# Test la résolution DNS et la connectivité de base avec MariaDB
ping -c 2 mariadb
# Test la résolution DNS et la connectivité de base avec Mosquitto
ping -c 2 mosquitto
