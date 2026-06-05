#!/bin/sh
# Test de Traefik
# Ce script vérifie que le reverse proxy fonctionne correctement

echo "Test Traefik..."

# Vérifier que le conteneur traefik est en cours d'exécution
docker ps --format "table {{.Names}}\t{{.Status}}" | grep "traefik" | grep -q "Up"
if [ $? -ne 0 ]; then
  echo "traefik container not running"
  exit 1
fi
echo "traefik container OK"

# Vérifier le port HTTPS (443)
nc -z traefik 443 > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "traefik port 443 OK"
else
  echo "traefik port 443 FAIL"
  exit 1
fi

# Vérifier le port MQTTS (8883)
nc -z traefik 8883 > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "traefik port 8883 OK"
else
  echo "traefik port 8883 FAIL"
  exit 1
fi

# Vérifier le dashboard Traefik (local)
nc -z 127.0.0.1 8080 > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "traefik dashboard port 8080 OK"
else
  echo "traefik dashboard port 8080 FAIL (may be expected if not on host)"
fi

# Vérifier que Traefik peut atteindre les services backend
docker exec traefik sh -c "
wget -q --spider http://web_app:5000 && echo 'web_app reachable OK' || echo 'web_app reachable FAIL'
wget -q --spider http://grafana:3000 && echo 'grafana reachable OK' || echo 'grafana reachable FAIL'
wget -q --spider http://phpmyadmin:80 && echo 'phpmyadmin reachable OK' || echo 'phpmyadmin reachable FAIL'
"

echo "Traefik OK"
