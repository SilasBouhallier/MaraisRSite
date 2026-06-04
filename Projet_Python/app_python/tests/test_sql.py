"""
Test unitaire pour le module sql.py

Ce test peut être lancé indépendamment avec :
    python test_sql.py

Note: Ce test nécessite une base de données MariaDB configurée.
Il utilise des variables d'environnement ou un fichier .env pour la connexion.
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock

# Ajout du chemin parent pour pouvoir importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.sql import DatabaseManager


class TestDatabaseManager(unittest.TestCase):
    """Tests pour la classe DatabaseManager."""

    def setUp(self):
        """Configuration initiale pour chaque test."""
        # Configuration de test pour la base de données
        self.config_bdd = {
            'host': 'localhost',
            'port': '3306',
            'database': 'Marais_R_Site',
            'user': 'test_user',
            'password': 'test_password'
        }

    def test_init_avec_config(self):
        """Test l'initialisation avec une configuration passée directement."""
        db = DatabaseManager(self.config_bdd)
        self.assertIsNotNone(db)
        print("✓ test_init_avec_config passé")

    @patch.dict(os.environ, {
        'MYSQL_MQTT_HOST': 'localhost',
        'MYSQL_MQTT_PORT': '3306',
        'MYSQL_MQTT_DATABASE': 'Marais_R_Site',
        'MYSQL_MQTT_USER': 'test_user',
        'MYSQL_MQTT_PASSWORD': 'test_password'
    })
    def test_init_avec_variables_docker(self):
        """Test l'initialisation avec les variables d'environnement Docker."""
        db = DatabaseManager()
        self.assertIsNotNone(db)
        print("✓ test_init_avec_variables_docker passé")

    @patch('utils.sql.mysql.connector.connect')
    def test_creer_connexion(self, mock_connect):
        """Test la création d'une connexion à la base de données."""
        mock_connection = Mock()
        mock_connect.return_value = mock_connection
        
        db = DatabaseManager(self.config_bdd)
        conn = db._DatabaseManager__creer_connexion()
        
        mock_connect.assert_called_once()
        self.assertEqual(conn, mock_connection)
        print("✓ test_creer_connexion passé")

    @patch('utils.sql.mysql.connector.connect')
    def test_trouver_id_emplacement_par_sonde(self, mock_connect):
        """Test la recherche d'ID d'emplacement par nom de sonde."""
        # Mock de la connexion et du curseur
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        mock_cursor.fetchone.return_value = (5,)
        
        db = DatabaseManager(self.config_bdd)
        result = db.trouver_id_emplacement_par_sonde('00:11:22:33:44:55')
        
        self.assertEqual(result, 5)
        mock_cursor.execute.assert_called_once()
        print("✓ test_trouver_id_emplacement_par_sonde passé")

    @patch('utils.sql.mysql.connector.connect')
    def test_trouver_id_emplacement_non_trouve(self, mock_connect):
        """Test la recherche d'ID d'emplacement quand la sonde n'existe pas."""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        mock_cursor.fetchone.return_value = None
        
        db = DatabaseManager(self.config_bdd)
        result = db.trouver_id_emplacement_par_sonde('AA:BB:CC:DD:EE:FF')
        
        self.assertIsNone(result)
        print("✓ test_trouver_id_emplacement_non_trouve passé")

    @patch('utils.sql.mysql.connector.connect')
    def test_trouver_id_type_mesure(self, mock_connect):
        """Test la recherche d'ID de type de mesure."""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        mock_cursor.fetchone.return_value = (2,)
        
        db = DatabaseManager(self.config_bdd)
        result = db.trouver_id_type_mesure('CO2')
        
        self.assertEqual(result, 2)
        print("✓ test_trouver_id_type_mesure passé")

    @patch('utils.sql.mysql.connector.connect')
    def test_trouver_id_type_mesure_par_defaut(self, mock_connect):
        """Test la recherche d'ID de type de mesure avec valeur par défaut."""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        mock_cursor.fetchone.return_value = None
        
        db = DatabaseManager(self.config_bdd)
        result = db.trouver_id_type_mesure('TypeInconnu')
        
        self.assertEqual(result, 1)  # Valeur par défaut
        print("✓ test_trouver_id_type_mesure_par_defaut passé")

    @patch('utils.sql.mysql.connector.connect')
    def test_determiner_id_alerte_normal(self, mock_connect):
        """Test la détermination d'ID d'alerte niveau normal."""
        mock_connection = Mock()
        mock_cursor = Mock(dictionary=True)
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        mock_cursor.fetchone.return_value = {
            'valeur_alerte_seuil': 1000.0,
            'valeur_danger_seuil': 2000.0
        }
        
        db = DatabaseManager(self.config_bdd)
        result = db.determiner_id_alerte(500.0, 'CO2')
        
        self.assertEqual(result, 1)  # Normal
        print("✓ test_determiner_id_alerte_normal passé")

    @patch('utils.sql.mysql.connector.connect')
    def test_determiner_id_alerte_attention(self, mock_connect):
        """Test la détermination d'ID d'alerte niveau attention."""
        mock_connection = Mock()
        mock_cursor = Mock(dictionary=True)
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        mock_cursor.fetchone.return_value = {
            'valeur_alerte_seuil': 1000.0,
            'valeur_danger_seuil': 2000.0
        }
        
        db = DatabaseManager(self.config_bdd)
        result = db.determiner_id_alerte(1500.0, 'CO2')
        
        self.assertEqual(result, 2)  # Attention
        print("✓ test_determiner_id_alerte_attention passé")

    @patch('utils.sql.mysql.connector.connect')
    def test_determiner_id_alerte_danger(self, mock_connect):
        """Test la détermination d'ID d'alerte niveau danger."""
        mock_connection = Mock()
        mock_cursor = Mock(dictionary=True)
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        mock_cursor.fetchone.return_value = {
            'valeur_alerte_seuil': 1000.0,
            'valeur_danger_seuil': 2000.0
        }
        
        db = DatabaseManager(self.config_bdd)
        result = db.determiner_id_alerte(2500.0, 'CO2')
        
        self.assertEqual(result, 3)  # Danger
        print("✓ test_determiner_id_alerte_danger passé")

    @patch('utils.sql.mysql.connector.connect')
    def test_ajouter_mesure(self, mock_connect):
        """Test l'ajout d'une mesure dans la base de données."""
        mock_connection = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_connection
        mock_connection.cursor.return_value = mock_cursor
        mock_connection.is_connected.return_value = True
        
        db = DatabaseManager(self.config_bdd)
        result = db.ajouter_mesure(
            valeur=450.0,
            date_heure='2024-01-01T12:00:00',
            id_emplacement=1,
            id_alerte=1,
            id_type_mesure=2
        )
        
        self.assertTrue(result)
        mock_cursor.execute.assert_called_once()
        mock_connection.commit.assert_called_once()
        print("✓ test_ajouter_mesure passé")


if __name__ == "__main__":
    print("=== Tests unitaires pour DatabaseManager ===\n")
    
    # Exécution des tests
    unittest.main(verbosity=2, exit=False)
    
    print("\n=== Tests terminés ===")
