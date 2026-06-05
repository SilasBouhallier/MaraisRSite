#!/bin/bash

# Charger le .env proprement
SCRIPT_DIR=$(dirname "$(readlink -f "$0")")
set -a
source "$SCRIPT_DIR/.env"
set +a

# Vérification
if [ -z "$MYSQL_ROOT_PASSWORD" ]; then
  echo "Erreur : MYSQL_ROOT_PASSWORD non défini"
  exit 1
fi

# Config
BACKUP_DIR="/home/debian/marais_project/backups/mysql"
DATE=$(date +%Y-%m-%d_%Hh%M)
CONTAINER_NAME="mariadb"
DB_NAME="Marais_R_Site"
OUTPUT_FILE="$BACKUP_DIR/backup_$DATE.sql"

# Créer dossier
mkdir -p "$BACKUP_DIR"

# Dump complet
docker exec "$CONTAINER_NAME" mariadb-dump \
  -u root -p"$MYSQL_ROOT_PASSWORD" \
  --single-transaction --quick --routines --triggers \
  "$DB_NAME" > "$OUTPUT_FILE"

# Vérification
if [ $? -ne 0 ]; then
  echo "Erreur lors du dump"
  rm -f "$OUTPUT_FILE"
  exit 1
fi

echo "Backup OK : $OUTPUT_FILE"

# Nettoyage (7 jours)
find "$BACKUP_DIR" -type f -mtime +7 -name "*.sql" -delete
