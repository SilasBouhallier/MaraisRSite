# Documentation Technique - Point de Vue Développeur

## Architecture du Code

### Structure des Modules

L'application Python est organisée selon une architecture modulaire avec une séparation claire des responsabilités :

```
app_python/
├── main.py                    # Point d'entrée, gestion des signaux
└── utils/
    ├── application.py         # Orchestrateur principal
    ├── maraisRSenseData.py    # Client MQTT subscriber
    ├── envoie_seuils.py       # Service de publication seuils
    ├── controleur.py          # Traitement messages MQTT
    ├── sql.py                 # ORM et gestion BDD
    ├── traitement_donnees.py  # Parsing JSON et validation
    └── requirements.txt       # Dépendances Python
```

### Flux d'Exécution

1. **Initialisation** (`main.py` → `application.py`)
   - Chargement variables environnement
   - Parsing fichier configuration avec substitution `${VAR}`
   - Initialisation des modules dans l'ordre dépendant

2. **Démarrage** (`application.start()`)
   - Lancement du service d'envoi des seuils (thread)
   - Démarrage du client MQTT (bloquant)

3. **Traitement Message MQTT**
   ```
   MaraisRSenseData.on_message() 
   → ControleurMQTT.traiter() 
   → TraitementDonnees.extraire_*() 
   → DatabaseManager.ajouter_mesure_automatique()
   ```

## Classes et Interfaces

### Application (utils/application.py)

**Responsabilité** : Orchestrateur principal, configuration et cycle de vie

```python
class Application:
    def __init__(self, fichier_config: str)
    def start(self) -> None
    def stop(self) -> None
    def _substituer_env(self, value: str) -> str
    def _get_config(self, section: str) -> dict
```

**Points clés pour développeurs** :
- Gère la substitution des variables `${VAR}` depuis l'environnement
- Initialise les modules dans le bon ordre (dépendances)
- Gère les signaux SIGINT/SIGTERM pour arrêt propre

### MaraisRSenseData (utils/maraisRSenseData.py)

**Responsabilité** : Client MQTT, réception des messages des sondes

```python
class MaraisRSenseData:
    def __init__(self, config_mqtt: dict, controleur: ControleurMQTT)
    def start(self) -> None
    def stop(self) -> None
    def on_message(self, client, userdata, message) -> None
    def _setup_tls(self) -> None
```

**Configuration TLS** :
```python
if self.port == 8883:
    self.client.tls_set(
        ca_certs="mosquitto/config/ca.crt",
        certfile="mosquitto/config/server.crt", 
        keyfile="mosquitto/config/server.key"
    )
```

### ControleurMQTT (utils/controleur.py)

**Responsabilité** : Logique métier de traitement des messages

```python
class ControleurMQTT:
    def __init__(self, config_mqtt: dict, config_bdd: dict)
    def traiter(self, topic: str, payload: bytes) -> None
    def _verifier_format_message(self, payload: dict) -> bool
```

### TraitementDonnees (utils/traitement_donnees.py)

**Responsabilité** : Parsing JSON, extraction MAC, validation données

```python
class TraitementDonnees:
    @staticmethod
    def extraire_mac(topic: str) -> str
    @staticmethod
    def extraire_donnees(payload: dict) -> list
    @staticmethod
    def valider_mesure(mesure: dict) -> bool
```

**Format attendu** :
```json
{
  "timestamp": "2025-01-01 12:00:00",
  "mesure": [{
    "CO2": 450,
    "Température": 22.5,
    "Humidité": 45
  }]
}
```

### DatabaseManager (utils/sql.py)

**Responsabilité** : Abstraction BDD, connexion, transactions

```python
class DatabaseManager:
    def __init__(self, config_bdd: dict = None)
    def connecter(self) -> None
    def ajouter_mesure_automatique(self, mac: str, mesures: list) -> None
    def get_seuils(self) -> dict
```

**Priorité de configuration** :
1. Config passée en paramètre
2. Variables d'environnement Docker
3. Valeurs par défaut

### EnvoiSeuils (utils/envoie_seuils.py)

**Responsabilité** : Service de synchronisation des seuils vers les sondes

```python
class EnvoiSeuils:
    def __init__(self, config_bdd: dict, config_mqtt: dict)
    def demarrer(self) -> None
    def arreter(self) -> None
    def _recuperer_seuils_bdd(self) -> dict
    def _comparer_seuils(self, seuils_bdd: dict) -> bool
```

**Thread de synchronisation** :
```python
def _thread_synchronisation(self):
    while self._actif:
        seuils_bdd = self._recuperer_seuils_bdd()
        if self._comparer_seuils(seuils_bdd):
            self._envoyer_seuils_mqtt(seuils_bdd)
        time.sleep(60)  # Synchronisation toutes les 60s
```

## Configuration

### Fichier configuration.cfg

