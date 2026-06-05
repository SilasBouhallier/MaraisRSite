#!/bin/sh
# Test de Beszel et Beszel Agent
# Ce script vérifie que les services de monitoring fonctionnent

echo "Test Beszel..."

# Vérifier que le conteneur beszel est en cours d'exécution
docker ps --format "table {{.Names}}\t{{.Status}}" | grep "beszel" | grep -q "Up"
if [ $? -ne 0 ]; then
  echo "beszel container not running"
  exit 1
fi
echo "beszel container OK"

# Vérifier le port Beszel
nc -z beszel 8090 > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "beszel port 8090 OK"
else
  echo "beszel port 8090 FAIL"
  exit 1
fi

# Vérifier que le conteneur beszel-agent est en cours d'exécution
docker ps --format "table {{.Names}}\t{{.Status}}" | grep "beszel-agent" | grep -q "Up"
if [ $? -ne 0 ]; then
  echo "beszel-agent container not running"
  exit 1
fi
echo "beszel-agent container OK"

# Vérifier le port Beszel Agent
nc -z beszel-agent 4567 > /dev/null 2>&1
if [ $? -eq 0 ]; then
  echo "beszel-agent port 4567 OK"
else
  echo "beszel-agent port 4567 FAIL"
  exit 1
fi

echo "Beszel OK"
