# Guide d'Utilisation - Système de Surveillance Environnementale Marais R Site

## Vue d'Ensemble

Le système Marais R Site est une solution complète de surveillance environnementale qui collecte, analyse et affiche des données en temps réel provenant de sondes IoT connectées. Il surveille la qualité de l'air intérieur avec des capteurs pour :

- **CO2** (ppm) - Qualité de l'air et ventilation
- **PM 2.5** (µg/m³) - Particules fines
- **PM 10** (µg/m³) - Particules grossières
- **TVOC** (ppb) - Composés organiques volatils

## Accès aux Services

### Interface Web Grafana (Visualisation)

**URL** : `http://localhost:3000` (accès local uniquement)

**Fonctionnalités** :
- Tableaux de bord en temps réel
- Historique des mesures
- Alertes et notifications
- Graphiques interactifs

**Identifiants par défaut** :
- Utilisateur : `admin`
- Mot de passe : `admin` (à changer lors première connexion)

### Administration Base de Données

**URL** : `http://localhost:8080` (accès local uniquement)

**Fonctionnalités** :
- Gestion des sondes et emplacements
- Configuration des seuils d'alerte
- Export des données
- Maintenance de la base

**Identifiants** :
- Serveur : `mariadb`
- Utilisateur : `root` ou `mqtt_user`
- Mot de passe : configuré dans `.env`

## Démarrage du Système

### Première Installation

1. **Prérequis** :
   - Docker et Docker Compose installés
   - Accès administrateur à la machine

2. **Téléchargement** :
   ```bash
   git clone <repository_url>
   cd Projet_Python
   ```

3. **Configuration** :
   ```bash
   # Copier le fichier d'environnement
   cp .env.example .env
   
   # Éditer les identifiants
   nano .env
   ```

4. **Démarrage** :
   ```bash
   docker compose up -d
   ```

5. **Vérification** :
   ```bash
   docker compose ps
   # Tous les services doivent être "Up"
   ```

### Utilisation Quotidienne

**Démarrer le système** :
```bash
docker compose up -d
```

**Vérifier l'état** :
```bash
docker compose ps
```

**Arrêter le système** :
```bash
docker compose down
```

## Gestion des Sondes

### Ajouter une Nouvelle Sonde

#### Étape 1 : Enregistrement dans la Base de Données

1. **Accéder à phpMyAdmin** : `http://localhost:8080`
2. **Sélectionner la base** : `Marais_R_Site`
3. **Ajouter la sonde** :
   ```sql
   INSERT INTO sonde (nom_sonde, date_installation_sonde) 
   VALUES ('Sonde_Bureau_01', NOW());
   ```
4. **Noter l'ID généré** (ex: `id_sonde = 6`)
5. **Créer l'emplacement** :
   ```sql
   INSERT INTO emplacement (nom_emplacement, id_sonde) 
   VALUES ('Bureau Étage 1 - Poste A', 6);
   ```

#### Étape 2 : Configuration Physique de la Sonde

**Paramètres MQTT à configurer sur la sonde** :

| Paramètre | Valeur |
|-----------|--------|
| Broker MQTT | `marais2026.btssn.ovh` (ou IP locale) |
| Port | `8883` |
| Nom d'utilisateur | `marais2026` |
| Mot de passe | `hyrome49#` |
| Topic Publication | `marais/sondes/{MAC_ADRESSE}/` |
| Sécurité | TLS/SSL activé |
| Certificat CA | Utiliser le certificat fourni |

**Exemple de topic** : `marais/sondes/A1:B2:C3:D4:E5:F6/`

#### Étape 3 : Test de Connexion

```bash
# Test depuis le serveur
mosquitto_pub -h localhost -p 8883 \
  -t "marais/sondes/A1:B2:C3:D4:E5:F6/" \
  -m '{"timestamp":"2025-05-12 14:30:00","mesure":[{"CO2":450,"Température":22.5}]}' \
  -u marais2026 -P "hyrome49#" \
  --cafile mosquitto/config/ca.crt --insecure
```

### Vérifier le Fonctionnement

1. **Dans Grafana** : Les données doivent apparaître dans les graphiques
2. **Dans phpMyAdmin** : Vérifier les insertions dans la table `mesure`
3. **Logs système** :
   ```bash
   docker compose logs app_python --tail 20
   ```

## Configuration des Seuils d'Alerte

### Seuils par Défaut

