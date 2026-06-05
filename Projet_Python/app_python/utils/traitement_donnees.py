# traitement_donnees.py
# Auteur : [Sejourne Antoine]
# BTS CIEL 2ème année - Projet Marais R Site
# Traitement des données des sondes



"""
Module traitement_donnees.py - Traitement et parsing des données des sondes.

Ce module définit la classe TraitementDonnees qui fournit des méthodes utilitaires
pour extraire les informations des messages MQTT :
- Extraction de l'adresse MAC du topic
- Parsing du JSON et extraction des mesures
- Gestion des différents formats de messages
"""
import json


class TraitementDonnees:
    """
    Classe utilitaire pour le traitement des données des sondes.
    
    Cette classe fournit des méthodes statiques pour :
    - Extraire l'adresse MAC d'un topic MQTT
    - Parser les messages JSON et extraire les mesures
    
    Toutes les méthodes sont statiques car cette classe ne gère pas d'état.
    """

    @staticmethod
    def tester_seuil(donnees):
        """
        Méthode placeholder pour le test de seuil.
        
        Note: La gestion des seuils est actuellement implémentée dans sql.py
        via la méthode determiner_id_alerte.
        
        Args:
            donnees: Données à tester (non utilisé actuellement)
        """
        pass

    @staticmethod
    def extraire_mac(topic):
        """
        Extrait l'adresse MAC d'un topic MQTT.
        
        Essaye d'abord de trouver le MAC dans le dernier segment du topic,
        puis effectue une recherche regex dans tout le topic si nécessaire.
        
        Args:
            topic: Le topic MQTT (ex: "marais/sondes/00:11:22:33:44:55")
            
        Returns:
            L'adresse MAC au format XX:XX:XX:XX:XX:XX ou None si non trouvée
        """
        # Extraction du dernier segment du topic
        last_segment = topic.split("/")[-1]
        
        # Vérification si c'est un format MAC (contient des :)
        if ":" in last_segment:
            return last_segment
        
        # Recherche regex d'un format MAC standard dans tout le topic
        import re
        mac_match = re.search(
            r'[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}', 
            topic
        )
        if mac_match:
            return mac_match.group(0)
        return None

    @staticmethod
    def extraire_donnees(message):
        """
        Parse un message MQTT et extrait les données.
        
        Supporte deux formats de message :
        1. Format avec MAC : "MAC = {...JSON...}"
        2. Format JSON seul : "{...JSON...}"
        
        Args:
            message: Le contenu du message MQTT (string)
            
        Returns:
            Tuple (mesures, timestamp, mac) où :
            - mesures: Liste de dictionnaires {type: valeur} ou None
            - timestamp: Timestamp de la mesure ou None
            - mac: Adresse MAC extraite ou None (à récupérer du topic)
            
            Retourne (None, None, None) en cas d'erreur de parsing
        """
        try:
            # Nettoyage des espaces et retours à la ligne
            message = message.strip()
            
            # Format avec MAC : "MAC = {...}"
            if '=' in message:
                parts = message.split('=', 1)
                mac = parts[0].strip()
                json_part = parts[1].strip()
            else:
                # Format sans MAC : juste le JSON, le MAC sera extrait du topic
                mac = None
                json_part = message
            
            # Parsing du JSON
            data = json.loads(json_part)
            
            # Extraction des champs
            timestamp = data.get("timestamp")
            mesures = data.get("mesure")
            
            # Vérification de la présence des mesures
            if mesures is None:
                return None, None, None
            
            # Normalisation en liste si c'est un unique dictionnaire
            if isinstance(mesures, dict):
                mesures = [mesures]
            
            return mesures, timestamp, mac

        except (json.JSONDecodeError, KeyError):
            # En cas d'erreur de parsing, retourner None pour tout
            return None, None, None


# ============================================================
# Diagramme de classe UML - TraitementDonnees
# ============================================================
#
#   +-----------------------------------+
#   |       TraitementDonnees            |
#   +-----------------------------------+
#   | <<utility class>>                 |
#   +-----------------------------------+
#   | + tester_seuil(donnees)           |
#   | + extraire_mac(topic): str         |
#   | + extraire_donnees(message): tuple |
#   +-----------------------------------+
#
#   Méthodes statiques uniquement (pas d'attributs d'instance)
#
# ============================================================

if __name__ == "__main__":
    """
    Test direct de la classe TraitementDonnees.
    """
    # Test d'extraction de MAC
    topic_test = "marais/sondes/62:03:57:41:38:23"
    mac = TraitementDonnees.extraire_mac(topic_test)
    print(f"MAC extrait du topic: {mac}")
    
    # Test de parsing de message
    message_test = '{"timestamp":"2026-06-03T10:00:00","mesure":[{"ECO2":1200,"TVOC":100}]}'
    mesures, timestamp, mac_json = TraitementDonnees.extraire_donnees(message_test)
    print(f"Mesures: {mesures}")
    print(f"Timestamp: {timestamp}")
    print(f"MAC du JSON: {mac_json}")