```ini
[MQTT]
broker = ${MQTT_BROKER}
port = ${MQTT_PORT}
username = ${MQTT_USER}
password = ${MQTT_PASSWORD}

[BDD]
host = ${MYSQL_MQTT_HOST}
user = ${MYSQL_MQTT_USER}
password = ${MYSQL_MQTT_PASSWORD}
database = ${MYSQL_MQTT_DATABASE}
```

### Variables d'Environnement

**Développement local** :
```bash
MQTT_BROKER=localhost
MQTT_PORT=8883
MQTT_USER=marais2026
MQTT_PASSWORD=hyrome49#
MYSQL_MQTT_HOST=localhost
MYSQL_MQTT_USER=mqtt_user
MYSQL_MQTT_PASSWORD=mqtt_password_hyrome49#
MYSQL_MQTT_DATABASE=Marais_R_Site
```

**Production Docker** :
```bash
MQTT_BROKER=mosquitto
MYSQL_MQTT_HOST=mariadb
```

## Développement Local

### Installation

```bash
# Installation dépendances
pip install -r utils/requirements.txt

# Configuration environnement
cp .env.example .env
# Éditer .env avec les bonnes valeurs

# Démarrage services requis
docker compose up -d mariadb mosquitto
```

### Exécution

```bash
# Lancement application
cd app_python
python main.py

# Avec logging debug
PYTHONPATH=. python -c "
import logging
logging.basicConfig(level=logging.DEBUG)
from main import main
main()
"
```

### Tests

```bash
# Tests unitaires
cd app_python
python -m pytest tests/ -v

# Test spécifique
python -m pytest tests/test_application.py::test_init -v

# Coverage
python -m pytest --cov=utils tests/
```

## Débogage

### Logging

**Niveaux de logging** :
```python
logging.basicConfig(level=logging.INFO)  # Production
logging.basicConfig(level=logging.DEBUG)  # Développement
```

**Logs par module** :
```python
logger = logging.getLogger(__name__)
logger.info("Message informatif")
logger.error("Message erreur")
logger.debug("Message debug")
```

### Erreurs Communes

**Connection refused MQTT** :
```python
# Vérifier broker et port
echo "Broker: ${MQTT_BROKER}, Port: ${MQTT_PORT}"
docker compose ps mosquitto
```

**Variable non substituée** :
```python
# Debug substitution
def _substituer_env(self, value):
    print(f"Avant: {value}")
    result = super()._substituer_env(value)
    print(f"Après: {result}")
    return result
```

### Points d'Arrêt (Debug)

```python
import pdb; pdb.set_trace()  # Breakpoint manuel

# Ou avec ipdb (plus convivial)
import ipdb; ipdb.set_trace()
```

## Extension du Code

### Ajouter un Nouveau Capteur

1. **Mettre à jour `traitement_donnees.py`** :
```python
TYPES_MESURES_VALIDES = [
    "CO2", "Température", "Humidité", 
    "PM 2.5", "PM 10", "TVOC",
    "NOUVEAU_CAPTEUR"  # Ajouter ici
]
```

2. **Mettre à jour la base de données** :
```sql
INSERT INTO type_info_mesure (nom_type_mesure, unite_mesure, 
    valeur_alerte_seuil, valeur_danger_seuil)
VALUES ('NOUVEAU_CAPTEUR', 'unité', 100, 200);
```

### Ajouter un Nouveau Topic MQTT

1. **Modifier `MaraisRSenseData.on_message()`** :
```python
def on_message(self, client, userdata, message):
    topic = message.topic.decode()
    
    if topic.startswith("marais/sondes/"):
        self.controleur.traiter(topic, message.payload)
    elif topic.startswith("marais/nouveau_topic/"):
        self._traiter_nouveau_topic(topic, message.payload)
```

### Personnaliser la Logique de Traitement

**Surcharge de `ControleurMQTT.traiter()`** :
```python
def traiter(self, topic: str, payload: bytes):
    try:
        # Traitement personnalisé
        if self._est_message_critique(topic, payload):
            self._envoyer_alerte_urgent(topic, payload)
        
        # Traitement standard
        super().traiter(topic, payload)
        
    except Exception as e:
        self.logger.error(f"Erreur traitement: {e}")
```

## Performance et Optimisation

### Connexions BDD

**Pooling de connexions** :
```python
# Dans sql.py
from mysql.connector import pooling

connection_pool = pooling.MySQLConnectionPool(
    pool_name="mqtt_pool",
    pool_size=5,
    **config
)
```

### Gestion des Messages MQTT

**Queue asynchrone** :
```python
import queue
import threading

class MessageQueue:
    def __init__(self):
        self.queue = queue.Queue()
        self.worker_thread = threading.Thread(target=self._process_queue)
        self.worker_thread.daemon = True
        self.worker_thread.start()
    
    def _process_queue(self):
        while True:
            topic, payload = self.queue.get()
            self.controleur.traiter(topic, payload)
            self.queue.task_done()
```

