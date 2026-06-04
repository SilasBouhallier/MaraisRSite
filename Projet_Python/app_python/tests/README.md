# Tests Unitaires - Marais R Site

Ce dossier contient les tests unitaires pour l'application Marais R Site.

## Structure des tests

Chaque fichier de test correspond à un module de l'application :

- `test_traitement_donnees.py` - Tests pour le module `traitement_donnees.py`
- `test_sql.py` - Tests pour le module `sql.py` (DatabaseManager)
- `test_controleur.py` - Tests pour le module `controleur.py` (ControleurMQTT)
- `test_maraisRSenseData.py` - Tests pour le module `maraisRSenseData.py` (MaraisRSenseData)
- `test_envoie_seuils.py` - Tests pour le module `envoie_seuils.py` (EnvoiSeuils)
- `test_alarmes_mqtt.py` - Tests pour le module `alarmes_mqtt.py` (AlarmesMQTT)
- `test_application.py` - Tests pour le module `application.py` (Application)

## Lancer les tests

### Lancer un test spécifique

Chaque test peut être lancé indépendamment depuis le dossier `tests` :

```bash
cd /home/eleve/Documents/Projet/Projet_Python/app_python/tests

# Test pour traitement_donnees
python test_traitement_donnees.py

# Test pour sql
python test_sql.py

# Test pour controleur
python test_controleur.py

# Test pour maraisRSenseData
python test_maraisRSenseData.py

# Test pour envoie_seuils
python test_envoie_seuils.py

# Test pour alarmes_mqtt
python test_alarmes_mqtt.py

# Test pour application
python test_application.py
```

### Lancer tous les tests

Pour lancer tous les tests en une fois :

```bash
cd /home/eleve/Documents/Projet/Projet_Python/app_python/tests
python -m unittest discover -v
```

## Dépendances

Les tests utilisent les modules suivants :
- `unittest` (module standard Python)
- `unittest.mock` (module standard Python pour les mocks)

## Notes

- Les tests pour `sql.py` nécessitent une base de données MariaDB configurée ou utilisent des mocks
- Les tests pour les modules MQTT utilisent des mocks pour simuler le broker MQTT
- Chaque test est conçu pour être indépendant et ne pas dépendre des autres tests
