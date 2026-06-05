#!/bin/sh
# Test de connectivité au broker MQTT Mosquitto
# Ce script vérifie que le port MQTTS 8883 est accessible

echo "Test MQTTS..."
# nc -z vérifie la connectivité TCP sur le port MQTTS 8883
# Si le port est ouvert, le broker MQTT est prêt à accepter des connexions TLS
nc -z mosquitto 8883

if [ $? -eq 0 ]; then
  echo "MQTTS OK"
else
  echo "MQTTS FAIL"
  exit 1
fi
