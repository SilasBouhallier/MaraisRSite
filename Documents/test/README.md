# Infrastructure Docker avec Tests Automatisés

## Architecture

```
docker-compose
│
├─ Infrastructure
│   ├─ MariaDB (port 3306)
│   ├─ Mosquitto MQTT (port 1884)
│   ├─ Grafana (port 3000)
│   └─ phpMyAdmin (port 8080)
│
└─ Validation
    └─ test_runner
```

## Services

### Base de données
- **MariaDB**: Base de données principale
- **phpMyAdmin**: Interface d'administration (http://localhost:8080)

### Monitoring
- **Grafana**: Tableaux de bord et monitoring (http://localhost:3000)

### Communication
- **Mosquitto**: Broker MQTT (port 1884)

### Tests
- **test_runner**: Conteneur de validation automatique

## Scripts de test

Les tests sont situés dans le dossier `tests/` :

- `test_database.sh`: Test de connexion à MariaDB
- `test_mqtt.sh`: Test du broker Mosquitto
- `test_network.sh`: Test de résolution DNS et connectivité
- `test_ports.sh`: Test des services web (phpMyAdmin, Grafana)
- `run_all_tests.sh`: Script principal d'exécution

## Utilisation

### Démarrer l'infrastructure avec tests
```bash
docker compose up --build --abort-on-container-exit
```

### Démarrer en arrière-plan
```bash
docker compose up -d
```

### Voir les logs des tests
```bash
docker compose logs test_runner
```

### Arrêter l'infrastructure
```bash
docker compose down
```

## Résultat des tests

En cas de succès, vous devriez voir :
```
===== INFRA TESTS =====
Test MariaDB...
MariaDB OK
Test MQTT...
MQTT OK
Test reseau...
Test phpmyadmin...
phpmyadmin OK
Test grafana...
grafana OK
===== ALL TESTS OK =====
```

## Intégration CI/CD

Pour utiliser cette architecture dans un pipeline CI/CD :

```bash
docker compose up --build --abort-on-container-exit
```

Si un test échoue, la commande retourne un code d'erreur différent de 0, ce qui fait échouer le pipeline.

## Testcontainers

Cette architecture teste l'infrastructure. Pour les tests applicatifs, utilisez Testcontainers dans vos tests unitaires/intégrations pour démarrer des containers temporaires.
