#!/bin/sh
# Suite de tests de connectivité de base pour l'infrastructure Docker
# Ce script exécute tous les tests individuels de connectivité

echo "===== BASIC CONNECTIVITY TESTS ====="
echo "Exécution des tests de connectivité de base pour tous les services..."

# Test 1: Base de données MariaDB
echo "1/4 - Test base de données..."
sh /tests/test_database.sh

# Test 2: Broker MQTT Mosquitto  
echo "2/4 - Test broker MQTT..."
sh /tests/test_mqtt.sh

# Test 3: Réseau et DNS
echo "3/4 - Test réseau et DNS..."
sh /tests/test_network.sh

# Test 4: Services web (phpMyAdmin, Grafana, web_app)
echo "4/4 - Test services web..."
sh /tests/test_ports.sh

echo "===== BASIC TESTS COMPLETE ====="
echo "Tous les tests de connectivité de base ont été exécutés avec succès"
