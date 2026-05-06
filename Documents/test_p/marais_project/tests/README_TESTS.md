# Documentation des Tests - Projet Marais R Site

## Table des matières

1. [Vue d'ensemble](#vue-densemble)
2. [Liste des tests disponibles](#liste-des-tests-disponibles)
3. [Exécution des tests](#exécution-des-tests)
4. [Description détaillée des tests](#description-détaillée-des-tests)
5. [Dépannage](#dépannage)
6. [Intégration CI/CD](#intégration-cicd)

---

## Vue d'ensemble

Les tests du projet Marais R Site permettent de valider le bon fonctionnement de l'infrastructure Docker, des services et de leurs interconnexions.

**Objectifs :**
- Vérifier la connectivité entre les services
- Valider le fonctionnement des bases de données
- Tester les protocoles sécurisés (SSL/TLS, MQTTS)
- Surveiller l'état des conteneurs et des volumes
- Détecter les erreurs de configuration

**Emplacement** : `/home/eleve/Documents/test_p/marais_project/tests/`

---

## Liste des tests disponibles

### Tests unitaires

| Fichier | Description | Services testés |
|---------|-------------|-----------------|
| `test_database.sh` | Connectivité MariaDB | MariaDB |
| `test_mqtt.sh` | Connectivité MQTTS | Mosquitto |
| `test_network.sh` | Réseau et DNS | Tous les services |
| `test_ports.sh` | Services web | phpMyAdmin, Grafana, web_app |
| `test_ssl.sh` | SSL/TLS | HTTPS, MQTTS |
| `test_app_python.sh` | Application MQTT | app_python |
| `test_beszel.sh` | Monitoring | Beszel, Beszel Agent |
| `test_traefik.sh` | Reverse Proxy | Traefik |
| `test_volumes.sh` | Volumes Docker | Tous les volumes |
| `test_disk_space.sh` | Espace disque | Système hôte |
| `test_database_insert.sh` | Insertion BDD | MariaDB |
| `test_mqtt_pubsub.sh` | MQTT pub/sub | Mosquitto |

### Suites de tests

| Fichier | Description | Tests inclus |
|---------|-------------|--------------|
| `basic_connectivity_tests.sh` | Tests de connectivité de base | Tous les tests unitaires |
| `container_connectivity_tests.sh` | Tests avancés inter-conteneurs | Connectivité, DNS, logs |
| `full_infrastructure_validation.sh` | Validation complète | Toutes les suites |

---

## Exécution des tests

### Prérequis

- Docker et Docker Compose installés
- Tous les conteneurs en cours d'exécution
- Accès au réseau Docker

### Vérifier l'état des conteneurs

```bash
cd /home/eleve/Documents/test_p/marais_project
docker-compose ps
```

### Exécution des tests unitaires

#### Via le conteneur test_runner (recommandé)

```bash
# Exécuter un test spécifique
docker-compose run --rm test_runner sh /tests/test_database.sh

# Exécuter un autre test
docker-compose run --rm test_runner sh /tests/test_mqtt.sh

# Exécuter tous les tests de base
docker-compose run --rm test_runner sh /tests/basic_connectivity_tests.sh
```

#### Directement sur l'hôte

```bash
cd /home/eleve/Documents/test_p/marais_project/tests

# Exécuter un test spécifique
./test_database.sh

# Exécuter tous les tests de base
./basic_connectivity_tests.sh
```

### Exécution des suites de tests

#### Tests de connectivité de base

```bash
# Via test_runner
docker-compose run --rm test_runner sh /tests/basic_connectivity_tests.sh

# Directement
cd /home/eleve/Documents/test_p/marais_project/tests
./basic_connectivity_tests.sh
```

**Sortie attendue :**
```
===== BASIC CONNECTIVITY TESTS =====
Exécution des tests de connectivité de base pour tous les services...
1/10 - Test base de données...
Test MariaDB...
MariaDB OK
2/10 - Test broker MQTT...
Test MQTTS...
MQTTS OK
...
===== BASIC TESTS COMPLETE =====
Tous les tests de connectivité de base ont été exécutés avec succès
```

#### Tests de connectivité avancés

```bash
# Via test_runner
docker-compose run --rm test_runner sh /tests/container_connectivity_tests.sh

# Directement
cd /home/eleve/Documents/test_p/marais_project/tests
./container_connectivity_tests.sh
```

**Sortie attendue :**
```
===== CONTAINER CONNECTIVITY TESTS =====

1. Tests depuis le conteneur web_app
----------------------------------------
Test connexion MariaDB depuis web_app:
OK
...
===== CONTAINER CONNECTIVITY TESTS COMPLETE =====
```

#### Validation complète

```bash
# Via test_runner
docker-compose run --rm test_runner sh /tests/full_infrastructure_validation.sh

# Directement
cd /home/eleve/Documents/test_p/marais_project/tests
./full_infrastructure_validation.sh
```

**Sortie attendue :**
```
===== INFRASTRUCTURE VALIDATION SUITE =====
Validation complète de l'infrastructure Docker avec tests approfondis...

1. Basic Connectivity Tests...
   Tests de connectivité de base depuis le conteneur test_runner
...

2. Container Connectivity Tests...
   Tests avancés de connectivité depuis chaque conteneur
...

3. Database Insert Test...
   Test d'insertion et lecture dans la base de données
...

4. MQTT Publish/Subscribe Test...
   Test de publication et abonnement MQTT
...

===== VALIDATION COMPLETE =====
L'infrastructure Docker a été entièrement validée
Prête pour la production ou les tests d'intégration
```

### Exécution automatique via Crontab

Pour exécuter les tests automatiquement toutes les heures :

```bash
# Éditer le crontab
crontab -e

# Ajouter la ligne suivante
0 * * * * cd /home/eleve/Documents/test_p/marais_project && docker-compose run --rm test_runner sh /tests/basic_connectivity_tests.sh >> /var/log/marais_tests.log 2>&1
```

Pour exécuter les tests quotidiennement à 2h du matin :

```bash
# Ajouter la ligne suivante
0 2 * * * cd /home/eleve/Documents/test_p/marais_project && docker-compose run --rm test_runner sh /tests/full_infrastructure_validation.sh >> /var/log/marais_tests.log 2>&1
```

---

## Description détaillée des tests

### test_database.sh

**Objectif** : Vérifier que MariaDB est accessible sur le port 3306

**Commande** : `nc -z mariadb 3306`

**Critère de succès** : Le port est ouvert et MariaDB répond

**Utilisation** :
```bash
docker-compose run --rm test_runner sh /tests/test_database.sh
```

### test_mqtt.sh

**Objectif** : Vérifier que Mosquitto est accessible sur le port MQTTS 8883

**Commande** : `nc -z mosquitto 8883`

**Critère de succès** : Le port MQTTS est ouvert

**Utilisation** :
```bash
docker-compose run --rm test_runner sh /tests/test_mqtt.sh
```

### test_network.sh

**Objectif** : Vérifier la résolution DNS et la connectivité réseau

**Commandes** :
- `ping -c 2 mariadb`
- `ping -c 2 mosquitto`

**Critère de succès** : Les pings réussissent

**Utilisation** :
```bash
docker-compose run --rm test_runner sh /tests/test_network.sh
```

### test_ports.sh

**Objectif** : Vérifier que les services web répondent sur leurs ports

**Commandes** :
- `wget -q --spider http://phpmyadmin:80`
- `wget -q --spider http://grafana:3000`
- `wget -q --spider http://web_app:5000`

**Critère de succès** : Tous les services répondent avec HTTP 200

**Utilisation** :
```bash
docker-compose run --rm test_runner sh /tests/test_ports.sh
```

### test_ssl.sh

**Objectif** : Vérifier que les certificats SSL sont valides

**Commandes** :
- `curl -k -I https://marais2026.btssn.ovh/`
- `curl -k -I https://marais2026.btssn.ovh/grafana/`
- `curl -k -I https://marais2026.btssn.ovh/phpmyadmin/`
- `nc -z marais2026.btssn.ovh 8883`

**Critère de succès** : Tous les services HTTPS et MQTTS sont accessibles

**Utilisation** :
```bash
docker-compose run --rm test_runner sh /tests/test_ssl.sh
```

### test_app_python.sh

**Objectif** : Vérifier que l'application MQTT fonctionne

**Vérifications** :
- Conteneur app_python en cours d'exécution
- Bibliothèque MQTT Python disponible
- Bibliothèque MySQL Python disponible

**Utilisation** :
```bash
docker-compose run --rm test_runner sh /tests/test_app_python.sh
```

### test_beszel.sh

**Objectif** : Vérifier que Beszel et son agent fonctionnent

**Vérifications** :
- Conteneur beszel en cours d'exécution
- Port 8090 accessible
- Conteneur beszel-agent en cours d'exécution
- Port 4567 accessible

**Utilisation** :
```bash
docker-compose run --rm test_runner sh /tests/test_beszel.sh
```

### test_traefik.sh

**Objectif** : Vérifier que le reverse proxy fonctionne

**Vérifications** :
- Conteneur traefik en cours d'exécution
- Port 443 (HTTPS) accessible
- Port 8883 (MQTTS) accessible
- Port 8080 (dashboard) accessible
- Services backend accessibles

**Utilisation** :
```bash
docker-compose run --rm test_runner sh /tests/test_traefik.sh
```

### test_volumes.sh

**Objectif** : Vérifier que les volumes Docker sont montés

**Vérifications** :
- vol_BDD existe
- vol_grafana existe
- vol_beszel existe
- mosquitto_data existe

**Utilisation** :
```bash
docker-compose run --rm test_runner sh /tests/test_volumes.sh
```

### test_disk_space.sh

**Objectif** : Vérifier l'espace disque disponible

**Vérifications** :
- Utilisation disque < 90%
- Espace disque des volumes Docker
- Espace disque par conteneur

**Utilisation** :
```bash
docker-compose run --rm test_runner sh /tests/test_disk_space.sh
```

### test_database_insert.sh

**Objectif** : Vérifier l'insertion et la lecture dans la BDD

**Vérifications** :
- Insertion d'une mesure de test
- Lecture de la mesure insérée
- Nettoyage de la mesure de test

**Utilisation** :
```bash
docker-compose run --rm test_runner sh /tests/test_database_insert.sh
```

### test_mqtt_pubsub.sh

**Objectif** : Vérifier la publication et l'abonnement MQTT

**Vérifications** :
- Publication d'un message
- Abonnement et réception du message

**Utilisation** :
```bash
docker-compose run --rm test_runner sh /tests/test_mqtt_pubsub.sh
```

---

## Dépannage

### Erreur : "container not running"

**Cause** : Le conteneur n'est pas démarré

**Solution** :
```bash
docker-compose ps
docker-compose up -d <service_name>
```

### Erreur : "nc: command not found"

**Cause** : netcat n'est pas installé dans le conteneur

**Solution** :
```bash
# Installer netcat dans le conteneur Alpine
docker-compose exec <service_name> apk add --no-cache netcat-openbsd
```

### Erreur : "docker-compose: command not found"

**Cause** : Docker Compose n'est pas installé

**Solution** :
```bash
# Installer Docker Compose
sudo apt install docker-compose
```

### Erreur : "connection refused"

**Cause** : Le service n'est pas accessible

**Solution** :
```bash
# Vérifier les logs du service
docker-compose logs <service_name>

# Redémarrer le service
docker-compose restart <service_name>
```

### Erreur : "permission denied"

**Cause** : Permissions insuffisantes sur les fichiers de test

**Solution** :
```bash
# Rendre les scripts exécutables
chmod +x /home/eleve/Documents/test_p/marais_project/tests/*.sh
```

### Erreur : "network not found"

**Cause** : Le réseau Docker n'existe pas

**Solution** :
```bash
# Recréer le réseau
docker-compose down
docker-compose up -d
```

---

## Intégration CI/CD

### GitHub Actions

Exemple de workflow GitHub Actions pour exécuter les tests :

```yaml
name: Tests Infrastructure

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]
  schedule:
    - cron: '0 2 * * *' # Tous les jours à 2h

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Start Docker containers
        run: |
          docker-compose up -d
          
      - name: Wait for services to be ready
        run: |
          sleep 30
          
      - name: Run basic connectivity tests
        run: |
          docker-compose run --rm test_runner sh /tests/basic_connectivity_tests.sh
          
      - name: Run full infrastructure validation
        run: |
          docker-compose run --rm test_runner sh /tests/full_infrastructure_validation.sh
          
      - name: Stop Docker containers
        if: always()
        run: |
          docker-compose down
```

### GitLab CI

Exemple de pipeline GitLab CI :

```yaml
stages:
  - test

test_infrastructure:
  stage: test
  script:
    - docker-compose up -d
    - sleep 30
    - docker-compose run --rm test_runner sh /tests/basic_connectivity_tests.sh
    - docker-compose run --rm test_runner sh /tests/full_infrastructure_validation.sh
  after_script:
    - docker-compose down
  only:
    - main
    - merge_requests
```

### Jenkins Pipeline

Exemple de pipeline Jenkins :

```groovy
pipeline {
    agent any
    stages {
        stage('Start Services') {
            steps {
                sh 'docker-compose up -d'
                sh 'sleep 30'
            }
        }
        stage('Run Tests') {
            steps {
                sh 'docker-compose run --rm test_runner sh /tests/basic_connectivity_tests.sh'
                sh 'docker-compose run --rm test_runner sh /tests/full_infrastructure_validation.sh'
            }
        }
        stage('Stop Services') {
            steps {
                sh 'docker-compose down'
            }
        }
    }
    post {
        always {
            sh 'docker-compose down'
        }
    }
}
```

---

## Bonnes pratiques

1. **Exécuter les tests avant tout déploiement**
2. **Surveiller les résultats des tests dans les logs**
3. **Garder les tests à jour avec les modifications de l'infrastructure**
4. **Utiliser les tests pour diagnostiquer les problèmes**
5. **Automatiser l'exécution des tests via crontab ou CI/CD**

---

## Contact

Pour toute question sur les tests, contacter :
- Email : eleve.marais@btssn.fr
- VPS : marais2026.btssn.ovh
