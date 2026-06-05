#!/bin/sh
# Test de connectivité des services web
# Ce script vérifie que les interfaces web sont accessibles depuis le réseau Docker

echo "Test phpmyadmin..."
# Test l'interface phpMyAdmin sur le port 80 du conteneur phpmyadmin
# wget --spider vérifie l'existence de l'URL sans télécharger le contenu
wget -q --spider http://phpmyadmin:80

if [ $? -eq 0 ]; then
  echo "phpmyadmin OK"
else
  echo "phpmyadmin FAIL"
  exit 1
fi

echo "Test grafana..."
# Test l'interface Grafana sur le port 3000 du conteneur grafana
wget -q --spider http://grafana:3000

if [ $? -eq 0 ]; then
  echo "grafana OK"
else
  echo "grafana FAIL"
  exit 1
fi

echo "Test web_app..."
# Test l'application web sur le port 5000 du conteneur web_app
wget -q --spider http://web_app:5000

if [ $? -eq 0 ]; then
  echo "web_app OK"
else
  echo "web_app FAIL"
  exit 1
fi
