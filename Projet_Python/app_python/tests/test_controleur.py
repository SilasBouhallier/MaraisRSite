"""
Test unitaire pour le module controleur.py

Ce test peut être lancé indépendamment avec :
    python test_controleur.py
"""

import sys
import os
from unittest.mock import Mock, patch

# Ajout du chemin parent pour pouvoir importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.controleur import ControleurMQTT


def test_init_controleur():
    """Test l'initialisation du contrôleur MQTT."""
    config_mqtt = {
        'broker': 'localhost',
        'port': '1883',
        'topics_sonde': 'marais/sondes/#'
    }
    config_bdd = {
        'host': 'localhost',
        'port': '3306',
        'database': 'Marais_R_Site',
        'user': 'test_user',
        'password': 'test_password'
    }
    
    with patch('utils.controleur.DatabaseManager') as mock_db:
        controleur = ControleurMQTT(config_mqtt, config_bdd)
        assert controleur is not None
        assert controleur.config_mqtt == config_mqtt
        assert controleur.config_bdd == config_bdd
        print("✓ test_init_controleur passé")


def test_traiter_message_complet():
    """Test le traitement d'un message MQTT complet."""
    config_mqtt = {'broker': 'localhost', 'port': '1883'}
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    
    with patch('utils.controleur.DatabaseManager') as mock_db_class:
        mock_db = Mock()
        mock_db_class.return_value = mock_db
        mock_db.ajouter_mesure_automatique.return_value = True
        
        controleur = ControleurMQTT(config_mqtt, config_bdd)
        
        topic = "marais/sondes/00:11:22:33:44:55"
        message = '{"timestamp": "2024-01-01T12:00:00", "mesure": {"CO2": 450}}'
        
        controleur.traiter(topic, message)
        
        # Vérifier que la méthode d'ajout a été appelée
        assert mock_db.ajouter_mesure_automatique.called
        print("✓ test_traiter_message_complet passé")


def test_traiter_message_avec_mac_dans_json():
    """Test le traitement d'un message avec MAC dans le JSON."""
    config_mqtt = {'broker': 'localhost', 'port': '1883'}
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    
    with patch('utils.controleur.DatabaseManager') as mock_db_class:
        mock_db = Mock()
        mock_db_class.return_value = mock_db
        mock_db.ajouter_mesure_automatique.return_value = True
        
        controleur = ControleurMQTT(config_mqtt, config_bdd)
        
        topic = "marais/sondes/data"
        message = '00:11:22:33:44:55 = {"timestamp": "2024-01-01T12:00:00", "mesure": {"CO2": 450}}'
        
        controleur.traiter(topic, message)
        
        assert mock_db.ajouter_mesure_automatique.called
        print("✓ test_traiter_message_avec_mac_dans_json passé")


def test_traiter_message_multiple_mesures():
    """Test le traitement d'un message avec plusieurs mesures."""
    config_mqtt = {'broker': 'localhost', 'port': '1883'}
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    
    with patch('utils.controleur.DatabaseManager') as mock_db_class:
        mock_db = Mock()
        mock_db_class.return_value = mock_db
        mock_db.ajouter_mesure_automatique.return_value = True
        
        controleur = ControleurMQTT(config_mqtt, config_bdd)
        
        topic = "marais/sondes/00:11:22:33:44:55"
        message = '{"timestamp": "2024-01-01T12:00:00", "mesure": [{"CO2": 450}, {"Temp": 22.5}]}'
        
        controleur.traiter(topic, message)
        
        # Vérifier que la méthode a été appelée 2 fois (une pour chaque mesure)
        assert mock_db.ajouter_mesure_automatique.call_count == 2
        print("✓ test_traiter_message_multiple_mesures passé")


def test_traiter_message_json_invalide():
    """Test le traitement d'un message JSON invalide."""
    config_mqtt = {'broker': 'localhost', 'port': '1883'}
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    
    with patch('utils.controleur.DatabaseManager') as mock_db_class:
        mock_db = Mock()
        mock_db_class.return_value = mock_db
        
        controleur = ControleurMQTT(config_mqtt, config_bdd)
        
        topic = "marais/sondes/00:11:22:33:44:55"
        message = "ceci n'est pas du json"
        
        # Ne devrait pas lever d'exception
        controleur.traiter(topic, message)
        
        # La base de données ne devrait pas être appelée
        assert not mock_db.ajouter_mesure_automatique.called
        print("✓ test_traiter_message_json_invalide passé")


def test_traiter_message_sans_mesure():
    """Test le traitement d'un message sans champ mesure."""
    config_mqtt = {'broker': 'localhost', 'port': '1883'}
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    
    with patch('utils.controleur.DatabaseManager') as mock_db_class:
        mock_db = Mock()
        mock_db_class.return_value = mock_db
        
        controleur = ControleurMQTT(config_mqtt, config_bdd)
        
        topic = "marais/sondes/00:11:22:33:44:55"
        message = '{"timestamp": "2024-01-01T12:00:00"}'
        
        controleur.traiter(topic, message)
        
        # La base de données ne devrait pas être appelée
        assert not mock_db.ajouter_mesure_automatique.called
        print("✓ test_traiter_message_sans_mesure passé")


def test_traiter_message_sans_mac():
    """Test le traitement d'un message sans adresse MAC."""
    config_mqtt = {'broker': 'localhost', 'port': '1883'}
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    
    with patch('utils.controleur.DatabaseManager') as mock_db_class:
        mock_db = Mock()
        mock_db_class.return_value = mock_db
        
        controleur = ControleurMQTT(config_mqtt, config_bdd)
        
        topic = "marais/sondes/data"  # Pas de MAC dans le topic
        message = '{"timestamp": "2024-01-01T12:00:00", "mesure": {"CO2": 450}}'
        
        controleur.traiter(topic, message)
        
        # La base de données ne devrait pas être appelée (pas de MAC)
        assert not mock_db.ajouter_mesure_automatique.called
        print("✓ test_traiter_message_sans_mac passé")


def test_traiter_message_sonde_inconnue():
    """Test le traitement d'un message d'une sonde inconnue."""
    config_mqtt = {'broker': 'localhost', 'port': '1883'}
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    
    with patch('utils.controleur.DatabaseManager') as mock_db_class:
        mock_db = Mock()
        mock_db_class.return_value = mock_db
        mock_db.ajouter_mesure_automatique.return_value = False  # Sonde non trouvée
        
        controleur = ControleurMQTT(config_mqtt, config_bdd)
        
        topic = "marais/sondes/AA:BB:CC:DD:EE:FF"
        message = '{"timestamp": "2024-01-01T12:00:00", "mesure": {"CO2": 450}}'
        
        controleur.traiter(topic, message)
        
        # La méthode a été appelée mais a retourné False
        assert mock_db.ajouter_mesure_automatique.called
        print("✓ test_traiter_message_sonde_inconnue passé")


if __name__ == "__main__":
    print("=== Tests unitaires pour ControleurMQTT ===\n")
    
    try:
        test_init_controleur()
        test_traiter_message_complet()
        test_traiter_message_avec_mac_dans_json()
        test_traiter_message_multiple_mesures()
        test_traiter_message_json_invalide()
        test_traiter_message_sans_mesure()
        test_traiter_message_sans_mac()
        test_traiter_message_sonde_inconnue()
        
        print("\n=== Tous les tests ont réussi ===")
    except AssertionError as e:
        print(f"\n✗ Test échoué: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Erreur inattendue: {e}")
        sys.exit(1)
