#!/bin/sh
# Test des volumes Docker
# Ce script vérifie que les volumes sont montés correctement

echo "Test volumes Docker..."

# Vérifier que les volumes existent
echo "Vérification des volumes..."
docker volume ls | grep -q "marais_project_vol_BDD"
if [ $? -eq 0 ]; then
  echo "vol_BDD OK"
else
  echo "vol_BDD FAIL"
  exit 1
fi

docker volume ls | grep -q "marais_project_vol_grafana"
if [ $? -eq 0 ]; then
  echo "vol_grafana OK"
else
  echo "vol_grafana FAIL"
  exit 1
fi

docker volume ls | grep -q "marais_project_vol_beszel"
if [ $? -eq 0 ]; then
  echo "vol_beszel OK"
else
  echo "vol_beszel FAIL"
  exit 1
fi

docker volume ls | grep -q "marais_project_mosquitto_data"
if [ $? -eq 0 ]; then
  echo "mosquitto_data OK"
else
  echo "mosquitto_data FAIL"
  exit 1
fi

# Vérifier l'utilisation des volumes
echo ""
echo "Utilisation des volumes:"
docker volume ls

echo "Volumes Docker OK"
