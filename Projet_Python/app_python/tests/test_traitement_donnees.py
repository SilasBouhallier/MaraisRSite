"""
Test unitaire pour le module traitement_donnees.py

Ce test peut être lancé indépendamment avec :
    python test_traitement_donnees.py
"""

import sys
import os

# Ajout du chemin parent pour pouvoir importer les modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.traitement_donnees import TraitementDonnees


def test_extraire_mac_dernier_segment():
    """Test l'extraction de MAC depuis le dernier segment du topic."""
    topic = "marais/sondes/00:11:22:33:44:55"
    result = TraitementDonnees.extraire_mac(topic)
    assert result == "00:11:22:33:44:55", f"Attendu: 00:11:22:33:44:55, Reçu: {result}"
    print("✓ test_extraire_mac_dernier_segment passé")


def test_extraire_mac_regex():
    """Test l'extraction de MAC via regex dans tout le topic."""
    topic = "marais/sondes/data/00:11:22:33:44:55/mesure"
    result = TraitementDonnees.extraire_mac(topic)
    assert result == "00:11:22:33:44:55", f"Attendu: 00:11:22:33:44:55, Reçu: {result}"
    print("✓ test_extraire_mac_regex passé")


def test_extraire_mac_non_trouve():
    """Test le cas où aucune MAC n'est trouvée."""
    topic = "marais/sondes/data"
    result = TraitementDonnees.extraire_mac(topic)
    assert result is None, f"Attendu: None, Reçu: {result}"
    print("✓ test_extraire_mac_non_trouve passé")


def test_extraire_donnees_avec_mac():
    """Test le parsing d'un message avec MAC."""
    message = "00:11:22:33:44:55 = {\"timestamp\": \"2024-01-01T12:00:00\", \"mesure\": {\"CO2\": 450}}"
    mesures, timestamp, mac = TraitementDonnees.extraire_donnees(message)
    
    assert mac == "00:11:22:33:44:55", f"Attendu: 00:11:22:33:44:55, Reçu: {mac}"
    assert timestamp == "2024-01-01T12:00:00", f"Attendu: 2024-01-01T12:00:00, Reçu: {timestamp}"
    assert isinstance(mesures, list), f"Attendu: list, Reçu: {type(mesures)}"
    assert len(mesures) == 1, f"Attendu: 1 mesure, Reçu: {len(mesures)}"
    assert mesures[0] == {"CO2": 450}, f"Attendu: {{'CO2': 450}}, Reçu: {mesures[0]}"
    print("✓ test_extraire_donnees_avec_mac passé")


def test_extraire_donnees_sans_mac():
    """Test le parsing d'un message sans MAC."""
    message = "{\"timestamp\": \"2024-01-01T12:00:00\", \"mesure\": {\"CO2\": 450}}"
    mesures, timestamp, mac = TraitementDonnees.extraire_donnees(message)
    
    assert mac is None, f"Attendu: None, Reçu: {mac}"
    assert timestamp == "2024-01-01T12:00:00", f"Attendu: 2024-01-01T12:00:00, Reçu: {timestamp}"
    assert isinstance(mesures, list), f"Attendu: list, Reçu: {type(mesures)}"
    assert len(mesures) == 1, f"Attendu: 1 mesure, Reçu: {len(mesures)}"
    print("✓ test_extraire_donnees_sans_mac passé")


def test_extraire_donnees_multiple_mesures():
    """Test le parsing d'un message avec plusieurs mesures."""
    message = "{\"timestamp\": \"2024-01-01T12:00:00\", \"mesure\": [{\"CO2\": 450}, {\"Temp\": 22.5}]}"
    mesures, timestamp, mac = TraitementDonnees.extraire_donnees(message)
    
    assert isinstance(mesures, list), f"Attendu: list, Reçu: {type(mesures)}"
    assert len(mesures) == 2, f"Attendu: 2 mesures, Reçu: {len(mesures)}"
    assert mesures[0] == {"CO2": 450}, f"Attendu: {{'CO2': 450}}, Reçu: {mesures[0]}"
    assert mesures[1] == {"Temp": 22.5}, f"Attendu: {{'Temp': 22.5}}, Reçu: {mesures[1]}"
    print("✓ test_extraire_donnees_multiple_mesures passé")


def test_extraire_donnees_json_invalide():
    """Test le parsing d'un message JSON invalide."""
    message = "ceci n'est pas du json"
    mesures, timestamp, mac = TraitementDonnees.extraire_donnees(message)
    
    assert mesures is None, f"Attendu: None, Reçu: {mesures}"
    assert timestamp is None, f"Attendu: None, Reçu: {timestamp}"
    assert mac is None, f"Attendu: None, Reçu: {mac}"
    print("✓ test_extraire_donnees_json_invalide passé")


def test_extraire_donnees_sans_mesure():
    """Test le parsing d'un message sans champ mesure."""
    message = "{\"timestamp\": \"2024-01-01T12:00:00\"}"
    mesures, timestamp, mac = TraitementDonnees.extraire_donnees(message)
    
    assert mesures is None, f"Attendu: None, Reçu: {mesures}"
    assert timestamp is None, f"Attendu: None, Reçu: {timestamp}"
    assert mac is None, f"Attendu: None, Reçu: {mac}"
    print("✓ test_extraire_donnees_sans_mesure passé")


def test_extraire_donnees_avec_espaces():
    """Test le parsing d'un message avec espaces et retours à la ligne."""
    message = """
    00:11:22:33:44:55 = 
    {"timestamp": "2024-01-01T12:00:00", "mesure": {"CO2": 450}}
    """
    mesures, timestamp, mac = TraitementDonnees.extraire_donnees(message)
    
    assert mac == "00:11:22:33:44:55", f"Attendu: 00:11:22:33:44:55, Reçu: {mac}"
    assert timestamp == "2024-01-01T12:00:00", f"Attendu: 2024-01-01T12:00:00, Reçu: {timestamp}"
    assert isinstance(mesures, list), f"Attendu: list, Reçu: {type(mesures)}"
    print("✓ test_extraire_donnees_avec_espaces passé")


if __name__ == "__main__":
    print("=== Tests unitaires pour TraitementDonnees ===\n")
    
    try:
        test_extraire_mac_dernier_segment()
        test_extraire_mac_regex()
        test_extraire_mac_non_trouve()
        test_extraire_donnees_avec_mac()
        test_extraire_donnees_sans_mac()
        test_extraire_donnees_multiple_mesures()
        test_extraire_donnees_json_invalide()
        test_extraire_donnees_sans_mesure()
        test_extraire_donnees_avec_espaces()
        
        print("\n=== Tous les tests ont réussi ===")
    except AssertionError as e:
        print(f"\n✗ Test échoué: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Erreur inattendue: {e}")
        sys.exit(1)
