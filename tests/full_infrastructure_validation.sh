#!/bin/sh
# Suite complète de validation d'infrastructure Docker
# Ce script exécute tous les tests : basiques + avancés dans les conteneurs

echo "===== INFRASTRUCTURE VALIDATION SUITE ====="
echo "Validation complète de l'infrastructure Docker avec tests approfondis..."

echo ""
echo "1. Basic Connectivity Tests..."
echo "   Tests de connectivité de base depuis le conteneur test_runner"
sh /tests/basic_connectivity_tests.sh

echo ""
echo "2. Container Connectivity Tests..."
echo "   Tests avancés de connectivité depuis chaque conteneur"
sh /tests/container_connectivity_tests.sh

echo ""
echo "3. Database Insert Test..."
echo "   Test d'insertion et lecture dans la base de données"
sh /tests/test_database_insert.sh

echo ""
echo "4. MQTT Publish/Subscribe Test..."
echo "   Test de publication et abonnement MQTT"
sh /tests/test_mqtt_pubsub.sh

echo ""
echo "===== VALIDATION COMPLETE ====="
echo "L'infrastructure Docker a été entièrement validée"
echo "Prête pour la production ou les tests d'intégration"
