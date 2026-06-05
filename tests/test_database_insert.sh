#!/bin/sh
# Test d'insertion dans la base de données
# Ce script vérifie que l'insertion de données fonctionne

echo "Test insertion BDD..."

# Tester l'insertion d'une mesure de test
docker-compose exec -T mariadb sh -c "
mysql -u root -p\$MYSQL_ROOT_PASSWORD Marais_R_Site -e \"
INSERT INTO mesure (valeur, date_heure, id_type_mesure, id_emplacement)
VALUES (100.5, NOW(), 1, 1);
SELECT 'Insertion OK' AS result;
\" 2>/dev/null
"

if [ $? -eq 0 ]; then
  echo "Insertion BDD OK"
else
  echo "Insertion BDD FAIL"
  exit 1
fi

# Tester la lecture de la mesure insérée
docker-compose exec -T mariadb sh -c "
mysql -u root -p\$MYSQL_ROOT_PASSWORD Marais_R_Site -e \"
SELECT valeur FROM mesure ORDER BY id_mesure DESC LIMIT 1;
\" 2>/dev/null
"

if [ $? -eq 0 ]; then
  echo "Lecture BDD OK"
else
  echo "Lecture BDD FAIL"
  exit 1
fi

# Nettoyer la mesure de test
docker-compose exec -T mariadb sh -c "
mysql -u root -p\$MYSQL_ROOT_PASSWORD Marais_R_Site -e \"
DELETE FROM mesure WHERE valeur = 100.5 ORDER BY id_mesure DESC LIMIT 1;
SELECT 'Nettoyage OK' AS result;
\" 2>/dev/null
"

echo "Test insertion BDD complet OK"
