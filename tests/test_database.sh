#!/bin/sh
# Test de connectivité à la base de données MariaDB
# Ce script vérifie que le port MySQL 3306 est accessible

echo "Test MariaDB..."
# nc -z vérifie la connectivité TCP sans envoyer de données
# -z = zero-I/O mode (scan only), -w 1 = timeout 1 seconde
nc -z mariadb 3306

if [ $? -eq 0 ]; then
  echo "MariaDB OK"
else
  echo "MariaDB FAIL"
  exit 1
fi
