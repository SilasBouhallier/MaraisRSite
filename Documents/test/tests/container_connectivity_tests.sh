#!/bin/sh

echo "===== CONTAINER CONNECTIVITY TESTS ====="

# Couleurs pour une meilleure lisibilité
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction pour afficher les résultats
test_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2 OK${NC}"
        return 0
    else
        echo -e "${RED}❌ $2 FAIL${NC}"
        return 1
    fi
}

echo -e "${BLUE}1. Tests depuis le conteneur web_app${NC}"
echo "----------------------------------------"

# Test connectivité depuis web_app
docker compose exec -T web_app sh -c "
echo 'Test connexion MariaDB depuis web_app:'
nc -z mariadb 3306 && echo 'OK' || echo 'FAIL'

echo 'Test connexion MQTT depuis web_app:'
nc -z mosquitto 1883 && echo 'OK' || echo 'FAIL'

echo 'Test phpMyAdmin depuis web_app:'
wget -q --spider http://phpmyadmin:80 && echo 'OK' || echo 'FAIL'

echo 'Test Grafana depuis web_app:'
wget -q --spider http://grafana:3000 && echo 'OK' || echo 'FAIL'

echo 'Test résolution DNS:'
nslookup mariadb && echo 'OK' || echo 'FAIL'
nslookup mosquitto && echo 'OK' || echo 'FAIL'
"

echo ""
echo -e "${BLUE}2. Tests depuis le conteneur mariadb${NC}"
echo "----------------------------------------"

# Test depuis mariadb
docker compose exec -T mariadb sh -c "
echo 'Test connexion web_app depuis mariadb:'
nc -z web_app 5000 && echo 'OK' || echo 'FAIL'

echo 'Test connexion MQTT depuis mariadb:'
nc -z mosquitto 1883 && echo 'OK' || echo 'FAIL'

echo 'Test phpMyAdmin depuis mariadb:'
wget -q --spider http://phpmyadmin:80 && echo 'OK' || echo 'FAIL'

echo 'Test Grafana depuis mariadb:'
wget -q --spider http://grafana:3000 && echo 'OK' || echo 'FAIL'
"

echo ""
echo -e "${BLUE}3. Tests de base de données depuis mariadb${NC}"
echo "----------------------------------------"

# Test base de données
docker compose exec -T mariadb sh -c "
echo 'Test connexion MySQL:'
mysql -u root -p\$MYSQL_ROOT_PASSWORD -e 'SELECT 1;' && echo 'OK' || echo 'FAIL'

echo 'Test bases de données:'
mysql -u root -p\$MYSQL_ROOT_PASSWORD -e 'SHOW DATABASES;' && echo 'OK' || echo 'FAIL'

echo 'Test création de table test:'
mysql -u root -p\$MYSQL_ROOT_PASSWORD -e 'CREATE DATABASE IF NOT EXISTS test_db; USE test_db; CREATE TABLE IF NOT EXISTS test_table (id INT);' && echo 'OK' || echo 'FAIL'
"

echo ""
echo -e "${BLUE}4. Tests réseau avancés${NC}"
echo "----------------------------------------"

# Tests réseau depuis un conteneur temporaire
docker run --rm --network test_marais_net alpine sh -c "
apk add --no-cache curl netcat-openbsd iputils bind-tools > /dev/null 2>&1

echo 'Test ping vers tous les services:'
ping -c 1 mariadb && echo 'MariaDB PING OK' || echo 'MariaDB PING FAIL'
ping -c 1 mosquitto && echo 'MQTT PING OK' || echo 'MQTT PING FAIL'
ping -c 1 web_app && echo 'web_app PING OK' || echo 'web_app PING FAIL'
ping -c 1 phpmyadmin && echo 'phpMyAdmin PING OK' || echo 'phpMyAdmin PING FAIL'
ping -c 1 grafana && echo 'Grafana PING OK' || echo 'Grafana PING FAIL'

echo ''
echo 'Test résolution DNS complète:'
nslookup mariadb && echo 'MariaDB DNS OK' || echo 'MariaDB DNS FAIL'
nslookup mosquitto && echo 'MQTT DNS OK' || echo 'MQTT DNS FAIL'
nslookup web_app && echo 'web_app DNS OK' || echo 'web_app DNS FAIL'

echo ''
echo 'Test ports TCP:'
nc -zv mariadb 3306 && echo 'MariaDB PORT OK' || echo 'MariaDB PORT FAIL'
nc -zv mosquitto 1883 && echo 'MQTT PORT OK' || echo 'MQTT PORT FAIL'
nc -zv web_app 5000 && echo 'web_app PORT OK' || echo 'web_app PORT FAIL'
nc -zv phpmyadmin 80 && echo 'phpMyAdmin PORT OK' || echo 'phpMyAdmin PORT FAIL'
nc -zv grafana 3000 && echo 'Grafana PORT OK' || echo 'Grafana PORT FAIL'
"

echo ""
echo -e "${BLUE}5. Tests de santé des services${NC}"
echo "----------------------------------------"

# Vérifier l'état des conteneurs
echo "État des conteneurs:"
docker compose ps

echo ""
echo "Utilisation mémoire:"
docker stats --no-stream --format "table {{.Container}}\t{{.MemUsage}}\t{{.CPUPerc}}"

echo ""
echo -e "${BLUE}6. Tests de logs récents${NC}"
echo "----------------------------------------"

# Vérifier les erreurs récentes dans les logs
echo "Vérification des erreurs récentes:"
echo "web_app erreurs:"
docker compose logs --tail=5 web_app | grep -i error || echo "Aucune erreur trouvée"

echo "mariadb erreurs:"
docker compose logs --tail=5 mariadb | grep -i error || echo "Aucune erreur trouvée"

echo "mosquitto erreurs:"
docker compose logs --tail=5 mosquitto | grep -i error || echo "Aucune erreur trouvée"

echo ""
echo -e "${GREEN}===== CONTAINER CONNECTIVITY TESTS COMPLETE =====${NC}"
