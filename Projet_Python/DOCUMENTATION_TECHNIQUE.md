# Documentation Technique - Projet Marais R

## Architecture Globale

Ce projet est un système IoT complet pour la collecte, le stockage et l'analyse de données environnementales (température, CO2, PM2.5, PM10, TVOC, humidité) provenant de sondes connectées via MQTT.

### Composants Principaux

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Sonde IoT     │────▶│  Broker MQTT     │────▶│  Application    │
│   (Capteurs)    │     │  (Mosquitto)     │     │  Python         │
└─────────────────┘     │  Port 8883 (TLS) │     │                 │
                        └──────────────────┘     │  • Traitement   │
                               │                  │  • Stockage BDD │
                               ▼                  │  • Envoi seuils │
                        ┌──────────────────┐     └────────┬────────┘
                        │  Base de données │              │
                        │  MariaDB         │◀─────────────┘
                        │  Port 3306       │
                        └──────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │  Visualisation   │
                        │  • Grafana       │
                        │  • phpMyAdmin    │
                        └──────────────────┘
```

### Services Docker

| Service | Image | Port(s) | Rôle |
|---------|-------|---------|------|
| `mariadb` | mariadb:10.11 | 3306 (localhost uniquement) | Stockage des mesures |
| `phpmyadmin` | phpmyadmin/phpmyadmin | 8080 (localhost) | Administration BDD |
| `grafana` | grafana/grafana | 3000 (localhost) | Visualisation des données |
| `mosquitto` | eclipse-mosquitto:2.0 | 1883 (MQTT), 8883 (MQTT-TLS) | Broker MQTT |
| `app_python` | Build local | - | Traitement des données MQTT |

---

## Commandes Principales

### Démarrage et Gestion des Services

```bash
# Démarrer tous les services
docker compose up -d

# Démarrer un service spécifique
docker compose up -d mosquitto
docker compose up -d app_python

# Arrêter tous les services
docker compose down

# Arrêter un service spécifique
docker compose down app_python

# Rebuild et redémarrer l'application Python
docker compose down app_python
docker compose up -d --build app_python

# Redémarrer un service
docker compose restart mosquitto
docker compose restart app_python
```

### Surveillance et Logs

```bash
# Voir les logs de tous les services
docker compose logs --tail 50

# Voir les logs d'un service spécifique
docker compose logs mosquitto --tail 20
docker compose logs app_python --tail 30
docker compose logs mariadb --tail 20

# Voir les logs en temps réel
docker compose logs -f app_python

# Vérifier le statut des conteneurs
docker compose ps
docker compose ps mosquitto
```

### Tests MQTT

```bash
# Vérifier si le port 8883 est ouvert (depuis le VPS)
sudo ss -tlnp | grep 8883

# Publier un message test en TLS
cd ~/marais_project
mosquitto_pub -h localhost -p 8883 -t "marais/sondes/test/" -m '{"timestamp":"2025-01-01 12:00:00","mesure":[{"CO2":450,"Température":22.5,"Humidité":45}]}' -u marais2026 -P "hyrome49#" --cafile mosquitto/config/ca.crt --insecure

# S'abonner à un topic en TLS
mosquitto_sub -h localhost -p 8883 -t "marais/sondes/#" -u marais2026 -P "hyrome49#" --cafile mosquitto/config/ca.crt --insecure

# Test avec port 1883 (non TLS) - uniquement en local
mosquitto_pub -h localhost -p 1883 -t "marais/sondes/test/" -m '{"timestamp":"2025-01-01 12:00:00","mesure":[{"CO2":450}]}' -u marais2026 -P "hyrome49#"
```

### Gestion des Certificats TLS

```bash
# Générer une CA et des certificats serveur
openssl genrsa -out ca.key 2048
openssl req -new -x509 -days 365 -key ca.key -out ca.crt -subj "/C=FR/ST=State/L=City/O=Organization/CN=CA"

openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr -subj "/C=FR/ST=State/L=City/O=Organization/CN=localhost"
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365

# Permissions des certificats
chmod 644 ca.crt server.crt
chmod 600 server.key
```

### Gestion des Utilisateurs Mosquitto

```bashgit status | grep -E "(env|passwd|key)" || echo "✅ Secrets exclus"
# Créer un fichier de mots de passe
docker compose exec mosquitto mosquitto_passwd -c /mosquitto/config/passwd marais2026

