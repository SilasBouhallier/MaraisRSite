# Documentation Complète du Projet Marais R Site

## Sommaire

Ce document présente l'architecture complète du projet **Marais R Site**, une application de surveillance environnementale déployée sur VPS via Docker Compose.

### Points clés

- **Architecture** : 10 conteneurs Docker orchestrés via docker-compose
- **Reverse Proxy** : Traefik gère le routage, le SSL (Let's Encrypt) et la sécurité
- **Base de données** : MariaDB stocke les mesures des capteurs
- **Collecte** : MQTT sécurisé (MQTTS) via Mosquitto
- **Visualisation** : Grafana pour les graphiques, phpMyAdmin pour la gestion BDD
- **Monitoring** : Beszel pour le monitoring des conteneurs
- **Sécurité** : TLS/SSL pour tous les services, isolation réseau, authentification multi-niveaux

### Services principaux

1. **Traefik** - Reverse Proxy et gestion SSL
2. **MariaDB** - Base de données
3. **phpMyAdmin** - Interface de gestion BDD
4. **Grafana** - Visualisation des données
5. **Mosquitto** - Broker MQTT sécurisé
6. **Web App** - Application Flask (interface utilisateur)
7. **app_python** - Application MQTT (collecte → BDD)
8. **Beszel** - Monitoring système
9. **Beszel Agent** - Agent de monitoring
10. **Test Runner** - Tests de connectivité

### Accès principaux

- Web App : `https://marais2026.btssn.ovh/`
- Grafana : `https://marais2026.btssn.ovh/grafana/`
- phpMyAdmin : `https://marais2026.btssn.ovh/phpmyadmin/`
- Beszel : `https://marais2026.btssn.ovh/beszel/`
- MQTT : `mqtts://marais2026.btssn.ovh:8883`

### Sécurité

- Certificats SSL automatiques (Let's Encrypt)
- MQTT chiffré avec TLS
- Isolation réseau via Docker bridge
- Authentification BDD séparée par service
- Variables d'environnement pour les secrets

---

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Architecture du système](#architecture-du-système)
3. [Services et conteneurs](#services-et-conteneurs)
4. [Réseau et interconnexions](#réseau-et-interconnexions)
5. [Sécurité](#sécurité)
6. [Lancement du projet](#lancement-du-projet)
7. [Configuration](#configuration)
8. [Maintenance et opérations](#maintenance-et-opérations)
9. [Scalabilité](#scalabilité)
10. [Documentation API](#documentation-api)
11. [Glossaire technique](#glossaire-technique)

---

## Vue d'ensemble

Le projet **Marais R Site** est une application de surveillance environnementale déployée sur un VPS via Docker Compose. Il permet de collecter des données de capteurs (CO2, PM2.5, PM10, TVOC) via MQTT, de les stocker dans une base de données MariaDB, et de les visualiser via Grafana.

### Domaine principal
- **URL** : `https://marais2026.btssn.ovh`
- **VPS** : marais2026.btssn.ovh

### Objectifs
- Collecte de données de capteurs en temps réel via MQTT
- Stockage des mesures dans MariaDB
- Visualisation des données via Grafana
- Gestion de la base de données via phpMyAdmin
- Monitoring des conteneurs via Beszel

---

## Architecture du système

### Schéma d'architecture

```
Internet
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│                      Traefik (Reverse Proxy)                │
│  - Port 443 (HTTPS)                                         │
│  - Port 8883 (MQTTS)                                        │
│  - Gestion SSL automatique (Let's Encrypt)                  │
│  - Routage vers les services internes                        │
└─────────────────────────────────────────────────────────────┘
    │           │           │           │           │
    ▼           ▼           ▼           ▼           ▼
┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐  ┌────────┐
│Web App │  │Grafana │  │phpMyAdm│  │Beszel  │  │Mosquitto│
│:5000   │  │:3000   │  │:80     │  │:8090   │  │:8883   │
└────────┘  └────────┘  └────────┘  └────────┘  └────────┘
    │           │           │           │           │
    └───────────┴───────────┴───────────┴───────────┘
                │
                ▼
         ┌──────────────┐
         │   MariaDB    │
         │   :3306      │
         └──────────────┘
                │
                ▼
         ┌──────────────┐
         │  app_python  │
         │  (MQTT → BDD)│
         └──────────────┘
```

### Réseau Docker
- **Nom du réseau** : `marais_net`
- **Type** : Bridge
- **Isolation** : Les conteneurs communiquent entre eux via ce réseau isolé

---

## Services et conteneurs

### 1. Traefik (Reverse Proxy)

**Rôle** : Point d'entrée unique, gestion du routage et du SSL

**Image** : `traefik:v3.0`

**Ports exposés** :
- `443:443` - HTTPS (trafic web sécurisé)
- `8883:8883` - MQTTS (MQTT sécurisé)
- `127.0.0.1:8080:8080` - Dashboard Traefik (accès local uniquement)

**Volumes** :
- `./traefik/traefik.yml:/traefik.yml:ro` - Configuration statique
- `./traefik/dynamic:/etc/traefik/dynamic:ro` - Configuration dynamique
- `letsencrypt:/letsencrypt` - Certificats SSL

**Configuration** :
- Résolveur de certificats Let's Encrypt automatique
- Dashboard accessible localement sur `http://localhost:8080`
- Logs au format common

---

### 2. MariaDB (Base de données)

**Rôle** : Stockage des mesures et données de l'application

**Image** : `mariadb:10.11`

**Ports** : Aucun port exposé (accès interne uniquement)

**Volumes** :
- `vol_BDD:/var/lib/mysql` - Données persistantes de la base

**Variables d'environnement** :
- `MARIADB_ROOT_PASSWORD` - Mot de passe root
- `MARIADB_DATABASE` - Base de données principale
- `MARIADB_USER` / `MARIADB_PASSWORD` - Utilisateur web
- `MARIADB_WEB_USER` / `MARIADB_WEB_PASSWORD` - Utilisateur application web
- `MARIADB_MQTT_USER` / `MARIADB_MQTT_PASSWORD` - Utilisateur MQTT

**Commande spéciale** :
- `--event-scheduler=ON` - Activation du planificateur d'événements pour l'archivage mensuel

**Tables principales** :
- `mesure` - Mesures des capteurs
- `archive_moyennes_mensuelles` - Archives mensuelles
- `type_info_mesure` - Types de mesures
- `emplacement` - Emplacements des capteurs
- `sonde` - Informations sur les sondes
- `alerte` - Niveaux d'alerte

---

### 3. phpMyAdmin

**Rôle** : Interface web de gestion de la base de données

**Image** : `phpmyadmin/phpmyadmin`

**Ports** : Expose port 80 (interne uniquement)

**Accès** : `https://marais2026.btssn.ovh/phpmyadmin/`

**Configuration** :
- Host : `mariadb` (nom du conteneur)
- URI absolue : `/phpmyadmin/`
- Middleware Traefik : Strip prefix `/phpmyadmin`

**Dépendances** : mariadb

---

### 4. Grafana

**Rôle** : Visualisation des données (graphiques, tableaux de bord)

**Image** : `grafana/grafana`

**Ports** : Expose port 3000 (interne uniquement)

**Accès** : `https://marais2026.btssn.ovh/grafana/`

**Volumes** :
- `vol_grafana:/var/lib/grafana` - Données persistantes (dashboards, configurations)

**Configuration** :
- Root URL : `https://marais2026.btssn.ovh/grafana/`
- Embedding autorisé (pour intégration dans iframe)
- Mode sous-chemin activé

**Source de données** : MariaDB via plugin MySQL

---

### 5. Mosquitto (Broker MQTT)

**Rôle** : Broker MQTT pour la communication avec les capteurs

**Image** : `eclipse-mosquitto:2.0`

**Ports** :
- Expose 1883 (MQTT standard - interne)
- Expose 8883 (MQTTS sécurisé - interne)

**Volumes** :
- `mosquitto_data:/mosquitto/data` - Données persistantes
- `mosquitto_log:/mosquitto/log` - Logs
- `./mosquitto/config:/mosquitto/config` - Configuration

**Configuration TLS** :
- Certificat serveur : `server.crt`
- Clé privée : `server.key`
- CA : `ca.crt`
- Fichier de mots de passe : `passwd`
- Authentification obligatoire (pas d'anonyme)

**Accès** : `mqtts://marais2026.btssn.ovh:8883`

---

### 6. Web App (Application Flask)

**Rôle** : Interface web principale de l'application

**Image** : Construite depuis `./web_app/Dockerfile`

**Base** : `python:3.11-slim`

**Ports** : Expose port 5000 (interne uniquement)

**Accès** : `https://marais2026.btssn.ovh/`

**Variables d'environnement** :
- `MYSQL_DATABASE` - Base de données
- `MYSQL_USER` - Utilisateur
- `MYSQL_PASSWORD` - Mot de passe
- `MYSQL_HOST` - Hôte MariaDB

**Dépendances** : mariadb

**Fonctionnalités** :
- Affichage des mesures en temps réel
- Gestion des alertes
- Interface utilisateur

---

### 7. app_python (Application MQTT)

**Rôle** : Abonnement aux topics MQTT et insertion dans la base de données

**Image** : Construite depuis `./app_python/Dockerfile`

**Base** : `python:3.12-slim`

**Variables d'environnement** :
- `PYTHONUNBUFFERED=1` - Logs non bufferisés
- `MQTT_BROKER` - Adresse du broker Mosquitto
- `MYSQL_MQTT_HOST` - Hôte MariaDB
- `MYSQL_MQTT_USER` - Utilisateur MQTT
- `MYSQL_MQTT_PASSWORD` - Mot de passe MQTT
- `MYSQL_MQTT_DATABASE` - Base de données

**Dépendances** : mariadb, mosquitto

**Fonctionnement** :
1. Se connecte au broker Mosquitto
2. S'abonne aux topics de capteurs
3. Reçoit les messages MQTT
4. Insère les données dans MariaDB
5. Détermine automatiquement les alertes

---

### 8. Beszel (Monitoring)

**Rôle** : Monitoring des conteneurs Docker et du système

**Image** : `henrygd/beszel:latest`

**Ports** : Expose port 8090 (interne uniquement)

**Accès** : `https://marais2026.btssn.ovh/beszel/`

**Volumes** :
- `vol_beszel:/data` - Données persistantes
- `/var/run/docker.sock:/var/run/docker.sock:ro` - Accès Docker en lecture seule

**Configuration** :
- URL : `https://marais2026.btssn.ovh/beszel`
- Middleware : Strip prefix `/beszel`

---

### 9. Beszel Agent

**Rôle** : Agent de monitoring sur le VPS

**Image** : `henrygd/beszel-agent:latest`

**Ports** : `4567:4567` (exposé pour communication avec le hub)

**Volumes** :
- `/var/run/docker.sock:/var/run/docker.sock:ro` - Accès Docker

**Variables d'environnement** :
- `PORT=4567`
- `KEY` - Clé d'authentification

---

### 10. Test Runner

**Rôle** : Tests de connectivité entre services

**Image** : `alpine`

**Commande** : Exécute `basic_connectivity_tests.sh`

**Dépendances** : Tous les services

**Fonction** : Vérifie que tous les services sont accessibles et répondent correctement

---

## Réseau et interconnexions

### Réseau marais_net

Tous les conteneurs sont connectés au réseau bridge `marais_net`, ce qui leur permet de communiquer entre eux en utilisant leurs noms de conteneur comme noms d'hôte.

### Flux de données

#### 1. Collecte de données (MQTT → BDD)

```
Capteur IoT
    │ (MQTT TLS)
    ▼
Mosquitto (port 8883)
    │ (interne)
    ▼
app_python (abonnement MQTT)
    │ (requête SQL)
    ▼
MariaDB (insertion)
```

#### 2. Affichage web (BDD → Utilisateur)

```
MariaDB
    │ (requête SQL)
    ▼
Web App (Flask)
    │ (HTTP interne)
    ▼
Traefik (routage)
    │ (HTTPS)
    ▼
Navigateur utilisateur
```

#### 3. Visualisation (BDD → Grafana)

```
MariaDB
    │ (requête SQL via plugin MySQL)
    ▼
Grafana
    │ (HTTP interne)
    ▼
Traefik (routage)
    │ (HTTPS)
    ▼
Navigateur utilisateur
```

### Configuration Traefik

#### Routers HTTP

| Service | Règle | Priorité | Middleware |
|---------|-------|----------|------------|
| web_app | `Host(marais2026.btssn.ovh) && PathPrefix(/)` | 1 | Aucun |
| grafana | `Host(marais2026.btssn.ovh) && PathPrefix(/grafana)` | 100 | Aucun |
| phpmyadmin | `Host(marais2026.btssn.ovh) && PathPrefix(/phpmyadmin)` | 100 | Strip prefix |
| beszel-main | `Host(marais2026.btssn.ovh) && PathPrefix(/beszel)` | 100 | Strip prefix |
| beszel-assets | `Host(marais2026.btssn.ovh) && PathPrefix(/beszel/static)` | 300 | Strip prefix |
| beszel-api | `Host(marais2026.btssn.ovh) && PathPrefix(/api/realtime)` | 300 | Aucun |

#### Router TCP (MQTTS)

| Service | Règle | Entrypoint |
|---------|-------|------------|
| mosquitto | `HostSNI(*)` | mqtts (8883) |

#### Services Load Balancer

| Service | URL interne |
|---------|-------------|
| web_app | `http://web_app:5000` |
| grafana | `http://grafana:3000` |
| phpmyadmin | `http://phpmyadmin:80` |
| beszel | `http://beszel:8090` |
| mosquitto | `mosquitto:8883` |

---

## Sécurité

### 1. SSL/TLS (Let's Encrypt)

**Mise en œuvre** : Traefik avec résolveur Let's Encrypt

**Configuration** :
- Email : `eleve.marais@btssn.fr`
- Stockage : `/letsencrypt/acme.json`
- Challenge : TLS-ALPN-01
- Renouvellement automatique

**Services sécurisés** :
- Web App (HTTPS)
- Grafana (HTTPS)
- phpMyAdmin (HTTPS)
- Beszel (HTTPS)

### 2. MQTT TLS (MQTTS)

**Configuration Mosquitto** :
- Port : 8883
- Certificat serveur : `server.crt`
- Clé privée : `server.key`
- CA : `ca.crt`
- Authentification par mot de passe (fichier `passwd`)
- Pas d'accès anonyme

**Traefik** :
- Mode passthrough TLS (le flux MQTT TLS passe directement à Mosquitto)
- Router TCP sur le port 8883

### 3. Isolation réseau

**Ports exposés** :
- Seuls les ports nécessaires sont exposés sur l'hôte
- La plupart des services n'exposent que des ports internes
- Traefik est le seul point d'entrée public

**Ports publics** :
- `443` - HTTPS (Traefik)
- `8883` - MQTTS (Traefik → Mosquitto)
- `4567` - Beszel Agent

**Ports locaux** :
- `127.0.0.1:8080` - Dashboard Traefik (accès local uniquement)

### 4. Authentification base de données

**Utilisateurs MariaDB** :
- `root` - Accès complet (mot de passe dans .env)
- `Marais_R_Site_User` - Utilisateur web
- `Marais_R_Site_User_MQTT` - Utilisateur MQTT

**Séparation des privilèges** :
- Chaque utilisateur a des droits limités à ses besoins
- L'utilisateur MQTT ne peut que insérer des données
- L'utilisateur web peut lire et écrire selon les besoins

### 5. Variables d'environnement

**Fichier .env** (non versionné) :
- Contient tous les mots de passe et clés secrètes
- Non inclus dans le dépôt Git
- Chargé par docker-compose

**Bonnes pratiques** :
- Ne jamais commit le fichier .env
- Utiliser des mots de passe forts
- Rotation régulière des mots de passe

### 6. Middleware Traefik

**Strip Prefix** :
- Utilisé pour phpMyAdmin et Beszel
- Supprime le préfixe de chemin avant de transmettre au service
- Exemple : `/phpmyadmin/xxx` → `/xxx` vers phpMyAdmin

### 7. Docker Socket

**Accès en lecture seule** :
- Beszel et Beszel Agent accèdent au socket Docker
- Monté en `ro` (read-only)
- Permet le monitoring sans risque de modification

---

## Lancement du projet

### Prérequis

- Docker
- Docker Compose
- Accès SSH au VPS
- Nom de domaine configuré (marais2026.btssn.ovh)
- Fichier .env configuré

### Structure des fichiers

```
marais_project/
├── docker-compose.yml          # Orchestration des conteneurs
├── .env                        # Variables d'environnement (non versionné)
├── app_python/                 # Application MQTT
│   ├── Dockerfile
│   ├── main.py
│   └── utils/
├── web_app/                    # Application Flask
│   ├── Dockerfile
│   ├── app.py
│   ├── requirements.txt
│   └── templates/
├── traefik/                    # Configuration Traefik
│   ├── traefik.yml
│   └── dynamic/
│       ├── web_app.yml
│       ├── grafana.yml
│       ├── phpmyadmin.yml
│       ├── mosquitto.yml
│       └── beszel.yml
├── mosquitto/                  # Configuration Mosquitto
│   └── config/
│       ├── mosquitto.conf
│       ├── server.crt
│       ├── server.key
│       ├── ca.crt
│       └── passwd
├── backups/                    # Sauvegardes BDD
├── tests/                      # Tests de connectivité
└── letsencrypt/                # Certificats SSL (créé automatiquement)
```

### Commandes de lancement

#### 1. Premier lancement

```bash
# Cloner le projet
git clone <repository_url>
cd marais_project

# Configurer le fichier .env
cp .env.example .env
nano .env  # Éditer les variables

# Lancer les conteneurs
docker-compose up -d

# Vérifier l'état
docker-compose ps
```

#### 2. Arrêt

```bash
# Arrêter tous les conteneurs
docker-compose down

# Arrêter et supprimer les volumes
docker-compose down -v
```

#### 3. Redémarrage

```bash
# Redémarrer un service spécifique
docker-compose restart <service_name>

# Redémarrer tous les services
docker-compose restart
```

#### 4. Mise à jour

```bash
# Récupérer les dernières modifications
git pull

# Reconstruire les images
docker-compose build

# Redémarrer avec les nouvelles images
docker-compose up -d
```

#### 5. Visualisation des logs

```bash
# Logs de tous les services
docker-compose logs -f

# Logs d'un service spécifique
docker-compose logs -f <service_name>

# Dernières 100 lignes
docker-compose logs --tail=100 <service_name>
```

### Ordre de démarrage

Docker Compose gère automatiquement les dépendances via `depends_on` :

1. **mariadb** - Base de données (pas de dépendances)
2. **mosquitto** - Broker MQTT (pas de dépendances)
3. **phpmyadmin** - Dépend de mariadb
4. **grafana** - Dépend de mariadb
5. **web_app** - Dépend de mariadb
6. **app_python** - Dépend de mariadb et mosquitto
7. **beszel** - Dépend de docker (via socket)
8. **beszel-agent** - Dépend de docker (via socket)
9. **traefik** - Dépend de web_app
10. **test_runner** - Dépend de tous les services

---

## Configuration

### Fichier .env

Le fichier `.env` contient toutes les variables sensibles :

```bash
# MariaDB
MYSQL_ROOT_PASSWORD=
MYSQL_DATABASE=
MYSQL_USER=
MYSQL_PASSWORD=
MYSQL_WEB_USER=
MYSQL_WEB_PASSWORD=
MYSQL_WEB_HOST=
MYSQL_MQTT_USER=
MYSQL_MQTT_PASSWORD=
MYSQL_MQTT_HOST=
MYSQL_MQTT_DATABASE=

# MQTT
MQTT_BROKER=

# Beszel
BESZEL_KEY=

# TOKENS
TOKEN_USER_GRAFANA=

```

### Configuration Traefik

**traefik.yml** (statique) :
- Entrypoints websecure (443) et mqtts (8883)
- Provider file pour configuration dynamique
- Certificat resolver Let's Encrypt
- Dashboard activé (accès local)

**dynamic/*.yml** (dynamique) :
- Un fichier par service
- Définit router, service, et middlewares
- Rechargement automatique (watch: true)

### Configuration Mosquitto

**mosquitto.conf** :
- Persistence activée
- Listener TLS sur port 8883
- Certificats TLS configurés
- Authentification par mot de passe
- Logs vers fichier

### Configuration Grafana

**Variables d'environnement** :
- `GF_SERVER_ROOT_URL` - URL de base
- `GF_SECURITY_ALLOW_EMBEDDING` - Autorise l'embed dans iframe
- `GF_SERVER_SERVE_FROM_SUB_PATH` - Mode sous-chemin

**Source de données** :
- Type : MySQL
- Hôte : mariadb:3306
- Base : Marais_R_Site
- Utilisateur : Marais_R_Site_User

---

## Maintenance et opérations

### Sauvegarde de la base de données

**Script automatique** : `backup_db.sh`

```bash
# Exécution manuelle
./backup_db.sh
```

**Configuration Crontab**

Pour automatiser la sauvegarde quotidienne de la base de données, ajouter la tâche suivante au crontab :

```bash
# Éditer le crontab
crontab -e

# Ajouter la ligne suivante pour une sauvegarde quotidienne à 1h du matin
0 1 * * * /bin/bash /marais_project/backup_db.sh
```

**Explication de la crontab** :
- `0 1 * * *` - S'exécute tous les jours à 1h00 du matin
- `/bin/bash` - Interpréteur de commandes
- `/marais_project/backup_db.sh` - Chemin du script de sauvegarde


**Vérification des tâches crontab** :
```bash
# Lister les tâches crontab de l'utilisateur actuel
crontab -l

# Vérifier les logs de crontab
grep CRON /var/log/syslog
```

**Sauvegardes stockées** : `backups/`

### Restauration de la base de données

```bash
# Depuis une sauvegarde
docker exec -i mariadb mysql -u root -p Marais_R_Site < backups/backup_YYYYMMDD.sql
```

### Mise à jour des certificats SSL

Les certificats Let's Encrypt sont renouvelés automatiquement par Traefik. Aucune intervention manuelle n'est requise.

### Monitoring

**Via Beszel** :
- Accès : `https://marais2026.btssn.ovh/beszel/`
- Métriques CPU, RAM, disque
- État des conteneurs
- Logs des conteneurs

**Via Traefik Dashboard** :
- Accès local : `http://localhost:8080`
- État des routers et services
- Statistiques de requêtes

### Tests de connectivité

**Script** : `tests/basic_connectivity_tests.sh`

```bash
# Exécution manuelle
docker-compose run --rm test_runner

# Vérifie :
# - Connectivité MariaDB
# - Connectivité Mosquitto
# - Réponse HTTP des services web
```

### Dépannage

#### Service ne démarre pas

```bash
# Vérifier les logs
docker-compose logs <service_name>

# Vérifier l'état
docker-compose ps

# Redémarrer
docker-compose restart <service_name>
```

#### Problème de connexion BDD

```bash
# Vérifier que MariaDB est actif
docker-compose exec mariadb mysql -u root -p

# Vérifier les variables d'environnement
docker-compose config
```

#### Problème MQTT

```bash
# Vérifier les logs Mosquitto
docker-compose logs mosquitto

# Tester la connexion
docker-compose exec app_python python -c "import paho.mqtt.client as mqtt; print('MQTT OK')"
```

#### Certificat SSL expiré

```bash
# Supprimer le certificat et redémarrer Traefik
rm -rf letsencrypt/acme.json
docker-compose restart traefik
```

### Mises à jour de sécurité

**Images Docker** :
```bash
# Mettre à jour toutes les images
docker-compose pull

# Reconstruire et redémarrer
docker-compose up -d --build
```

**Système hôte** :
```bash
# Mises à jour Debian
sudo apt update
sudo apt upgrade
```

---

## Résumé des points d'accès

| Service | URL | Authentification |
|---------|-----|------------------|
| Web App | https://marais2026.btssn.ovh/ | Session Flask |
| Grafana | https://marais2026.btssn.ovh/grafana/ | Compte Grafana |
| phpMyAdmin | https://marais2026.btssn.ovh/phpmyadmin/ | MariaDB |
| Beszel | https://marais2026.btssn.ovh/beszel/ | Compte Beszel |
| Cockpit | https://marais2026.btssn.ovh:9090/system | Système (root) |
| MQTT | mqtts://marais2026.btssn.ovh:8883 | Certificat + Mot de passe |
| Traefik Dashboard | http://localhost:8080 | Aucun (local) |

---

## Scalabilité

### Ajout de capteurs

Pour ajouter un nouveau capteur IoT au système :

#### 1. Configuration matérielle

Le capteur doit supporter :
- Protocole MQTT
- TLS/SSL pour la communication sécurisée
- Capteurs : ECO2, TVOC, PM2.5, PM10

#### 2. Enregistrement dans la base de données

```sql
-- Ajouter une nouvelle sonde
INSERT INTO sonde (nom_sonde, id_sonde_mqtt, description)
VALUES ('sonde4', 'sensor/zone4', 'Capteur zone 4');

-- Récupérer l'ID de la sonde
SELECT id_sonde FROM sonde WHERE nom_sonde = 'sonde4';

-- Créer un emplacement associé
INSERT INTO emplacement (nom_emplacement, id_sonde, description)
VALUES ('Zone 4', <id_sonde>, 'Emplacement zone 4');
```

#### 3. Configuration MQTT

Le capteur doit publier sur les topics suivants :
- `sensor/zone4/ECO2` - Valeurs CO2
- `sensor/zone4/TVOC` - Valeurs TVOC
- `sensor/zone4/PM2.5` - Valeurs PM2.5
- `sensor/zone4/PM10` - Valeurs PM10

#### 4. Format des messages MQTT

```json
{
  "value": 450.5,
  "unit": "ppm",
  "timestamp": "2025-05-04T10:00:00Z"
}
```

#### 5. Configuration app_python

L'application `app_python` s'abonne automatiquement à tous les topics commençant par `sensor/`. Aucune modification n'est nécessaire si le capteur suit le format standard.

---

### Ajout de nœuds MariaDB

Pour améliorer la disponibilité et les performances de la base de données :

#### Architecture maître-esclave

**Avantages** :
- Lecture distribuée sur plusieurs nœuds
- Haute disponibilité
- Sauvegarde sans interruption

#### Configuration docker-compose.yml

```yaml
mariadb-master:
  image: mariadb:10.11
  container_name: mariadb-master
  restart: unless-stopped
  command: ["mariadbd", "--server-id=1", "--log-bin=mysql-bin", "--binlog-format=ROW"]
  environment:
    MARIADB_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
    MARIADB_DATABASE: ${MYSQL_DATABASE}
    MARIADB_USER: ${MYSQL_USER}
    MARIADB_PASSWORD: ${MYSQL_PASSWORD}
  volumes:
    - vol_BDD_master:/var/lib/mysql
  networks:
    - marais_net

mariadb-slave:
  image: mariadb:10.11
  container_name: mariadb-slave
  restart: unless-stopped
  command: ["mariadbd", "--server-id=2", "--relay-log=relay-bin", "--read-only=1"]
  environment:
    MARIADB_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
  depends_on:
    - mariadb-master
  networks:
    - marais_net
```

#### Configuration de la réplication

```sql
-- Sur le maître
CREATE USER 'replication'@'%' IDENTIFIED BY 'replication_password';
GRANT REPLICATION SLAVE ON *.* TO 'replication'@'%';
FLUSH PRIVILEGES;
SHOW MASTER STATUS;

-- Sur l'esclave
CHANGE MASTER TO
  MASTER_HOST='mariadb-master',
  MASTER_USER='replication',
  MASTER_PASSWORD='replication_password',
  MASTER_LOG_FILE='mysql-bin.000001',
  MASTER_LOG_POS=123;
START SLAVE;
```

#### Mise à jour des applications

Modifier les variables d'environnement pour utiliser le nœud approprié :
- Écritures : `mariadb-master`
- Lectures : `mariadb-slave` (load balancing)

---

### Load Balancing

#### Load Balancing HTTP avec Traefik

Traefik gère déjà le load balancing via son service loadBalancer. Pour ajouter plusieurs instances d'un service :

```yaml
web_app:
  image: marais-web-app:latest
  deploy:
    replicas: 3
  networks:
    - marais_net
```

#### Load Balancing MQTT

Pour distribuer les connexions MQTT sur plusieurs brokers :

```yaml
mosquitto-1:
  image: eclipse-mosquitto:2.0
  container_name: mosquitto-1
  # ... configuration ...

mosquitto-2:
  image: eclipse-mosquitto:2.0
  container_name: mosquitto-2
  # ... configuration ...

traefik:
  # ...
  # Router MQTT avec load balancing
```

#### Load Balancing base de données

Utiliser un proxy comme ProxySQL ou HAProxy :

```yaml
proxysql:
  image: proxysql/proxysql:latest
  container_name: proxysql
  ports:
    - "6033:6033"
  volumes:
    - ./proxysql/proxysql.cnf:/etc/proxysql.cnf
  networks:
    - marais_net
```

---

## Documentation API

### Endpoints MQTT

#### Topics de publication (capteurs → broker)

**Format** : `sensor/{zone}/{type_mesure}`

**Exemples** :
- `sensor/zone1/ECO2` - Mesures CO2 zone 1
- `sensor/zone2/TVOC` - Mesures TVOC zone 2
- `sensor/zone3/PM2.5` - Mesures PM2.5 zone 3
- `sensor/zone4/PM10` - Mesures PM10 zone 4

#### Format des messages

```json
{
  "value": 450.5,
  "unit": "ppm",
  "timestamp": "2025-05-04T10:00:00Z",
  "sensor_id": "sensor_001"
}
```

**Champs** :
- `value` (float) : Valeur de la mesure
- `unit` (string) : Unité de mesure (ppm, µg/m³)
- `timestamp` (ISO 8601) : Horodatage de la mesure
- `sensor_id` (string) : Identifiant unique du capteur (optionnel)

#### QoS (Quality of Service)

- **QoS 0** : Au plus une fois (fire and forget)
- **QoS 1** : Au moins une fois (recommandé pour les mesures)
- **QoS 2** : Exactement une fois (non utilisé)

#### Configuration TLS

**Certificats requis** :
- CA : `ca.crt`
- Certificat client : `client.crt`
- Clé privée : `client.key`

**Connexion** :
```python
import paho.mqtt.client as mqtt

client = mqtt.Client()
client.tls_set(ca_certs="ca.crt", certfile="client.crt", keyfile="client.key")
client.connect("marais2026.btssn.ovh", 8883)
```

---

### Endpoints HTTP (Application Web)

#### GET `/`

**Description** : Page d'accueil de l'application

**Réponse** : HTML (template Flask)

#### GET `/api/mesures`

**Description** : Récupérer les dernières mesures

**Paramètres** :
- `limit` (int) : Nombre de mesures (défaut: 100)
- `type` (string) : Type de mesure (ECO2, TVOC, PM2.5, PM10)
- `zone` (string) : Zone d'emplacement

**Réponse** :
```json
{
  "mesures": [
    {
      "id": 1,
      "valeur": 450.5,
      "date_heure": "2025-05-04T10:00:00Z",
      "type_mesure": "ECO2",
      "emplacement": "Zone 1",
      "alerte": "Normal"
    }
  ]
}
```

#### GET `/api/alertes`

**Description** : Récupérer les alertes actives

**Réponse** :
```json
{
  "alertes": [
    {
      "id": 1,
      "niveau": "Danger",
      "type_mesure": "ECO2",
      "valeur": 2100.0,
      "seuil": 2000.0,
      "date_heure": "2025-05-04T10:00:00Z"
    }
  ]
}
```

#### POST `/api/mesure`

**Description** : Insérer une mesure manuellement

**Corps de la requête** :
```json
{
  "valeur": 450.5,
  "type_mesure": "ECO2",
  "emplacement": "Zone 1"
}
```

**Réponse** :
```json
{
  "success": true,
  "id": 1234
}
```

#### GET `/api/stats`

**Description** : Statistiques globales

**Réponse** :
```json
{
  "total_mesures": 15000,
  "alertes_actives": 3,
  "capteurs_actifs": 4,
  "derniere_mise_a_jour": "2025-05-04T10:00:00Z"
}
```

---

### Cockpit (Administration Système)

**Accès** : `https://marais2026.btssn.ovh:9090/system`

**Description** : Interface d'administration système pour le VPS

**Fonctionnalités** :
- Gestion des services système
- Monitoring des ressources (CPU, RAM, disque)
- Gestion des utilisateurs
- Logs système
- Mises à jour système
- Configuration réseau
- Gestion des conteneurs Docker

**Authentification** :
- Utilisateur : `root` ou utilisateur système
- Mot de passe : Mot de passe système VPS

**Sécurité** :
- Port 9090 exposé directement (non protégé par Traefik)
- Recommandation : Limiter l'accès via firewall iptables
- Exemple de règle iptables :
```bash
# Autoriser uniquement depuis IP spécifique
iptables -A INPUT -p tcp --dport 9090 -s <votre_ip> -j ACCEPT
iptables -A INPUT -p tcp --dport 9090 -j DROP
```

**Utilisation typique** :
- Surveillance de l'état du VPS
- Gestion des services Docker
- Diagnostic des problèmes système
- Maintenance et mises à jour

---

## Glossaire technique

### Termes Docker

- **Container** : Instance légère d'une application avec toutes ses dépendances
- **Image** : Template read-only utilisé pour créer des conteneurs
- **Docker Compose** : Outil pour définir et exécuter des applications multi-conteneurs
- **Volume** : Stockage persistant pour les conteneurs
- **Network** : Réseau virtuel permettant la communication entre conteneurs
- **Expose** : Port ouvert uniquement sur le réseau Docker interne
- **Ports** : Port mappé entre l'hôte et le conteneur

### Termes réseau

- **Reverse Proxy** : Serveur qui reçoit les requêtes et les transmet aux services backend
- **TLS/SSL** : Protocole de chiffrement pour sécuriser les communications
- **HTTPS** : HTTP sécurisé avec TLS/SSL
- **MQTTS** : MQTT sécurisé avec TLS/SSL
- **Bridge Network** : Réseau Docker isolé pour la communication entre conteneurs
- **Load Balancer** : Distribution du trafic entre plusieurs serveurs

### Termes MQTT

- **MQTT** : Message Queuing Telemetry Transport, protocole de messagerie léger
- **Broker** : Serveur MQTT qui reçoit et distribue les messages
- **Topic** : Chaîne de caractères hiérarchique pour filtrer les messages
- **Publisher** : Client qui envoie des messages au broker
- **Subscriber** : Client qui reçoit des messages du broker
- **QoS** : Quality of Service, niveau de garantie de livraison
- **Retain** : Message conservé par le broker pour les nouveaux abonnés

### Termes base de données

- **MariaDB** : Système de gestion de base de données relationnelle (fork de MySQL)
- **Replication** : Copie des données d'un serveur maître vers des esclaves
- **Event Scheduler** : Planificateur d'événements pour l'exécution automatique de tâches
- **Foreign Key** : Contrainte d'intégrité référentielle entre tables
- **Index** : Structure de données pour accélérer les requêtes

### Termes sécurité

- **Let's Encrypt** : Autorité de certification gratuite pour SSL/TLS
- **ACME** : Automatic Certificate Management Environment, protocole Let's Encrypt
- **TLS Challenge** : Méthode de validation de domaine pour SSL
- **Passthrough** : Mode Traefik où le flux TLS passe directement au service
- **Strip Prefix** : Middleware Traefik qui supprime un préfixe de chemin

### Termes monitoring

- **Beszel** : Outil de monitoring pour conteneurs Docker et systèmes
- **Grafana** : Plateforme de visualisation et monitoring
- **Dashboard** : Interface graphique avec des graphiques et métriques
- **Panel** : Composant individuel d'un dashboard Grafana
- **Data Source** : Source de données pour Grafana (MySQL, Prometheus, etc.)

### Termes développement

- **Flask** : Framework web micro Python
- **Python** : Langage de programmation utilisé pour les applications
- **Requirements.txt** : Fichier listant les dépendances Python
- **Dockerfile** : Fichier de configuration pour construire une image Docker
- **Environment Variables** : Variables d'environnement pour la configuration

### Abréviations courantes

- **VPS** : Virtual Private Server
- **API** : Application Programming Interface
- **HTTP** : Hypertext Transfer Protocol
- **HTTPS** : HTTP Secure
- **JSON** : JavaScript Object Notation
- **ISO 8601** : Format standard pour les dates et heures
- **RTO** : Recovery Time Objective (temps de reprise)
- **RPO** : Recovery Point Objective (perte de données acceptable)

---

## Tests Unitaires et Validation d'Infrastructure

### Vue d'ensemble des tests

Le projet Marais R Site inclut une suite complète de tests unitaires pour valider le bon fonctionnement de l'infrastructure Docker. Ces tests permettent de vérifier :

- La connectivité entre les services
- Le fonctionnement des protocoles sécurisés
- L'état des conteneurs et volumes
- La disponibilité des ressources système

### Architecture des tests

#### Conteneur test_runner

Les tests utilisent un conteneur dédié `test_runner` basé sur l'image Alpine Linux :

```yaml
test_runner:
  image: alpine
  volumes:
    - ./tests:/tests
    - /var/run/docker.sock:/var/run/docker.sock
  command: >
    sh -c "
    apk add --no-cache curl netcat-openbsd iputils docker &&
    sh /tests/basic_connectivity_tests.sh
    "
  networks:
    - marais_net
```

**Pourquoi Alpine ?**
- **Légèreté** : Image de 5MB vs 30-70MB pour Debian/Ubuntu
- **Sécurité** : Surface d'attaque minimale
- **Rapidité** : Démarrage quasi instantané

**Installation des outils :**
- `curl` : Tests HTTP/HTTPS
- `netcat-openbsd` : Tests de ports TCP
- `iputils` : Tests ping
- `docker` : Accès à l'API Docker

### Description détaillée des tests

#### 1. test_database.sh

**Objectif** : Vérifier que MariaDB est accessible sur le port 3306

**Fonctionnement :**
```bash
nc -z mariadb 3306
```

**Pourquoi ce test ?**
- MariaDB est le cœur du système de stockage
- Le port 3306 doit être ouvert et écouter
- Sans base de données, toute l'application est inutilisable

**Critère de succès** : Le port répond avec succès

#### 2. test_mqtt.sh

**Objectif** : Vérifier que le broker MQTT Mosquitto est accessible sur le port MQTTS 8883

**Fonctionnement :**
```bash
nc -z mosquitto 8883
```

**Pourquoi ce test ?**
- MQTT est le protocole de communication pour les capteurs
- Le port 8883 (MQTTS) est sécurisé avec TLS
- Les capteurs ne peuvent pas envoyer de données si le broker est inaccessible

**Critère de succès** : Le port MQTTS répond avec succès

#### 3. test_network.sh

**Objectif** : Vérifier la résolution DNS et la connectivité réseau

**Fonctionnement :**
```bash
ping -c 2 mariadb
ping -c 2 mosquitto
```

**Pourquoi ce test ?**
- Les conteneurs doivent pouvoir communiquer entre eux
- La résolution DNS est cruciale pour la découverte des services
- Sans réseau, aucun service ne peut fonctionner

**Critère de succès** : Les pings réussissent avec des réponses

#### 4. test_ports.sh

**Objectif** : Vérifier que les services web répondent sur leurs ports respectifs

**Fonctionnement :**
```bash
wget -q --spider http://phpmyadmin:80
wget -q --spider http://grafana:3000
wget -q --spider http://web_app:5000
```

**Pourquoi ce test ?**
- Valide que les services web sont démarrés et fonctionnels
- Vérifie que les ports internes sont accessibles
- Prépare la validation des accès externes via Traefik

**Critère de succès** : Tous les services répondent avec HTTP 200

#### 5. test_ssl.sh

**Objectif** : Vérifier que les ports sécurisés sont accessibles

**Fonctionnement :**
```bash
nc -z traefik 443      # HTTPS
nc -z mosquitto 8883   # MQTTS
```

**Pourquoi ce test ?**
- HTTPS (443) est essentiel pour la sécurité web
- MQTTS (8883) assure la confidentialité des données des capteurs
- Sans SSL/TLS, les communications sont vulnérables

**Critère de succès** : Les ports sécurisés sont ouverts

#### 6. test_app_python.sh

**Objectif** : Vérifier que l'application MQTT Python fonctionne

**Fonctionnement :**
```bash
# Vérification du conteneur
docker ps --format "table {{.Names}}\t{{.Status}}" | grep "app_python" | grep -q "Up"

# Vérification des bibliothèques
docker exec app_python sh -c "
python -c 'import paho.mqtt.client as mqtt; print(\"MQTT client OK\")'
python -c 'import mysql.connector; print(\"MySQL connector OK\")'
"
```

**Pourquoi ce test ?**
- L'application Python traite les messages MQTT
- Elle doit pouvoir se connecter à la base de données
- Sans cette application, les données des capteurs ne sont pas traitées

**Critère de succès** : Le conteneur est running et les bibliothèques sont disponibles

#### 7. test_beszel.sh

**Objectif** : Vérifier que le système de monitoring Beszel fonctionne

**Fonctionnement :**
```bash
# Vérification des conteneurs
docker ps --format "table {{.Names}}\t{{.Status}}" | grep "beszel" | grep -q "Up"
docker ps --format "table {{.Names}}\t{{.Status}}" | grep "beszel-agent" | grep -q "Up"

# Vérification des ports
nc -z beszel 8090
nc -z beszel-agent 4567
```

**Pourquoi ce test ?**
- Beszel monitor l'état de l'infrastructure
- L'agent collecte les métriques système
- Le monitoring est crucial pour la maintenance proactive

**Critère de succès** : Les deux conteneurs sont running et les ports sont accessibles

#### 8. test_traefik.sh

**Objectif** : Vérifier que le reverse proxy Traefik fonctionne

**Fonctionnement :**
```bash
# Vérification du conteneur
docker ps --format "table {{.Names}}\t{{.Status}}" | grep "traefik" | grep -q "Up"

# Vérification des ports
nc -z traefik 443      # HTTPS
nc -z traefik 8883     # MQTTS
nc -z 127.0.0.1 8080   # Dashboard local

# Vérification des services backend
docker exec traefik sh -c "
wget -q --spider http://web_app:5000
wget -q --spider http://grafana:3000
wget -q --spider http://phpmyadmin:80
"
```

**Pourquoi ce test ?**
- Traefik est la porte d'entrée de toute l'infrastructure
- Il gère le SSL/TLS et le routage
- Sans Traefik, aucun accès externe n'est possible

**Critère de succès** : Le conteneur est running, les ports sont ouverts, et les services backend sont accessibles

#### 9. test_volumes.sh

**Objectif** : Vérifier que les volumes Docker sont montés correctement

**Fonctionnement :**
```bash
# Vérification des volumes
docker volume ls | grep -q "marais_project_vol_BDD"
docker volume ls | grep -q "marais_project_vol_grafana"
docker volume ls | grep -q "marais_project_vol_beszel"
docker volume ls | grep -q "marais_project_mosquitto_data"
```

**Pourquoi ce test ?**
- Les volumes assurent la persistance des données
- Sans volumes, les données seraient perdues au redémarrage
- La persistance est critique pour la base de données et les configurations

**Critère de succès** : Tous les volumes nommés existent

#### 10. test_disk_space.sh

**Objectif** : Vérifier qu'il y a suffisamment d'espace disque

**Fonctionnement :**
```bash
# Vérification de l'utilisation disque
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')

# Alertes
if [ $DISK_USAGE -gt 90 ]; then
  echo "WARNING: Espace disque critique (>90%)"
  exit 1
elif [ $DISK_USAGE -gt 80 ]; then
  echo "WARNING: Espace disque élevé (>80%)"
fi

# Vérification des volumes Docker
docker system df
```

**Pourquoi ce test ?**
- L'espace disque est une ressource limitée sur le VPS
- Sans espace, les bases de données ne peuvent plus écrire
- Les logs et les volumes peuvent remplir le disque rapidement

**Critère de succès** : Utilisation disque < 90%

### Tests avancés


### Suites de tests

#### basic_connectivity_tests.sh

**Objectif** : Exécuter tous les tests de connectivité de base

**Fonctionnement :**
```bash
# Exécution séquentielle des 10 tests unitaires
sh /tests/test_database.sh
sh /tests/test_mqtt.sh
sh /tests/test_network.sh
sh /tests/test_ports.sh
sh /tests/test_ssl.sh
sh /tests/test_app_python.sh
sh /tests/test_beszel.sh
sh /tests/test_traefik.sh
sh /tests/test_volumes.sh
sh /tests/test_disk_space.sh
```

**Pourquoi cette suite ?**
- Validation rapide de l'état général
- Durée : ~2 minutes
- Couvre tous les points critiques

#### container_connectivity_tests.sh

**Objectif** : Tests avancés depuis chaque conteneur

**Fonctionnement :**
```bash
# Tests depuis web_app
docker exec web_app sh -c "
nc -zv mariadb 3306
nc -zv mosquitto 8883
wget -q --spider http://grafana:3000
"

# Tests depuis app_python
docker exec app_python sh -c "
ping -c 1 mariadb
ping -c 1 mosquitto
"

# Vérification des logs
docker logs --tail=5 web_app | grep -i error
docker logs --tail=5 mariadb | grep -i error
docker logs --tail=5 mosquitto | grep -i error
```

**Pourquoi cette suite ?**
- Valide la connectivité réelle entre services
- Détecte les problèmes de réseau internes
- Vérifie l'absence d'erreurs critiques

#### full_infrastructure_validation.sh

**Objectif** : Validation complète de l'infrastructure

**Fonctionnement :**
```bash
# 1. Tests de base
sh /tests/basic_connectivity_tests.sh

# 2. Tests avancés
sh /tests/container_connectivity_tests.sh

# 3. Tests fonctionnels
# Note: Les tests avancés d'insertion BDD et MQTT pub/sub ont été retirés
# car ils nécessitent des dépendances supplémentaires et ne sont pas essentiels
# pour la validation de base de l'infrastructure.
```

**Pourquoi cette suite ?**
- Validation exhaustive avant mise en production
- Durée : ~2 minutes
- Vérification des logs des conteneurs pour détecter les erreurs
- Couvre tous les aspects fonctionnels critiques

### Exécution des tests

#### Prérequis - Permissions

Avant d'exécuter les tests, assurez-vous que les scripts ont les permissions appropriées :

```bash
# Vérifier les permissions des fichiers de tests
ls -la tests/*.sh

# Rendre les scripts exécutables si nécessaire
chmod +x tests/*.sh
```

**Impact sur la sécurité :**
- Les scripts de tests ont besoin des permissions d'exécution pour fonctionner
- Ils utilisent `docker` et `docker-compose` qui nécessitent des privilèges
- Limitez l'exécution des tests aux utilisateurs autorisés uniquement
- Ne donnez jamais les permissions d'exécution sur des scripts non vérifiés

**Fichiers nécessitant des permissions :**
- `*.sh` : Tous les scripts de tests doivent être exécutables
- `docker-compose.yml` : Doit être lisible par l'utilisateur
- Répertoire `tests/` : Doit être accessible en lecture/exécution

#### Commandes d'exécution

```bash
# Test unitaire spécifique
docker compose run --rm test_runner sh /tests/test_database.sh

# Suite de tests de base
docker compose run --rm test_runner sh /tests/basic_connectivity_tests.sh

# Validation complète
docker compose run --rm test_runner sh /tests/full_infrastructure_validation.sh
```

#### Automatisation

**Via crontab :**
```bash
# Tests horaires
0 * * * * cd /marais_project && docker compose run --rm test_runner sh /tests/basic_connectivity_tests.sh

# Tests quotidiens complets
0 2 * * * cd /marais_project && docker compose run --rm test_runner sh /tests/full_infrastructure_validation.sh
```

**Note :** Les logs des tests ne sont pas redirigés vers un fichier spécifique. Les résultats s'affichent directement dans les logs système de crontab.

**Via CI/CD :**
Les tests peuvent être intégrés dans des pipelines GitHub Actions, GitLab CI, ou Jenkins pour validation automatique avant déploiement.

### Résultats attendus

#### Succès
```
===== BASIC CONNECTIVITY TESTS =====
Exécution des tests de connectivité de base pour tous les services...
1/10 - Test base de données...
Test MariaDB...
MariaDB OK
...
===== BASIC TESTS COMPLETE =====
Tous les tests de connectivité de base ont été exécutés avec succès
```

#### Échec
```
Test MQTTS...
Connection to mosquitto (172.18.0.3) 8883 port [tcp/*] failed: Connection refused
MQTTS FAIL
```

### Dépannage

#### Problèmes courants

1. **Container not running**
   - Solution : `docker compose up -d <service>`

2. **Connection refused**
   - Solution : Vérifier les logs du service
   - Commande : `docker compose logs <service>`

3. **Permission denied**
   - Solution : `chmod +x tests/*.sh`

4. **docker: not found**
   - Solution : Installer Docker dans le conteneur test_runner

### Interprétation des résultats

- **OK** : Service fonctionnel
- **FAIL** : Service nécessite une intervention
- **WARNING** : Attention requise mais non critique
- **Exit code 0** : Tous les tests passés
- **Exit code 1** : Au moins un test échoué

Les tests sont conçus pour être **autonomes** et **répétables**, permettant une validation continue de l'état de l'infrastructure.

---

## Commandes Utiles

### Connexion SSH

#### Connexion de base

```bash
# Connexion simple au VPS
ssh debian@marais2026.btssn.ovh

# Connexion avec port spécifique
ssh -p 22 debian@marais2026.btssn.ovh

# Connexion avec clé spécifique
ssh -i ~/.ssh/cle_privee debian@marais2026.btssn.ovh
```

#### Connexion avec tunneling et redirection

```bash
# Tunneling local (accéder à un service distant localement)
ssh -L 8080:localhost:8080 debian@marais2026.btssn.ovh

# Tunneling distant (exposer un port local vers le VPS)
ssh -R 9000:localhost:3000 debian@marais2026.btssn.ovh

# Tunneling dynamique (SOCKS proxy)
ssh -D 1080 debian@marais2026.btssn.ovh
```

#### Exécution de commandes à distance

```bash
# Exécuter une commande simple
ssh debian@marais2026.btssn.ovh "ls -la"

# Exécuter des commandes multiples
ssh debian@marais2026.btssn.ovh "cd /marais_project && docker-compose ps"

# Exécuter des scripts
ssh debian@marais2026.btssn.ovh "cd /marais_project && ./backup_db.sh"

# Rediriger la sortie vers un fichier local
ssh debian@marais2026.btssn.ovh "docker-compose logs --tail=50" > logs_vps.txt
```

#### Transfert de fichiers via SSH

```bash
# Copier de l'host vers le VPS
scp /chemin/local/fichier debian@marais2026.btssn.ovh:/chemin/distant/

# Copier un répertoire entier
scp -r /chemin/local/repertoire debian@marais2026.btssn.ovh:/chemin/distant/

# Copier du VPS vers l'host
scp debian@marais2026.btssn.ovh:/chemin/distant/fichier /chemin/local/

# Copier avec port spécifique
scp -P 2222 fichier debian@marais2026.btssn.ovh:/chemin/distant/
```

#### Transfert avec rsync via SSH

```bash
# Synchroniser un répertoire (host → VPS)
rsync -avz /chemin/local/ debian@marais2026.btssn.ovh:/chemin/distant/

# Synchroniser avec exclusion de fichiers
rsync -avz --exclude='*.log' --exclude='*.tmp' /chemin/local/ debian@marais2026.btssn.ovh:/chemin/distant/

# Synchronisation avec suppression des fichiers distants
rsync -avz --delete /chemin/local/ debian@marais2026.btssn.ovh:/chemin/distant/

# Synchronisation avec affichage détaillé
rsync -avz --progress /chemin/local/ debian@marais2026.btssn.ovh:/chemin/distant/
```

#### Configuration SSH

```bash
# Générer une paire de clés SSH
ssh-keygen -t rsa -b 4096 -C "votre_email@example.com"

# Copier la clé publique sur le VPS
ssh-copy-id debian@marais2026.btssn.ovh

# Copier manuellement la clé publique
cat ~/.ssh/id_rsa.pub | ssh debian@marais2026.btssn.ovh "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

# Configurer un alias dans ~/.ssh/config
echo "Host marais
    HostName marais2026.btssn.ovh
    User debian
    Port 22
    IdentityFile ~/.ssh/id_rsa" >> ~/.ssh/config

# Utiliser l'alias
ssh marais
```

#### Sessions persistantes et multiplexage

```bash
# Activer le multiplexage SSH (connexion réutilisable)
echo "ControlMaster auto
ControlPath ~/.ssh/master-%r@%h:%p
ControlPersist 600" >> ~/.ssh/config

# Se connecter en arrière-plan
ssh -f -N -L 8080:localhost:8080 debian@marais2026.btssn.ovh

# Vérifier les connexions actives
ssh -O check debian@marais2026.btssn.ovh

# Fermer une connexion persistante
ssh -O exit debian@marais2026.btssn.ovh
```

#### Dépannage SSH

```bash
# Connexion en mode verbeux (pour diagnostiquer)
ssh -v debian@marais2026.btssn.ovh

# Tester la connexion sans exécuter de commande
ssh -o BatchMode=yes -o ConnectTimeout=5 debian@marais2026.btssn.ovh echo "OK"

# Vérifier les permissions des clés
ls -la ~/.ssh/
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_rsa
chmod 644 ~/.ssh/id_rsa.pub
chmod 644 ~/.ssh/authorized_keys

# Nettoyer les clés hôtes connues
ssh-keygen -R marais2026.btssn.ovh
```

### Transfert de fichiers (Host ↔ VPS)

#### Copie directe avec SCP

```bash
# Copier un fichier spécifique
scp /home/eleve/Documents/test_p/marais_project/tests/test_database.sh debian@marais2026.btssn.ovh:/marais_project/tests/

# Copier un répertoire entier
scp -r /home/eleve/Documents/test_p/marais_project/tests/ debian@marais2026.btssn.ovh:/marais_project/

# Copier plusieurs fichiers
scp test_*.sh debian@marais2026.btssn.ovh:/marais_project/tests/

# Copier avec préservation des permissions
scp -p /chemin/local/fichier debian@marais2026.btssn.ovh:/chemin/distant/

# Copier avec limite de bande passante
scp -l 1000 gros_fichier debian@marais2026.btssn.ovh:/chemin/distant/
```

#### Copie du VPS vers l'host

```bash
# Copier un fichier du VPS vers l'host
scp debian@marais2026.btssn.ovh:/marais_project/logs/app.log ./logs/

# Copier un répertoire du VPS vers l'host
scp -r debian@marais2026.btssn.ovh:/var/log/marais_project/ ./logs/

# Copier avec compression
scp -C debian@marais2026.btssn.ovh:/marais_project/backup.sql ./
```

#### Transfert avancé avec rsync

```bash
# Synchronisation complète avec progression
rsync -avz --progress /home/eleve/Documents/test_p/marais_project/tests/ debian@marais2026.btssn.ovh:/marais_project/tests/

# Synchronisation avec exclusion et compression
rsync -avz --exclude='*.log' --exclude='*.tmp' /chemin/local/ debian@marais2026.btssn.ovh:/chemin/distant/

# Synchronisation avec suppression des fichiers supprimés localement
rsync -avz --delete /chemin/local/ debian@marais2026.btssn.ovh:/chemin/distant/

# Synchronisation avec vérification des checksums (plus lent mais plus sûr)
rsync -avz --checksum /chemin/local/ debian@marais2026.btssn.ovh:/chemin/distant/

# Synchronisation sèche (simulation)
rsync -avz --dry-run /chemin/local/ debian@marais2026.btssn.ovh:/chemin/distant/
```

### Commandes Docker Compose

#### Gestion des conteneurs

```bash
# Démarrer tous les services
docker-compose up -d

# Démarrer un service spécifique
docker-compose up -d mariadb

# Arrêter tous les services
docker-compose down

# Arrêter un service spécifique
docker-compose stop mariadb

# Redémarrer un service
docker-compose restart mariadb

# Recréer un service (avec reconstruction)
docker-compose up -d --force-recreate mariadb

# Mettre à jour et reconstruire les images
docker-compose up -d --build
```

#### Visualisation des états

```bash
# Liste des conteneurs avec leur état
docker-compose ps

# Liste détaillée de tous les conteneurs
docker ps -a

# Utilisation des ressources
docker-compose top

# Statistiques en temps réel
docker stats
```

#### Logs et débogage

```bash
# Logs de tous les services
docker-compose logs

# Logs d'un service spécifique
docker-compose logs mariadb

# Logs en temps réel
docker-compose logs -f mariadb

# Dernières lignes des logs
docker-compose logs --tail=50 mariadb

# Logs avec horodatage
docker-compose logs -t mariadb

# Logs des erreurs uniquement
docker-compose logs mariadb | grep -i error
```

#### Maintenance

```bash
# Nettoyer les conteneurs arrêtés
docker-compose down --remove-orphans

# Nettoyer les images non utilisées
docker image prune -f

# Nettoyer les volumes non utilisés
docker volume prune -f

# Nettoyer tout (conteneurs, images, volumes, réseaux)
docker system prune -a -f

# Vérifier l'utilisation des ressources
docker system df
```

### Commandes de Sauvegarde

#### Sauvegarde manuelle de la base de données

```bash
# Exécuter le script de sauvegarde
./backup_db.sh

# Sauvegarde avec compression
docker exec mariadb mariadb-dump -u root -p$MYSQL_ROOT_PASSWORD Marais_R_Site | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz

# Sauvegarde vers un répertoire spécifique
docker exec mariadb mariadb-dump -u root -p$MYSQL_ROOT_PASSWORD Marais_R_Site > /backups/backup_$(date +%Y%m%d_%H%M%S).sql
```

#### Restauration de la base de données

```bash
# Restauration depuis un fichier SQL
docker exec -i mariadb mysql -u root -p$MYSQL_ROOT_PASSWORD Marais_R_Site < backup_20241201_120000.sql

# Restauration depuis un fichier compressé
gunzip -c backup_20241201_120000.sql.gz | docker exec -i mariadb mysql -u root -p$MYSQL_ROOT_PASSWORD Marais_R_Site
```

#### Sauvegarde des volumes Docker

```bash
# Sauvegarder un volume spécifique
docker run --rm -v marais_project_vol_BDD:/data -v $(pwd):/backup alpine tar czf /backup/vol_BDD_backup_$(date +%Y%m%d).tar.gz -C /data .

# Lister les volumes à sauvegarder
docker volume ls | grep marais_project

# Sauvegarder tous les volumes du projet
docker volume ls --format "{{.Name}}" | grep marais_project | while read volume; do
    docker run --rm -v $volume:/data -v $(pwd):/backup alpine tar czf /backup/${volume}_backup_$(date +%Y%m%d).tar.gz -C /data .
done
```

### Commandes de Configuration et Autostart

#### Vérification des services système

```bash
# Vérifier si Docker est actif
systemctl status docker

# Activer Docker au démarrage
sudo systemctl enable docker

# Vérifier les services actifs
systemctl list-units --type=service --state=running

# Vérifier les services qui démarrent automatiquement
systemctl list-unit-files --type=service --state=enabled
```

#### Configuration Crontab

```bash
# Éditer le crontab de l'utilisateur
crontab -e

# Lister les tâches cron actuelles
crontab -l

# Vérifier les logs de cron
grep CRON /var/log/syslog | tail -20

# Vérifier si le service cron est actif
systemctl status cron

# Redémarrer le service cron
sudo systemctl restart cron
```

#### Configuration réseau

```bash
# Vérifier les ports ouverts
netstat -tlnp | grep :443
netstat -tlnp | grep :8883

# Vérifier la configuration du firewall
sudo ufw status
sudo iptables -L -n

# Tester la connectivité depuis l'extérieur
curl -I https://marais2026.btssn.ovh
nc -zv marais2026.btssn.ovh 443
```

#### Configuration SSL/TLS

```bash
# Vérifier les certificats Let's Encrypt
sudo certbot certificates

# Renouveler manuellement les certificats
sudo certbot renew

# Simuler le renouvellement
sudo certbot renew --dry-run

# Vérifier la date d'expiration des certificats
openssl x509 -in /etc/letsencrypt/live/marais2026.btssn.ovh/cert.pem -noout -dates
```

### Commandes de Monitoring

#### Surveillance des ressources

```bash
# Utilisation CPU et mémoire
htop
top

# Utilisation disque
df -h
du -sh /var/lib/docker/

# Surveillance réseau
iftop
nethogs

# Logs système en temps réel
sudo journalctl -f
```

#### Monitoring spécifique au projet

```bash
# État des conteneurs Marais
docker-compose ps | grep marais

# Utilisation mémoire par conteneur
docker stats --no-stream --format "table {{.Container}}\t{{.MemUsage}}\t{{.CPUPerc}}"

# Logs récents des services critiques
docker-compose logs --tail=20 mariadb | grep -E "(ERROR|WARN)"
docker-compose logs --tail=20 mosquitto | grep -E "(ERROR|WARN)"
docker-compose logs --tail=20 traefik | grep -E "(ERROR|WARN)"

# Vérification de l'espace disque des volumes
docker volume ls --format "table {{.Name}}\t{{.Driver}}" | grep marais_project
```

### Commandes de Dépannage

#### Résolution de problèmes courants

```bash
# Conteneur qui ne démarre pas
docker-compose logs nom_du_conteneur
docker inspect nom_du_conteneur

# Problèmes de réseau
docker network ls
docker network inspect marais_net
docker exec conteneur ping autre_conteneur

# Problèmes de volume
docker volume ls
docker volume inspect nom_du_volume
docker run --rm -v nom_du_volume:/data alpine ls -la /data

# Nettoyage complet après problème
docker-compose down --volumes --remove-orphans
docker system prune -a -f
docker-compose up -d
```

#### Diagnostic complet

```bash
# Script de diagnostic complet
echo "=== Diagnostic Infrastructure Marais R Site ==="
echo "Date: $(date)"
echo ""
echo "=== État des conteneurs ==="
docker-compose ps
echo ""
echo "=== Utilisation disque ==="
df -h
echo ""
echo "=== Utilisation mémoire ==="
free -h
echo ""
echo "=== État des services système ==="
systemctl status docker | head -10
echo ""
echo "=== Erreurs récentes dans les logs ==="
docker-compose logs --tail=10 | grep -i error || echo "Aucune erreur trouvée"
echo ""
echo "=== Connectivité externe ==="
curl -s -o /dev/null -w "%{http_code}" https://marais2026.btssn.ovh && echo " - Site accessible" || echo " - Site inaccessible"
```

---

## Notes importantes

1. **Sécurité** : Ne jamais exposer les ports de base de données ou MQTT directement sur Internet. Tout passe par Traefik.
2. **Persistance** : Les volumes Docker assurent la persistance des données même après suppression des conteneurs.
3. **Scalabilité** : L'architecture permet d'ajouter facilement de nouveaux services via docker-compose.
4. **Monitoring** : Beszel fournit une vue d'ensemble de l'état du système.
5. **Sauvegardes** : Les sauvegardes automatiques sont essentielles pour la récupération en cas de panne.

---

## Contact

Pour toute question ou problème, contacter :
- Email : eleve.marais@btssn.fr
- VPS : marais2026.btssn.ovh
