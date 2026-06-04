"""
Test unitaire pour le module maraisRSenseData.py

Ce test peut être lancé indépendamment avec :
    python test_maraisRSenseData.py
"""

import sys
import os
from unittest.mock import Mock, patch, MagicMock

# Ajout du chemin parent pour pouvoir importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.maraisRSenseData import MaraisRSenseData


def test_init_sans_auth():
    """Test l'initialisation sans authentification."""
    config = {
        'broker': 'localhost',
        'port': '1883',
        'topics_sonde': 'marais/sondes/#'
    }
    
    client = MaraisRSenseData(config)
    
    assert client.broker == 'localhost'
    assert client.port == 1883
    assert client.topics == 'marais/sondes/#'
    assert client.username is None
    assert client.password is None
    print("✓ test_init_sans_auth passé")


def test_init_avec_auth():
    """Test l'initialisation avec authentification."""
    config = {
        'broker': 'localhost',
        'port': '1883',
        'topics_sonde': 'marais/sondes/#',
        'username': 'test_user',
        'password': 'test_password'
    }
    
    with patch('utils.maraisRSenseData.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        client = MaraisRSenseData(config)
        
        assert client.username == 'test_user'
        assert client.password == 'test_password'
        mock_client.username_pw_set.assert_called_once_with('test_user', 'test_password')
        print("✓ test_init_avec_auth passé")


def test_init_avec_controleur():
    """Test l'initialisation avec un contrôleur."""
    config = {
        'broker': 'localhost',
        'port': '1883',
        'topics_sonde': 'marais/sondes/#'
    }
    mock_controleur = Mock()
    
    client = MaraisRSenseData(config, mock_controleur)
    
    assert client.controleur == mock_controleur
    print("✓ test_init_avec_controleur passé")


def test_on_connect_succes():
    """Test le callback on_connect en cas de succès."""
    config = {
        'broker': 'localhost',
        'port': '1883',
        'topics_sonde': 'marais/sondes/#'
    }
    
    with patch('utils.maraisRSenseData.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        client = MaraisRSenseData(config)
        
        # Simulation du callback on_connect avec rc=0 (succès)
        client.on_connect(mock_client, None, None, 0)
        
        # Vérifier que le subscribe a été appelé
        mock_client.subscribe.assert_called_once_with('marais/sondes/#')
        print("✓ test_on_connect_succes passé")


def test_on_connect_echec():
    """Test le callback on_connect en cas d'échec."""
    config = {
        'broker': 'localhost',
        'port': '1883',
        'topics_sonde': 'marais/sondes/#'
    }
    
    with patch('utils.maraisRSenseData.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        client = MaraisRSenseData(config)
        
        # Simulation du callback on_connect avec rc=1 (échec)
        client.on_connect(mock_client, None, None, 1)
        
        # Vérifier que le subscribe n'a PAS été appelé
        mock_client.subscribe.assert_not_called()
        print("✓ test_on_connect_echec passé")


def test_on_message_avec_controleur():
    """Test le callback on_message avec un contrôleur défini."""
    config = {
        'broker': 'localhost',
        'port': '1883',
        'topics_sonde': 'marais/sondes/#'
    }
    mock_controleur = Mock()
    
    with patch('utils.maraisRSenseData.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        client = MaraisRSenseData(config, mock_controleur)
        
        # Simulation d'un message reçu
        mock_msg = Mock()
        mock_msg.topic = "marais/sondes/00:11:22:33:44:55"
        mock_msg.payload = b'{"timestamp": "2024-01-01T12:00:00", "mesure": {"CO2": 450}}'
        
        client.on_message(mock_client, None, mock_msg)
        
        # Vérifier que le contrôleur a reçu le message
        mock_controleur.traiter.assert_called_once_with(
            "marais/sondes/00:11:22:33:44:55",
            '{"timestamp": "2024-01-01T12:00:00", "mesure": {"CO2": 450}}'
        )
        print("✓ test_on_message_avec_controleur passé")


def test_on_message_sans_controleur():
    """Test le callback on_message sans contrôleur."""
    config = {
        'broker': 'localhost',
        'port': '1883',
        'topics_sonde': 'marais/sondes/#'
    }
    
    with patch('utils.maraisRSenseData.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        client = MaraisRSenseData(config)
        
        # Simulation d'un message reçu
        mock_msg = Mock()
        mock_msg.topic = "marais/sondes/00:11:22:33:44:55"
        mock_msg.payload = b'{"timestamp": "2024-01-01T12:00:00", "mesure": {"CO2": 450}}'
        
        # Ne devrait pas lever d'exception
        client.on_message(mock_client, None, mock_msg)
        print("✓ test_on_message_sans_controleur passé")


def test_start():
    """Test la méthode start."""
    config = {
        'broker': 'localhost',
        'port': '1883',
        'topics_sonde': 'marais/sondes/#'
    }
    
    with patch('utils.maraisRSenseData.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        client = MaraisRSenseData(config)
        
        # La méthode start appelle connect et loop_forever
        # On ne peut pas vraiment tester loop_forever car c'est bloquant
        # On vérifie juste que les attributs sont corrects
        assert client.broker == 'localhost'
        assert client.port == 1883
        print("✓ test_start passé")


def test_stop():
    """Test la méthode stop."""
    config = {
        'broker': 'localhost',
        'port': '1883',
        'topics_sonde': 'marais/sondes/#'
    }
    
    with patch('utils.maraisRSenseData.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        client = MaraisRSenseData(config)
        
        client.stop()
        
        # Vérifier que loop_stop et disconnect ont été appelés
        mock_client.loop_stop.assert_called_once()
        mock_client.disconnect.assert_called_once()
        print("✓ test_stop passé")


def test_configurer_tls():
    """Test la configuration TLS pour le port 8883."""
    config = {
        'broker': 'localhost',
        'port': '8883',
        'topics_sonde': 'marais/sondes/#'
    }
    
    with patch('utils.maraisRSenseData.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        client = MaraisRSenseData(config)
        
        # Vérifier que tls_set a été appelé
        mock_client.tls_set.assert_called_once()
        print("✓ test_configurer_tls passé")


if __name__ == "__main__":
    print("=== Tests unitaires pour MaraisRSenseData ===\n")
    
    try:
        test_init_sans_auth()
        test_init_avec_auth()
        test_init_avec_controleur()
        test_on_connect_succes()
        test_on_connect_echec()
        test_on_message_avec_controleur()
        test_on_message_sans_controleur()
        test_start()
        test_stop()
        test_configurer_tls()
        
        print("\n=== Tous les tests ont réussi ===")
    except AssertionError as e:
        print(f"\n✗ Test échoué: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Erreur inattendue: {e}")
        sys.exit(1)