# Ajouter un utilisateur supplémentaire
docker compose exec mosquitto mosquitto_passwd /mosquitto/config/passwd nouvel_utilisateur

# Supprimer un utilisateur
docker compose exec mosquitto mosquitto_passwd -D /mosquitto/config/passwd utilisateur
```

### Base de Données

```bash
# Accéder à MariaDB en ligne de commande
docker compose exec mariadb mariadb -u root -p

# Dump de la base de données
docker compose exec mariadb mysqldump -u root -p Marais_R_Site > backup.sql

# Restaurer une base de données
docker compose exec -i mariadb mariadb -u root -p Marais_R_Site < backup.sql
```

### Exécution Locale (hors Docker)

```bash
# Lancer l'application Python en local
cd /home/eleve/Documents/Project_X(1)/Project_X /app_python
/bin/python3 main.py

# Installer les dépendances
pip install -r utils/requirements.txt
```

---

## Sécurité

### 1. Authentification MQTT

**Configuration Mosquitto** (`mosquitto/config/mosquitto.conf`):

```
# Fichier de mots de passe
password_file /mosquitto/config/passwd

# Interdiction des connexions anonymes
allow_anonymous false
```

**Identifiants**:
- **Utilisateur**: `marais2026`
- **Mot de passe**: `hyrome49#`

### 2. Chiffrement TLS (Port 8883)

**Fichiers de certificats** dans `mosquitto/config/`:
- `ca.crt` : Certificat de l'Autorité de Certification
- `server.crt` : Certificat serveur
- `server.key` : Clé privée serveur

**Configuration**:
```
listener 8883
certfile /mosquitto/config/server.crt
keyfile /mosquitto/config/server.key
cafile /mosquitto/config/ca.crt
allow_anonymous false
```

**Implémentation Python** (`maraisRSenseData.py`, `envoie_seuils.py`):

```python
# TLS si port 8883
if self.port == 8883:
    self.client.tls_set(
        ca_certs=os.path.join(base_dir, "mosquitto/config/ca.crt"),
        certfile=os.path.join(base_dir, "mosquitto/config/server.crt"),
        keyfile=os.path.join(base_dir, "mosquitto/config/server.key")
    )

# Authentification
self.client.username_pw_set(self.username, self.password)
```

### 3. Sécurité de la Base de Données

**Configuration**:
- MariaDB accessible uniquement via `127.0.0.1:3306` (pas exposé publiquement)
- Utilisateur dédié pour l'application MQTT : `mqtt_user`
- Mots de passe stockés dans `.env` et variables d'environnement Docker

**Hiérarchie des connexions** (`sql.py`):

```python
# Priorité 1: Config passée
if config_bdd:
    self.__host = config_bdd.get('host', 'localhost')
    self.__user = config_bdd.get('user')
    self.__password = config_bdd.get('password')

# Priorité 2: Variables d'environnement Docker
elif os.getenv('MYSQL_MQTT_HOST'):
    self.__host = os.getenv('MYSQL_MQTT_HOST')
    self.__user = os.getenv('MYSQL_MQTT_USER')
    self.__password = os.getenv('MYSQL_MQTT_PASSWORD')
```

### 4. Isolation Réseau

**Réseau Docker** (`docker-compose.yml`):

```yaml
networks:
  marais_net:
    driver: bridge
```

Tous les services communiquent via un réseau interne Docker isolé.

**Bind Address** (MariaDB):
```yaml
ports:
  - "127.0.0.1:3306:3306"  # Uniquement localhost
```

**Ports exposés**:
- `1883` : MQTT (non chiffré - à éviter en production)
- `8883` : MQTT-TLS (recommandé)
- `127.0.0.1:8080` : phpMyAdmin (uniquement localhost)
- `127.0.0.1:3000` : Grafana (uniquement localhost)
- `127.0.0.1:3306` : MariaDB (uniquement localhost)

### 5. Gestion des Secrets

**Fichier `.env`** (non versionné):
```
MYSQL_ROOT_PASSWORD=rootpassword
MYSQL_PASSWORD=Marais_R_Site_User/123
MQTT_USER=marais2026
MQTT_PASSWORD=hyrome49#
```

