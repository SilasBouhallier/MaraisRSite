#!/bin/sh
# Test de l'application app_python
# Ce script vérifie que l'application MQTT fonctionne correctement

echo "Test app_python..."

# Vérifier que le conteneur app_python est en cours d'exécution
# Utiliser docker ps car docker compose ps n'a pas --format dans Alpine
# Chercher le conteneur avec "app_python" dans le nom
docker ps --format "table {{.Names}}\t{{.Status}}" | grep "app_python" | grep -q "Up"
if [ $? -ne 0 ]; then
  echo "app_python container not running"
  exit 1
fi
echo "app_python container OK"

# Vérifier la connexion MQTT depuis app_python
docker exec app_python sh -c "
python -c 'import paho.mqtt.client as mqtt; print(\"MQTT client OK\")' 2>/dev/null
if [ \$? -eq 0 ]; then
  echo 'MQTT library OK'
else
  echo 'MQTT library FAIL'
  exit 1
fi
"

# Vérifier la connexion MariaDB depuis app_python
docker exec app_python sh -c "
python -c 'import mysql.connector; print(\"MySQL connector OK\")' 2>/dev/null
if [ \$? -eq 0 ]; then
  echo 'MySQL library OK'
else
  echo 'MySQL library FAIL'
  exit 1
fi
"

echo "app_python OK"