| Capteur | Seuil Alerte | Seuil Danger | Action recommandée |
|---------|--------------|--------------|-------------------|
| CO2 | 1000 ppm | 1500 ppm | Ventilation accrue |
| Température | 30°C | 35°C | Contrôle climatisation |
| Humidité | 70% | 85% | Déshumidification |
| PM 2.5 | 35 µg/m³ | 55 µg/m³ | Vérification filtres |
| PM 10 | 50 µg/m³ | 100 µg/m³ | Surveillance air |
| TVOC | 500 ppb | 1000 ppb | Aération renforcée |

### Modifier les Seuils

**Via phpMyAdmin** :
1. Accéder à la table `type_info_mesure`
2. Modifier les colonnes :
   - `valeur_alerte_seuil`
   - `valeur_danger_seuil`

**Exemple SQL** :
```sql
UPDATE type_info_mesure 
SET valeur_alerte_seuil = 800, valeur_danger_seuil = 1200 
WHERE nom_type_mesure = 'CO2';
```

Les nouveaux seuils sont automatiquement envoyés aux sondes dans la minute.

## Visualisation des Données

### Tableaux de Bord Grafana

#### Tableau de Bord Principal

**Accès** : `http://localhost:3000/d/main`

**Panels disponibles** :
- **CO2 en temps réel** : Graphique des 24 dernières heures
- **Température et Humidité** : Courbes combinées
- **Qualité de l'air** : Indice PM 2.5/PM 10
- **Alertes actives** : Compteur et liste
- **Carte des emplacements** : Vue géographique des sondes

#### Personnalisation

**Créer un nouveau dashboard** :
1. Cliquer sur `+` → `Dashboard`
2. Ajouter des panels avec le bouton `Add panel`
3. Sélectionner les données depuis `marais_r_site`

**Filtres temporels** :
- Dernière heure
- Dernières 24 heures  
- Dernière semaine
- Plage personnalisée

### Export des Données

**Export CSV depuis Grafana** :
1. Ouvrir le graphique souhaité
2. Cliquer sur l'icône de téléchargement
3. Choisir `CSV`

**Export complet via phpMyAdmin** :
```sql
SELECT 
    m.date_heure_mesure,
    e.nom_emplacement,
    t.nom_type_mesure,
    m.valeur_mesure,
    a.niveau_alerte
FROM mesure m
JOIN emplacement e ON m.id_emplacement = e.id_emplacement
JOIN type_info_mesure t ON m.id_type_mesure = t.id_type_mesure
JOIN alerte a ON m.id_alerte = a.id_alerte
WHERE m.date_heure_mesure >= '2025-05-01'
ORDER BY m.date_heure_mesure DESC;
```

## Alertes et Notifications

### Types d'Alertes

**Niveau 1 - Normal** : Valeurs dans les limites acceptables
- Couleur verte dans Grafana
- Aucune action requise

**Niveau 2 - Attention** : Dépassement seuil d'alerte
- Couleur orange dans Grafana
- Actions correctives recommandées

**Niveau 3 - Danger** : Dépassement seuil critique
- Couleur rouge dans Grafana
- Actions immédiates requises

### Configuration des Notifications

**Email (optionnel)** :
1. Dans Grafana : `Configuration` → `Alerting` → `Notification channels`
2. Créer un canal `Email`
3. Configurer les destinataires

**Webhook (pour intégrations)** :
```json
{
  "url": "https://votre-webhook.com/alerts",
  "method": "POST",
  "headers": {
    "Authorization": "Bearer votre-token"
  }
}
```

## Maintenance et Dépannage

### Vérifications Quotidiennes

**État des services** :
```bash
docker compose ps
# Tous les services doivent être "Up"
```

**Dernières mesures** :
```bash
docker compose logs app_python --tail 10
# Vérifier les insertions récentes
```

**Espace disque** :
```bash
df -h
# Vérifier l'espace disponible
```

### Problèmes Courants

#### Sonde ne communique pas

**Symptôme** : Pas de données dans Grafana

**Diagnostic** :
```bash
# Vérifier si Mosquitto fonctionne
docker compose ps mosquitto

# Vérifier les logs
docker compose logs mosquitto --tail 20

# Tester la connexion
mosquitto_pub -h localhost -p 8883 -t "test" -m "test" \
  -u marais2026 -P "hyrome49#" \
  --cafile mosquitto/config/ca.crt --insecure
```

**Solutions** :
- Vérifier la configuration réseau de la sonde
- Confirmer les identifiants MQTT
- Vérifier le certificat TLS

#### Grafana inaccessible

**Symptôme** : Page blanche ou erreur 502

**Diagnostic** :
```bash
docker compose logs grafana --tail 20
docker compose restart grafana
```

