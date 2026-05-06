#!/bin/sh
# Test de publication et abonnement MQTT
# Ce script vérifie que le broker MQTT fonctionne correctement

echo "Test MQTT publish/subscribe..."

# Installer mosquitto-clients si nécessaire
docker-compose exec -T app_python sh -c "
which mosquitto_pub > /dev/null 2>&1 || apk add --no-cache mosquitto-clients > /dev/null 2>&1
"

# Test de publication
echo "Test publication MQTT..."
docker-compose exec -T app_python sh -c "
mosquitto_pub -h mosquitto -p 8883 -t 'test/topic' -m 'test_message' --insecure -u test -p test 2>/dev/null
if [ \$? -eq 0 ]; then
  echo 'Publication OK'
else
  echo 'Publication FAIL (may need authentication)'
fi
"

# Test d'abonnement (en arrière-plan)
echo "Test abonnement MQTT..."
docker-compose exec -T app_python sh -c "
timeout 2 mosquitto_sub -h mosquitto -p 8883 -t 'test/topic' --insecure -u test -p test 2>/dev/null &
SUB_PID=\$!
sleep 1
mosquitto_pub -h mosquitto -p 8883 -t 'test/topic' -m 'test_message' --insecure -u test -p test 2>/dev/null
wait \$SUB_PID 2>/dev/null
if [ \$? -eq 0 ]; then
  echo 'Abonnement OK'
else
  echo 'Abonnement FAIL (may need authentication)'
fi
"

echo "Test MQTT publish/subscribe terminé"
