#!/bin/sh
# Test de l'espace disque
# Ce script vérifie qu'il y a suffisamment d'espace disque

echo "Test espace disque..."

# Vérifier l'espace disque du système
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
echo "Utilisation disque: ${DISK_USAGE}%"

if [ $DISK_USAGE -gt 90 ]; then
  echo "WARNING: Espace disque critique (>90%)"
  exit 1
elif [ $DISK_USAGE -gt 80 ]; then
  echo "WARNING: Espace disque élevé (>80%)"
else
  echo "Espace disque OK"
fi

# Vérifier l'espace disque des volumes Docker
echo ""
echo "Espace disque des volumes:"
docker system df

# Vérifier l'espace disque des conteneurs
echo ""
echo "Espace disque par conteneur:"
docker ps -q | xargs docker inspect --format '{{.Name}}: {{.SizeRw}}' 2>/dev/null || echo "Non disponible"

echo "Test espace disque terminé"