### Monitoring

**Métriques de performance** :
```python
import time
from collections import defaultdict

class PerformanceMonitor:
    def __init__(self):
        self.metrics = defaultdict(list)
    
    def time_function(self, func_name):
        def decorator(func):
            def wrapper(*args, **kwargs):
                start = time.time()
                result = func(*args, **kwargs)
                duration = time.time() - start
                self.metrics[func_name].append(duration)
                return result
            return wrapper
        return decorator
```

## Sécurité - Bonnes Pratiques

### Validation des Entrées

```python
def valider_payload_json(payload: bytes) -> dict:
    try:
        data = json.loads(payload.decode())
        # Validation structure
        required_keys = ["timestamp", "mesure"]
        if not all(key in data for key in required_keys):
            raise ValueError("Structure JSON invalide")
        return data
    except json.JSONDecodeError:
        raise ValueError("Payload JSON invalide")
```

### Gestion des Secrets

```python
# Ne jamais logger les secrets
def log_config_sans_secrets(config: dict):
    safe_config = config.copy()
    if 'password' in safe_config:
        safe_config['password'] = '***'
    logger.info(f"Config: {safe_config}")
```

### TLS/SSL

```python
# Validation stricte des certificats
self.client.tls_set(
    ca_certs="ca.crt",
    certfile="client.crt",
    keyfile="client.key",
    cert_reqs=ssl.CERT_REQUIRED,
    tls_version=ssl.PROTOCOL_TLSv1_2
)
```

## Tests - Guide Complet

### Structure des Tests

```
tests/
├── test_application.py        # Tests classe Application
├── test_controleur.py        # Tests logique métier
├── test_maraisRSenseData.py  # Tests client MQTT
├── test_sql.py              # Tests BDD
├── test_traitement_donnees.py # Tests parsing
└── fixtures/                # Données de test
    ├── sample_messages.json
    └── test_database.sql
```

### Mock des Services Externes

```python
import unittest.mock as mock

@mock.patch('utils.sql.mysql.connector.connect')
def test_connexion_bdd(self, mock_connect):
    # Configuration du mock
    mock_connect.return_value = mock.MagicMock()
    
    # Test
    db_manager = DatabaseManager(config_test)
    db_manager.connecter()
    
    # Assertions
    mock_connect.assert_called_once_with(**config_test)
```

### Tests d'Intégration

```python
def test_flux_complet_mqtt_vers_bdd(self):
    # Setup
    with patch('utils.maraisRSenseData.paho.mqtt.client.Client') as mock_client:
        # Simulation message MQTT
        message = MockMessage(
            topic="marais/sondes/A1:B2:C3:D4:E5:F6/",
            payload=b'{"timestamp":"2025-01-01 12:00:00","mesure":[{"CO2":450}]}'
        )
        
        # Exécution
        mqtt_client = MaraisRSenseData(config_mqtt, controleur)
        mqtt_client.on_message(None, None, message)
        
        # Vérification BDD
        cursor = self.db_conn.cursor()
        cursor.execute("SELECT * FROM mesure WHERE valeur_mesure = 450")
        self.assertEqual(len(cursor.fetchall()), 1)
```

## Déploiement - CI/CD

### Dockerfile Optimisé

```dockerfile
FROM python:3.12-slim as builder

WORKDIR /app
COPY utils/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.12-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["python", "main.py"]
```

### GitHub Actions

```yaml
name: CI/CD Pipeline

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      mariadb:
        image: mariadb:10.11
        env:
          MYSQL_ROOT_PASSWORD: test
          MYSQL_DATABASE: test_db
        ports:
          - 3306:3306
      mosquitto:
        image: eclipse-mosquitto:2.0
        ports:
          - 1883:1883
    
    steps:
    - uses: actions/checkout@v3
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.12'
    
    - name: Install dependencies
      run: |
        pip install -r app_python/utils/requirements.txt
        pip install pytest pytest-cov
    
    - name: Run tests
      run: |
        cd app_python
        pytest --cov=utils tests/
    
    - name: Upload coverage
      uses: codecov/codecov-action@v3
```

## Ressources Développeur

### Documentation API

- **Paho MQTT Python** : https://eclipse.dev/paho/clients/python/
- **MySQL Connector** : https://dev.mysql.com/doc/connector-python/en/
- **Python Logging** : https://docs.python.org/3/library/logging.html

### Outils de Développement

```bash
# Formattage code
black app_python/
isort app_python/

# Linting
flake8 app_python/
pylint app_python/

# Type checking
mypy app_python/

# Security scan
bandit -r app_python/
```

### IDE Configuration

**VS Code `.vscode/settings.json`** :
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.pylintEnabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.unittestEnabled": false
}
```

Cette documentation est conçue pour les développeurs qui doivent comprendre, maintenir et étendre l'application Marais R Site.