**Substitution des variables** (`application.py`):

```python
# Fonction pour substituer les variables ${VAR} par les valeurs d'environnement
def substituer_env(section):
    result = {}
    for key, value in parser.items(section):
        def remplacer(match):
            var_name = match.group(1)
            env_value = os.getenv(var_name)
            if env_value:
                return env_value
            return match.group(0)
        result[key] = re.sub(r'\$\{([^}]+)\}', remplacer, value)
    return result
```

---

## Structure du Projet

```
/home/eleve/Documents/Project_X(1)/Project_X /
├── .env                          # Variables d'environnement (secrets)
├── docker-compose.yml            # Orchestration Docker
├── mosquitto/
│   └── config/
│       ├── ca.crt               # Certificat CA TLS
│       ├── server.crt           # Certificat serveur
│       ├── server.key           # Clé privée serveur
│       ├── mosquitto.conf       # Configuration Mosquitto
│       └── passwd               # Fichier mots de passe MQTT
└── app_python/
    ├── main.py                  # Point d'entrée
    ├── Dockerfile               # Build image Python
    ├── seuils_cache.json        # Cache local des seuils
    └── utils/
        ├── application.py       # Classe principale Application
        ├── maraisRSenseData.py  # Client MQTT subscriber
        ├── envoie_seuils.py     # Service d'envoi des seuils
        ├── controleur.py        # Traitement des messages MQTT
        ├── sql.py               # Gestion BDD MariaDB
        ├── traitement_donnees.py # Parsing JSON/MAC
        ├── configuration.cfg    # Configuration avec variables
        └── requirements.txt     # Dépendances Python
```

---

## Flux de Données

### 1. Réception des Données MQTT

```
Sonde ──▶ Mosquitto:8883 ──▶ MaraisRSenseData.on_message()
                                    │
                                    ▼
                          ControleurMQTT.traiter()
                                    │
                                    ▼
                          TraitementDonnees.extraire_mac()
                          TraitementDonnees.extraire_donnees()
                                    │
                                    ▼
                          DatabaseManager.ajouter_mesure_automatique()
                                    │
                                    ▼
                                MariaDB
```

### 2. Synchronisation des Seuils

```
EnvoiSeuils ──▶ _recuperer_seuils_bdd() ──▶ MariaDB
                    │
                    ▼
              _comparer_seuils() ◀──▶ seuils_cache.json
                    │
                    ▼ (si changement)
              _envoyer_seuils_mqtt() ──▶ Mosquitto:8883
                    │
                    ▼
              _sauvegarder_cache() ──▶ seuils_cache.json
```

---

## Topics MQTT

| Topic | Direction | Description |
|-------|-----------|-------------|
| `marais/sondes/#` | Subscriber | Données des sondes (MAC, mesures) |
| `marais/alertes/` | Subscriber | Alertes générées |
| `marais/seuils` | Publisher | Configuration des seuils (JSON) |

### Format des Messages

**Données sondes** (`marais/sondes/{MAC}/`):
```json
{
  "timestamp": "2025-01-01 12:00:00",
  "mesure": [{
    "CO2": 450,
    "Température": 22.5,
    "Humidité": 45,
    "PM 2.5": 12,
    "PM 10": 25,
    "TVOC": 350
  }]
}
```

**Seuils** (`marais/seuils`):
```json
{
  "timestamp": "2025-01-01T12:00:00",
  "seuils": {
    "CO2": {
      "valeur_alerte_seuil": 1000,
      "valeur_danger_seuil": 1500
    },
    "Température": {
      "valeur_alerte_seuil": 30,
      "valeur_danger_seuil": 35
    }
  }
}
```

---

## Schéma de Base de Données

### Tables Principales

| Table | Description |
|-------|-------------|
| `mesure` | Stockage des valeurs mesurées |
| `sonde` | Informations sur les sondes |
| `emplacement` | Localisation des sondes |
| `type_info_mesure` | Types de mesures et leurs seuils |
| `alerte` | Niveaux d'alerte (1=Normal, 2=Attention, 3=Danger) |

### Relations

