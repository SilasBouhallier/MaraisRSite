# Système de Surveillance des Marais

Application web de surveillance pour le projet Marais.

## Installation

### 1. Créer l'environnement virtuel
```bash
python3 -m venv venv
```

### 2. Activer l'environnement virtuel
```bash
source venv/bin/activate  # Linux/macOS
# ou
venv\Scripts\activate     # Windows
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configurer la base de données
- Créer la base de données `marais_surveillance` dans MySQL
- Créer l'utilisateur `web_user` avec les permissions nécessaires
- Modifier le fichier `config.env` si nécessaire

### 5. Démarrer l'application
```bash
python app.py
```

L'application sera accessible sur http://localhost:5000

## Structure du projet

- `app.py` - Application Flask principale
- `database_manager.py` - Gestionnaire de base de données
- `templates/` - Templates HTML
- `config.env` - Configuration de l'environnement
- `requirements.txt` - Dépendances Python

## Fonctionnalités

- Visualisation des mesures
- Gestion des emplacements
- Administration des sondes
- Export des données
- API REST