#### Base de données lente

**Symptôme** : Graphiques qui se chargent lentement

**Diagnostic** :
```bash
# Vérifier la taille de la base
docker compose exec mariadb mariadb -u root -p -e "
  SELECT table_name, 
         ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'Size (MB)'
  FROM information_schema.tables 
  WHERE table_schema = 'Marais_R_Site'
  ORDER BY (data_length + index_length) DESC;
"
```

### Nettoyage des Données

**Purge des anciennes mesures** :
```sql
-- Supprimer les mesures de plus de 1 an
DELETE FROM mesure 
WHERE date_heure_mesure < DATE_SUB(NOW(), INTERVAL 1 YEAR);
```

**Optimisation de la base** :
```sql
OPTIMIZE TABLE mesure;
OPTIMIZE TABLE sonde;
OPTIMIZE TABLE emplacement;
```

## Sauvegarde et Restauration

### Sauvegarde Automatique

**Script de sauvegarde quotidien** :
```bash
#!/bin/bash
# backup_marais.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/marais_r_site"

# Créer le répertoire
mkdir -p $BACKUP_DIR

# Sauvegarder la base de données
docker compose exec -T mariadb mysqldump -u root -p$MYSQL_ROOT_PASSWORD \
  Marais_R_Site > $BACKUP_DIR/bdd_$DATE.sql

# Sauvegarder les certificats
tar -czf $BACKUP_DIR/certs_$DATE.tar.gz mosquitto/config/*.crt mosquitto/config/*.key

# Supprimer les sauvegardes de plus de 30 jours
find $BACKUP_DIR -name "*.sql" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete

echo "Sauvegarde terminée: $DATE"
```

**Programmation avec cron** :
```bash
# Exécuter tous les jours à 2h du matin
0 2 * * * /chemin/vers/backup_marais.sh
```

### Restauration

**Base de données** :
```bash
docker compose exec -i mariadb mariadb -u root -p Marais_R_Site < backup_20250512.sql
```

**Certificats** :
```bash
tar -xzf certs_backup.tar.gz -C mosquitto/config/
docker compose restart mosquitto
```

## Support et Assistance

### Ressources Disponibles

**Documentation technique** :
- `DOCUMENTATION_TECHNIQUE.md` - Documentation complète pour administrateurs
- `DOCUMENTATION_DEVELOPPEUR.md` - Guide pour les développeurs

**Logs utiles pour le support** :
```bash
# Logs complets pour diagnostic
docker compose logs > logs_complets_$(date +%Y%m%d).txt

# Logs par service
docker compose logs app_python > logs_python_$(date +%Y%m%d).txt
docker compose logs mosquitto > logs_mqtt_$(date +%Y%m%d).txt
docker compose logs mariadb > logs_bdd_$(date +%Y%m%d).txt
```

### Contact Support

**Informations à fournir** :
- Version du système : `docker compose version`
- Logs des services concernés
- Description détaillée du problème
- Heure de survenance du problème
- Actions déjà tentées

**Commande de diagnostic complet** :
```bash
#!/bin/bash
# diagnostic_complet.sh

echo "=== Diagnostic Marais R Site ==="
echo "Date: $(date)"
echo "Version Docker: $(docker --version)"
echo "Version Docker Compose: $(docker compose version)"
echo ""

echo "=== État des services ==="
docker compose ps
echo ""

echo "=== Espace disque ==="
df -h
echo ""

echo "=== Mémoire ==="
free -h
echo ""

echo "=== Réseau ==="
netstat -tlnp | grep -E "(1883|8883|3306|3000|8080)"
echo ""

echo "=== Logs récents ==="
docker compose logs --tail 20
```

## Bonnes Pratiques

### Sécurité

- **Changer les mots de passe par défaut** lors de la première installation
- **Mettre à jour régulièrement** les composants Docker
- **Limiter l'accès réseau** : les services ne doivent être accessibles qu'en local
- **Sauvegarder régulièrement** les certificats et la base de données

### Performance

- **Surveiller l'espace disque** : les données peuvent s'accumuler rapidement
- **Nettoyer périodiquement** les anciennes mesures
- **Optimiser les requêtes** dans Grafana pour éviter les surcharges

### Utilisation

- **Vérifier les alertes** quotidiennement
- **Documenter les changements** de configuration
- **Former les utilisateurs** à l'interprétation des données
- **Établir des procédures** d'intervention en cas d'alerte

Ce guide est conçu pour les utilisateurs et administrateurs du système Marais R Site. Pour des informations techniques détaillées, consultez la documentation développeur.