```
sonde (1) ──── (N) emplacement (1) ──── (N) mesure
                                    │
                                    (N) type_info_mesure
                                    │
                                    (1) alerte
```

---

## Dépannage

### Erreur "Connection refused"

```bash
# Vérifier que Mosquitto tourne
docker compose ps mosquitto

# Vérifier le port
docker compose exec mosquitto netstat -tlnp | grep 8883
# ou depuis l'hôte :
sudo ss -tlnp | grep 8883

# Vérifier les logs
docker compose logs mosquitto --tail 20
```

### Erreur "SSLCertVerificationError"

- Le hostname doit correspondre au CN du certificat
- Utiliser `--insecure` pour les tests (pas en production)
- Régénérer les certificats avec le bon CN/SAN

### Erreur "invalid literal for int() with base 10: '${MQTT_PORT}'"

Les variables d'environnement ne sont pas substituées. Vérifier `application.py` et s'assurer que la substitution fonctionne.

### Données non insérées dans la BDD

```bash
# Vérifier les logs
docker compose logs app_python --tail 20

# Vérifier la connexion BDD
docker compose exec mariadb mariadb -u mqtt_user -p -e "SELECT 1"

# Vérifier la structure des tables
docker compose exec mariadb mariadb -u root -p -e "USE Marais_R_Site; SHOW TABLES;"
```

---

## Maintenance

### Mise à jour des Seuils

Modifier les valeurs dans `type_info_mesure` via phpMyAdmin ou SQL :
```sql
UPDATE type_info_mesure 
SET valeur_alerte_seuil = 1200, valeur_danger_seuil = 2000 
WHERE nom_type_mesure = 'CO2';
```

L'application détectera automatiquement le changement et enverra les nouveaux seuils.

### Sauvegarde

```bash
# BDD
docker compose exec mariadb mysqldump -u root -p Marais_R_Site > backup_$(date +%Y%m%d).sql

# Certificats
tar -czf mosquitto_certs_$(date +%Y%m%d).tar.gz mosquitto/config/*.crt mosquitto/config/*.key
```

### Nettoyage

```bash
# Supprimer tous les volumes et données
docker compose down -v

# Supprimer les images non utilisées
docker image prune -a
```

---

## Déploiement Local vs VPS

### Configuration Local (Développement)

**Fichier `.env`** :
```
MQTT_BROKER=localhost
MQTT_PORT=8883
MQTT_USER=marais2026
MQTT_PASSWORD=hyrome49#
```

**Configuration `configuration.cfg`** :
```ini
[MQTT]
broker = localhost
port = 8883
```

**Certificats** : Auto-signés avec `CN=localhost`

### Configuration VPS (Production)

**Fichier `.env`** :
```
MQTT_BROKER=mosquitto
MQTT_PORT=8883
MQTT_USER=marais2026
MQTT_PASSWORD=hyrome49#
```

**Configuration `configuration.cfg`** :
```ini
[MQTT]
broker = mosquitto
port = 8883
```

**Différences clés** :

| Aspect | Local | VPS |
|--------|-------|-----|
| `MQTT_BROKER` | `localhost` | `mosquitto` (nom service Docker) |
| Certificats CN | `localhost` | `marais2026.btssn.ovh` ou `localhost` |
| TLS requis | Optionnel | Obligatoire (port 8883) |
| MariaDB | `127.0.0.1:3306` | `mariadb` (service Docker) |

---

## Onboarding d'une Nouvelle Sonde

### Étape 1 : Configuration Base de Données

```sql
-- 1. Créer la sonde
INSERT INTO sonde (nom_sonde, date_installation_sonde) 
VALUES ('Sonde_Salle_A', NOW());

-- 2. Récupérer l'ID généré
SELECT id_sonde FROM sonde WHERE nom_sonde = 'Sonde_Salle_A';
-- Supposons id_sonde = 5

-- 3. Créer l'emplacement
INSERT INTO emplacement (nom_emplacement, id_sonde) 
VALUES ('Salle A - Bâtiment Principal', 5);

-- 4. Vérifier
SELECT s.nom_sonde, e.nom_emplacement, e.id_emplacement
FROM sonde s 
JOIN emplacement e ON s.id_sonde = e.id_sonde 
WHERE s.nom_sonde = 'Sonde_Salle_A';
```

