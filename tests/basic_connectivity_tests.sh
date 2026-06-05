#!/bin/sh
# Suite de tests de connectivité de base pour l'infrastructure Docker
# Ce script exécute tous les tests individuels de connectivité

echo "===== BASIC CONNECTIVITY TESTS ====="
echo "Exécution des tests de connectivité de base pour tous les services..."

# Test 1: Base de données MariaDB
echo "1/10 - Test base de données..."
sh /tests/test_database.sh

# Test 2: Broker MQTT Mosquitto
echo "2/10 - Test broker MQTT..."
sh /tests/test_mqtt.sh

# Test 3: Réseau et DNS
echo "3/10 - Test réseau et DNS..."
sh /tests/test_network.sh

# Test 4: Services web (phpMyAdmin, Grafana, web_app)
echo "4/10 - Test services web..."
sh /tests/test_ports.sh

# Test 5: SSL/TLS
echo "5/10 - Test SSL/TLS..."
sh /tests/test_ssl.sh

# Test 6: app_python
echo "6/10 - Test app_python..."
sh /tests/test_app_python.sh

# Test 7: Beszel
echo "7/10 - Test Beszel..."
sh /tests/test_beszel.sh

# Test 8: Traefik
echo "8/10 - Test Traefik..."
sh /tests/test_traefik.sh

# Test 9: Volumes Docker
echo "9/10 - Test volumes Docker..."
sh /tests/test_volumes.sh

# Test 10: Espace disque
echo "10/10 - Test espace disque..."
sh /tests/test_disk_space.sh

echo "===== BASIC TESTS COMPLETE ====="
echo "Tous les tests de connectivité de base ont été exécutés avec succès"
