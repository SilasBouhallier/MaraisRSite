#!/bin/sh
# Test de connectivité au broker MQTT Mosquitto
# Ce script vérifie que le port MQTT 1883 est accessible

echo "Test MQTT..."
# nc -z vérifie la connectivité TCP sur le port MQTT standard 1883
# Si le port est ouvert, le broker MQTT est prêt à accepter des connexions
nc -z mosquitto 1883

if [ $? -eq 0 ]; then
  echo "MQTT OK"
else
  echo "MQTT FAIL"
  exit 1
fi