### Étape 2 : Configuration Sonde Physique

Paramètres MQTT à configurer sur la sonde :

| Paramètre | Valeur |
|-----------|--------|
| Broker | `marais2026.btssn.ovh` (VPS) ou `192.168.x.x` (local) |
| Port | `8883` |
| Username | `marais2026` |
| Password | `hyrome49#` |
| Topic Publish | `marais/sondes/{MAC}/` (ex: `marais/sondes/A1:B2:C3:D4:E5:F6/`) |
| TLS/SSL | Activé |
| CA Certificate | Contenu de `mosquitto/config/ca.crt` |

### Étape 3 : Format du Message

```json
{
  "timestamp": "2025-05-05 10:30:00",
  "mesure": [{
    "CO2": 450,
    "Température": 22.5,
    "Humidité": 48,
    "PM 2.5": 8,
    "PM 10": 15,
    "TVOC": 220
  }]
}
```

### Étape 4 : Test de Connexion

```bash
# Depuis le VPS, simuler la sonde
mosquitto_pub -h localhost -p 8883 -t "marais/sondes/A1:B2:C3:D4:E5:F6/" \
  -m '{"timestamp":"2025-05-05 10:30:00","mesure":[{"CO2":450,"Température":22.5}]}' \
  -u marais2026 -P "hyrome49#" --cafile mosquitto/config/ca.crt --insecure

# Vérifier l'insertion
docker compose exec mariadb mariadb -u mqtt_user -p -e \
  "USE Marais_R_Site; SELECT * FROM mesure ORDER BY date_heure_mesure DESC LIMIT 5;"
```

---

## Matrice des Alertes et Seuils

### Types de Mesures et Seuils Actuels

| Type de Mesure | Unité | Seuil Alerte | Seuil Danger | Action Alerte | Action Danger |
|----------------|-------|--------------|--------------|---------------|---------------|
| CO2 | ppm | 1000 | 1500 | Ventilation accrue | Ventilation urgente |
| Température | °C | 30 | 35 | Contrôle climatisation | Alerting maintenance |
| Humidité | % | 70 | 85 | Déshumidification | Risque moisissure |
| PM 2.5 | µg/m³ | 35 | 55 | Filtre à vérifier | Filtration urgente |
| PM 10 | µg/m³ | 50 | 100 | Surveillance air | Protection respiratoire |
| TVOC | ppb | 500 | 1000 | Aération conseillée | Évacuation recommandée |

### Modification des Seuils

```sql
-- Exemple : Modifier les seuils CO2
UPDATE type_info_mesure 
SET valeur_alerte_seuil = 800, 
    valeur_danger_seuil = 1200 
WHERE nom_type_mesure = 'CO2';

-- Vérification
SELECT nom_type_mesure, valeur_alerte_seuil, valeur_danger_seuil 
FROM type_info_mesure;
```

L'application Python synchronise automatiquement les seuils toutes les 60 secondes.

---

## Scripts de Test

### Script de Simulation de Sonde (Bash)

```bash
#!/bin/bash
# simulate_sonde.sh - Simule l'envoi de données MQTT

BROKER="localhost"
PORT="8883"
USER="marais2026"
PASS="hyrome49#"
TOPIC="marais/sondes/TEST:SONDE:01/"
CAFILE="mosquitto/config/ca.crt"

while true; do
    TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
    CO2=$((400 + RANDOM % 1200))
    TEMP=$((18 + RANDOM % 15))
    HUM=$((30 + RANDOM % 50))
    
    PAYLOAD="{\"timestamp\":\"$TIMESTAMP\",\"mesure\":[{\"CO2\":$CO2,\"Température\":$TEMP,\"Humidité\":$HUM}]}"
    
    mosquitto_pub -h $BROKER -p $PORT -t "$TOPIC" -m "$PAYLOAD" \
        -u $USER -P "$PASS" --cafile $CAFILE --insecure
    
    echo "[$TIMESTAMP] Sent: CO2=$CO2, Temp=$TEMP°C, Hum=$HUM%"
    sleep 10
done
```

### Script de Vérification BDD (Python)

