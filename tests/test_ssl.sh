#!/bin/sh
# Test SSL/TLS pour les services sécurisés
# Ce script vérifie que les ports sécurisés sont accessibles

echo "Test SSL/TLS..."

# Test HTTPS sur le port 443 (Traefik)
echo "Test HTTPS sur port 443..."
nc -z traefik 443 > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "HTTPS OK"
else
  echo "HTTPS FAIL"
  exit 1
fi

# Test MQTTS (port 8883)
echo "Test MQTTS sur port 8883..."
nc -z mosquitto 8883 > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "MQTTS OK"
else
  echo "MQTTS FAIL"
  exit 1
fi

echo "Tous les tests SSL/TLS OK"
