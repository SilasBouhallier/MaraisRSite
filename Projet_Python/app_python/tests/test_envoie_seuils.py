"""
Test unitaire pour le module envoie_seuils.py

Ce test peut être lancé indépendamment avec :
    python test_envoie_seuils.py
"""

import sys
import os
from unittest.mock import Mock, patch

# Ajout du chemin parent pour pouvoir importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.envoie_seuils import EnvoiSeuils


def test_init():
    """Test l'initialisation de EnvoiSeuils."""
    config_bdd = {
        'host': 'localhost',
        'port': '3306',
        'database': 'Marais_R_Site',
        'user': 'test_user',
        'password': 'test_password'
    }
    config_mqtt = {
        'broker': 'localhost',
        'port': '1883',
        'topics_sonde': 'marais/sondes/#',
        'topics_seuils': 'marais/seuils/#'
    }
    
    with patch('utils.envoie_seuils.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        envoi_seuils = EnvoiSeuils(config_bdd, config_mqtt)
        
        assert envoi_seuils.config == config_mqtt
        assert envoi_seuils.topic == 'marais/sondes/seuils'
        assert not envoi_seuils.connecte
        print("✓ test_init passé")


def test_init_avec_auth():
    """Test l'initialisation avec authentification."""
    config_bdd = {
        'host': 'localhost',
        'port': '3306',
        'database': 'Marais_R_Site',
        'user': 'test_user',
        'password': 'test_password'
    }
    config_mqtt = {
        'broker': 'localhost',
        'port': '1883',
        'topics_sonde': 'marais/sondes/#',
        'username': 'test_user',
        'password': 'test_password'
    }
    
    with patch('utils.envoie_seuils.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        envoi_seuils = EnvoiSeuils(config_bdd, config_mqtt)
        
        mock_client.username_pw_set.assert_called_once_with('test_user', 'test_password')
        print("✓ test_init_avec_auth passé")


def test_init_avec_tls():
    """Test l'initialisation avec TLS (port 8883)."""
    config_bdd = {
        'host': 'localhost',
        'port': '3306',
        'database': 'Marais_R_Site',
        'user': 'test_user',
        'password': 'test_password'
    }
    config_mqtt = {
        'broker': 'localhost',
        'port': '8883',
        'topics_sonde': 'marais/sondes/#'
    }
    
    with patch('utils.envoie_seuils.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        envoi_seuils = EnvoiSeuils(config_bdd, config_mqtt)
        
        mock_client.tls_set.assert_called_once()
        print("✓ test_init_avec_tls passé")


def test_on_connect_succes():
    """Test le callback on_connect en cas de succès."""
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    config_mqtt = {'broker': 'localhost', 'port': '1883', 'topics_sonde': 'marais/sondes/#'}
    
    with patch('utils.envoie_seuils.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        envoi_seuils = EnvoiSeuils(config_bdd, config_mqtt)
        
        # Simulation du callback on_connect avec rc=0 (succès)
        envoi_seuils.on_connect(mock_client, None, None, 0)
        
        assert envoi_seuils.connecte == True
        print("✓ test_on_connect_succes passé")


def test_on_connect_echec():
    """Test le callback on_connect en cas d'échec."""
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    config_mqtt = {'broker': 'localhost', 'port': '1883', 'topics_sonde': 'marais/sondes/#'}
    
    with patch('utils.envoie_seuils.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        envoi_seuils = EnvoiSeuils(config_bdd, config_mqtt)
        
        # Simulation du callback on_connect avec rc=1 (échec)
        envoi_seuils.on_connect(mock_client, None, None, 1)
        
        assert envoi_seuils.connecte == False
        print("✓ test_on_connect_echec passé")


def test_on_disconnect():
    """Test le callback on_disconnect."""
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    config_mqtt = {'broker': 'localhost', 'port': '1883', 'topics_sonde': 'marais/sondes/#'}
    
    with patch('utils.envoie_seuils.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        envoi_seuils = EnvoiSeuils(config_bdd, config_mqtt)
        
        # Simulation du callback on_disconnect
        envoi_seuils.on_disconnect(mock_client, None, 0)
        
        assert envoi_seuils.connecte == False
        print("✓ test_on_disconnect passé")


def test_publier_connecte():
    """Test la publication de seuils quand connecté."""
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    config_mqtt = {'broker': 'localhost', 'port': '1883', 'topics_sonde': 'marais/sondes/#'}
    
    with patch('utils.envoie_seuils.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_result = Mock()
        mock_result.mid = 123
        mock_client.publish.return_value = mock_result
        
        envoi_seuils = EnvoiSeuils(config_bdd, config_mqtt)
        envoi_seuils.connecte = True
        
        payload = {"Seuils": {"valeur_alerte_seuil": 150.0, "valeur_danger_seuil": 200.0}}
        result = envoi_seuils.publier(payload)
        
        assert result is not None
        assert result.mid == 123
        mock_client.publish.assert_called_once()
        print("✓ test_publier_connecte passé")


def test_publier_non_connecte():
    """Test la publication de seuils quand non connecté."""
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    config_mqtt = {'broker': 'localhost', 'port': '1883', 'topics_sonde': 'marais/sondes/#'}
    
    with patch('utils.envoie_seuils.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        envoi_seuils = EnvoiSeuils(config_bdd, config_mqtt)
        envoi_seuils.connecte = False
        
        payload = {"Seuils": {"valeur_alerte_seuil": 150.0, "valeur_danger_seuil": 200.0}}
        result = envoi_seuils.publier(payload)
        
        assert result is None
        mock_client.publish.assert_not_called()
        print("✓ test_publier_non_connecté passé")


def test_publier_format_json():
    """Test que le payload est bien converti en JSON compact."""
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    config_mqtt = {'broker': 'localhost', 'port': '1883', 'topics_sonde': 'marais/sondes/#'}
    
    with patch('utils.envoie_seuils.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_result = Mock()
        mock_client.publish.return_value = mock_result
        
        envoi_seuils = EnvoiSeuils(config_bdd, config_mqtt)
        envoi_seuils.connecte = True
        
        payload = {"Seuils": {"valeur_alerte_seuil": 150.0, "valeur_danger_seuil": 200.0}}
        envoi_seuils.publier(payload)
        
        # Vérifier les arguments de publish
        call_args = mock_client.publish.call_args
        message_json = call_args[0][1]  # Le deuxième argument est le message
        
        # Vérifier que c'est du JSON compact (sans espaces)
        assert ' ' not in message_json
        assert '{"Seuils":' in message_json
        print("✓ test_publier_format_json passé")


def test_demarrer():
    """Test la méthode demarrer."""
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    config_mqtt = {'broker': 'localhost', 'port': '1883', 'topics_sonde': 'marais/sondes/#'}
    
    with patch('utils.envoie_seuils.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        envoi_seuils = EnvoiSeuils(config_bdd, config_mqtt)
        
        # La méthode demarrer ne fait qu'afficher un message
        envoi_seuils.demarrer()
        print("✓ test_demarrer passé")


def test_arreter():
    """Test la méthode arreter."""
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    config_mqtt = {'broker': 'localhost', 'port': '1883', 'topics_sonde': 'marais/sondes/#'}
    
    with patch('utils.envoie_seuils.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        envoi_seuils = EnvoiSeuils(config_bdd, config_mqtt)
        
        envoi_seuils.arreter()
        
        mock_client.loop_stop.assert_called_once()
        mock_client.disconnect.assert_called_once()
        print("✓ test_arreter passé")


if __name__ == "__main__":
    print("=== Tests unitaires pour EnvoiSeuils ===\n")
    
    try:
        test_init()
        test_init_avec_auth()
        test_init_avec_tls()
        test_on_connect_succes()
        test_on_connect_echec()
        test_on_disconnect()
        test_publier_connecte()
        test_publier_non_connecte()
        test_publier_format_json()
        test_demarrer()
        test_arreter()
        
        print("\n=== Tous les tests ont réussi ===")
    except AssertionError as e:
        print(f"\n✗ Test échoué: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Erreur inattendue: {e}")
        sys.exit(1)