```python
# check_mesures.py - Vérifie les dernières mesures
import mysql.connector
import sys

config = {
    'host': 'localhost',
    'user': 'mqtt_user',
    'password': 'mqtt_password_hyrome49#',
    'database': 'Marais_R_Site'
}

try:
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT m.valeur_mesure, m.date_heure_mesure, 
               t.nom_type_mesure, e.nom_emplacement
        FROM mesure m
        JOIN type_info_mesure t ON m.id_type_mesure = t.id_type_mesure
        JOIN emplacement e ON m.id_emplacement = e.id_emplacement
        ORDER BY m.date_heure_mesure DESC
        LIMIT 10
    """
    
    cursor.execute(query)
    results = cursor.fetchall()
    
    print("Dernières 10 mesures :")
    print("-" * 80)
    for row in results:
        print(f"{row['date_heure_mesure']} | {row['nom_emplacement'][:20]:20} | "
              f"{row['nom_type_mesure'][:12]:12} | {row['valeur_mesure']}")
    
    cursor.close()
    conn.close()
    
except mysql.connector.Error as err:
    print(f"Erreur: {err}")
    sys.exit(1)
```

### Test de Connectivité Complète

```bash
#!/bin/bash
# test_full_chain.sh - Test complet de la chaîne

echo "=== Test 1: Mosquitto ==="
docker compose ps mosquitto

echo -e "\n=== Test 2: Port 8883 ==="
sudo ss -tlnp | grep 8883

echo -e "\n=== Test 3: Envoi MQTT ==="
mosquitto_pub -h localhost -p 8883 -t "marais/sondes/TEST/" \
    -m '{"timestamp":"'$(date '+%Y-%m-%d %H:%M:%S')'","mesure":[{"CO2":999}]}' \
    -u marais2026 -P "hyrome49#" --cafile mosquitto/config/ca.crt --insecure \
    && echo "✅ MQTT OK" || echo "❌ MQTT FAIL"

echo -e "\n=== Test 4: Dernière mesure BDD ==="
sleep 2
docker compose exec mariadb mariadb -u mqtt_user -p"mqtt_password_hyrome49#" -e \
    "USE Marais_R_Site; SELECT * FROM mesure WHERE valeur_mesure = 999 ORDER BY date_heure_mesure DESC LIMIT 1;" \
    && echo "✅ BDD OK" || echo "❌ BDD FAIL"
```

---

## Checklist Mise en Production

### Pré-déploiement

- [ ] Certificats TLS générés avec le bon CN (hostname VPS)
- [ ] Fichier `.env` configuré avec les secrets de production
- [ ] Variables d'environnement Docker vérifiées
- [ ] Fichier `mosquitto/config/passwd` créé avec `marais2026`
- [ ] Firewall configuré (ports 8883, 22 ouverts uniquement)
- [ ] Accès SSH par clé uniquement (pas de password)
- [ ] Backup automatique configuré (BDD + certificats)

### Déploiement

- [ ] `docker compose down` sur l'ancienne version
- [ ] `docker compose up -d` sur la nouvelle version
- [ ] Vérification logs : `docker compose logs --tail 50`
- [ ] Test MQTT avec `mosquitto_pub`
- [ ] Test BDD avec requête SELECT
- [ ] Grafana accessible via tunnel SSH

### Post-déploiement

- [ ] Monitoring activé (Beszel Agent)
- [ ] Alertes configurées (seuils dans BDD)
- [ ] Documentation à jour
- [ ] Procédure de rollback testée

### Sécurité

- [ ] Port 1883 fermé ou non exposé publiquement
- [ ] MariaDB accessible uniquement en localhost
- [ ] phpMyAdmin accessible uniquement en localhost
- [ ] Grafana accessible uniquement en localhost ou avec auth
- [ ] Certificats renouvelés si nécessaire (validité 365 jours)

---

## Références

- **Mosquitto** : https://mosquitto.org/documentation/
- **Paho MQTT Python** : https://eclipse.dev/paho/clients/python/
- **MariaDB** : https://mariadb.com/kb/en/documentation/
- **Docker Compose** : https://docs.docker.com/compose/
- **MQTT Specification** : https://docs.oasis-open.org/mqtt/mqtt/v5.0/mqtt-v5.0.html
