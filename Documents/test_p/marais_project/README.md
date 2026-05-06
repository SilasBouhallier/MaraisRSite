# Marais R Site

Projet de surveillance environnementale déployé sur VPS via Docker Compose.

## 🌟 Description

Application complète de collecte et visualisation de données environnementales avec architecture microservices.

## 🏗️ Architecture

- **10 conteneurs Docker** orchestrés via docker-compose
- **Reverse Proxy** : Traefik avec SSL automatique (Let's Encrypt)
- **Base de données** : MariaDB
- **Broker MQTT** : Mosquitto sécurisé (MQTTS)
- **Visualisation** : Grafana
- **Interface web** : Flask (web_app)
- **Collecte** : Python MQTT (app_python)
- **Monitoring** : Beszel
- **Admin BDD** : phpMyAdmin

## 🚀 Services

- Web App : `https://marais2026.btssn.ovh/`
- Grafana : `https://marais2026.btssn.ovh/grafana/`
- phpMyAdmin : `https://marais2026.btssn.ovh/phpmyadmin/`
- Beszel : `https://marais2026.btssn.ovh/beszel/`
- MQTT : `mqtts://marais2026.btssn.ovh:8883`

## 🔧 Technologies

- Docker & Docker Compose
- Traefik v3.0
- MariaDB 10.11
- Python (Flask, paho-mqtt)
- Grafana
- Mosquitto MQTT
- Beszel

## 📁 Structure

```
marais_project/
├── docker-compose.yml       # Orchestration des services
├── DOCUMENTATION_PROJET.md  # Documentation détaillée
├── app_python/              # Application MQTT (collecte → BDD)
├── web_app/                 # Application Flask (interface utilisateur)
├── traefik/                 # Configuration Traefik
├── mosquitto/               # Configuration MQTT
├── tests/                   # Tests de connectivité
└── backup_db.sh             # Script de sauvegarde
```

## 🔐 Sécurité

- Certificats SSL automatiques
- MQTT chiffré avec TLS
- Isolation réseau via Docker bridge
- Authentification multi-niveaux

## 📖 Documentation

Voir [DOCUMENTATION_PROJET.md](DOCUMENTATION_PROJET.md) pour la documentation complète.

## 🏷️ Version

Version actuelle : v3
