"""
Test unitaire pour le module alarmes_mqtt.py

Ce test peut être lancé indépendamment avec :
    python test_alarmes_mqtt.py
"""

import sys
import os
from unittest.mock import Mock, patch

# Ajout du chemin parent pour pouvoir importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.alarmes_mqtt import AlarmesMQTT


def test_init():
    """Test l'initialisation de AlarmesMQTT."""
    config_bdd = {
        'host': 'localhost',
        'port': '3306',
        'database': 'Marais_R_Site',
        'user': 'test_user',
        'password': 'test_password'
    }
    config_mqtt = {
        'broker': 'localhost',
        'port': '1883'
    }
    
    with patch('utils.alarmes_mqtt.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        alarmes = AlarmesMQTT(config_bdd, config_mqtt)
        
        assert alarmes is not None
        print("✓ test_init passé")


def test_init_avec_auth():
    """Test l'initialisation avec authentification."""
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    config_mqtt = {
        'broker': 'localhost',
        'port': '1883',
        'username': 'test_user',
        'password': 'test_password'
    }
    
    with patch('utils.alarmes_mqtt.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        alarmes = AlarmesMQTT(config_bdd, config_mqtt)
        
        mock_client.username_pw_set.assert_called_once_with('test_user', 'test_password')
        print("✓ test_init_avec_auth passé")


def test_init_avec_tls():
    """Test l'initialisation avec TLS (port 8883)."""
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    config_mqtt = {
        'broker': 'localhost',
        'port': '8883'
    }
    
    with patch('utils.alarmes_mqtt.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        alarmes = AlarmesMQTT(config_bdd, config_mqtt)
        
        mock_client.tls_set.assert_called_once()
        print("✓ test_init_avec_tls passé")


def test_declencher_gyrophare_1():
    """Test le déclenchement du gyrophare 1."""
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    config_mqtt = {'broker': 'localhost', 'port': '1883'}
    
    with patch('utils.alarmes_mqtt.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_result = Mock()
        mock_result.mid = 456
        mock_client.publish.return_value = mock_result
        
        alarmes = AlarmesMQTT(config_bdd, config_mqtt)
        alarmes.connected = True
        
        result = alarmes.declencher_gyrophare(1)
        
        assert result is not None
        assert result.mid == 456
        mock_client.publish.assert_called_once()
        
        # Vérifier le topic
        call_args = mock_client.publish.call_args
        topic = call_args[0][0]
        assert topic == "marais/alarme/gyrophare_1/rpc"
        print("✓ test_declencher_gyrophare_1 passé")


def test_declencher_gyrophare_2():
    """Test le déclenchement du gyrophare 2."""
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    config_mqtt = {'broker': 'localhost', 'port': '1883'}
    
    with patch('utils.alarmes_mqtt.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_result = Mock()
        mock_client.publish.return_value = mock_result
        
        alarmes = AlarmesMQTT(config_bdd, config_mqtt)
        alarmes.connected = True
        
        result = alarmes.declencher_gyrophare(2)
        
        assert result is not None
        mock_client.publish.assert_called_once()
        
        # Vérifier le topic
        call_args = mock_client.publish.call_args
        topic = call_args[0][0]
        assert topic == "marais/alarme/gyrophare_2/rpc"
        print("✓ test_declencher_gyrophare_2 passé")


def test_declencher_gyrophare_non_connecte():
    """Test le déclenchement de gyrophare quand non connecté."""
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    config_mqtt = {'broker': 'localhost', 'port': '1883'}
    
    with patch('utils.alarmes_mqtt.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        alarmes = AlarmesMQTT(config_bdd, config_mqtt)
        alarmes.connected = False
        
        result = alarmes.declencher_gyrophare(1)
        
        assert result is None
        mock_client.publish.assert_not_called()
        print("✓ test_declencher_gyrophare_non_connecte passé")


def test_payload_json_rpc():
    """Test que le payload est bien formaté en JSON-RPC."""
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    config_mqtt = {'broker': 'localhost', 'port': '1883'}
    
    with patch('utils.alarmes_mqtt.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_result = Mock()
        mock_client.publish.return_value = mock_result
        
        alarmes = AlarmesMQTT(config_bdd, config_mqtt)
        alarmes.connected = True
        
        alarmes.declencher_gyrophare(1)
        
        # Vérifier le payload
        call_args = mock_client.publish.call_args
        payload = call_args[0][1]
        
        # Vérifier que c'est du JSON compact
        assert ' ' not in payload
        assert '"id":1' in payload
        assert '"method":"Switch.Set"' in payload
        assert '"on":true' in payload
        print("✓ test_payload_json_rpc passé")


def test_demarrer():
    """Test la méthode demarrer."""
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    config_mqtt = {'broker': 'localhost', 'port': '1883'}
    
    with patch('utils.alarmes_mqtt.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        alarmes = AlarmesMQTT(config_bdd, config_mqtt)
        
        # La méthode demarrer ne fait rien (pass)
        alarmes.demarrer()
        print("✓ test_demarrer passé")


def test_arreter():
    """Test la méthode arreter."""
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    config_mqtt = {'broker': 'localhost', 'port': '1883'}
    
    with patch('utils.alarmes_mqtt.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        alarmes = AlarmesMQTT(config_bdd, config_mqtt)
        
        alarmes.arreter()
        
        mock_client.loop_stop.assert_called_once()
        print("✓ test_arreter passé")


def test_callback_connect():
    """Test que le callback on_connect met connected à True."""
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    config_mqtt = {'broker': 'localhost', 'port': '1883'}
    
    with patch('utils.alarmes_mqtt.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        alarmes = AlarmesMQTT(config_bdd, config_mqtt)
        
        # Simuler le callback on_connect avec rc=0
        alarmes.client.on_connect(mock_client, None, None, 0)
        
        assert alarmes.connected == True
        print("✓ test_callback_connect passé")


def test_callback_disconnect():
    """Test que le callback on_disconnect met connected à False."""
    config_bdd = {'host': 'localhost', 'port': '3306', 'database': 'Marais_R_Site', 'user': 'test', 'password': 'test'}
    config_mqtt = {'broker': 'localhost', 'port': '1883'}
    
    with patch('utils.alarmes_mqtt.mqtt.Client') as mock_client_class:
        mock_client = Mock()
        mock_client_class.return_value = mock_client
        
        alarmes = AlarmesMQTT(config_bdd, config_mqtt)
        alarmes.connected = True
        
        # Simuler le callback on_disconnect
        alarmes.client.on_disconnect(mock_client, None, 0)
        
        assert alarmes.connected == False
        print("✓ test_callback_disconnect passé")


if __name__ == "__main__":
    print("=== Tests unitaires pour AlarmesMQTT ===\n")
    
    try:
        test_init()
        test_init_avec_auth()
        test_init_avec_tls()
        test_declencher_gyrophare_1()
        test_declencher_gyrophare_2()
        test_declencher_gyrophare_non_connecte()
        test_payload_json_rpc()
        test_demarrer()
        test_arreter()
        test_callback_connect()
        test_callback_disconnect()
        
        print("\n=== Tous les tests ont réussi ===")
    except AssertionError as e:
        print(f"\n✗ Test échoué: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Erreur inattendue: {e}")
        sys.exit(1)
