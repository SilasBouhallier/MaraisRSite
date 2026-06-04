"""
Module alarmes_mqtt.py - Service de déclenchement des alarmes via MQTT.

Ce module implémente le service de contrôle des gyrophares (alarmes)
via le broker MQTT en utilisant le protocole JSON-RPC.
"""

import paho.mqtt.client as mqtt
import json
import time
import ssl


class AlarmesMQTT:
    """
    Contrôleur MQTT des gyrophares (alarmes).
    
    Cette classe gère la connexion au broker MQTT et le contrôle
    des gyrophares via des messages JSON-RPC sur les topics dédiés.
    """

    def __init__(self, config_bdd, config_mqtt):
        """
        Initialise le contrôleur MQTT et établit la connexion.
        
        Args:
            config_bdd: Configuration base de données (non utilisée actuellement)
            config_mqtt: Dictionnaire de configuration MQTT (broker, port, auth, etc.)
        """
        cfg = config_mqtt
        
        # Création du client MQTT avec identifiant unique
        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION1,
            client_id="marais_alarmes_controller"
        )
        
        # Callbacks pour le suivi de la connexion
        self.client.on_connect = lambda c, u, f, rc: setattr(self, 'connected', rc == 0)
        self.client.on_disconnect = lambda c, u, rc: setattr(self, 'connected', False)
        
        # Configuration de l'authentification si credentials fournis
        if cfg.get('username') and cfg.get('password'):
            self.client.username_pw_set(cfg['username'], cfg['password'])
        
        # Configuration TLS si port sécurisé (8883)
        if int(cfg.get('port')) == 8883:
            self.client.tls_set(cert_reqs=ssl.CERT_NONE)
        
        # Connexion au broker et démarrage de la boucle réseau
        self.client.connect(cfg.get('broker'), int(cfg.get('port')), 60)
        self.client.loop_start()
        time.sleep(0.5)  # Attente de la connexion

    def declencher_gyrophare(self, numero_gyrophare):
        """
        Déclenche un gyrophare via MQTT.
        
        Args:
            numero_gyrophare: Numéro du gyrophare (1 ou 2)
            
        Returns:
            Résultat de la publication MQTT ou None si non connecté
        """
        if not getattr(self, 'connected', False):
            return None
        
        # Construction du topic RPC
        topic = f"marais/alarme/gyrophare_{numero_gyrophare}/rpc"
        
        # Construction du payload JSON-RPC
        payload = {
            "id": 1,
            "src": f"marais/alarme/gyrophare_{numero_gyrophare}",
            "method": "Switch.Set",
            "params": {
                "id": 0,
                "on": True
            }
        }
        
        return self.client.publish(
            topic,
            json.dumps(payload, separators=(',', ':')),
            qos=1,
            retain=False
        )

    def demarrer(self):
        """
        Méthode de démarrage pour compatibilité avec application.py.
        La connexion est déjà établie dans __init__.
        """
        pass

    def arreter(self):
        """
        Arrête proprement le client MQTT.
        Arrête la boucle réseau et ferme la connexion.
        """
        self.client.loop_stop()


if __name__ == "__main__":
    """
    Test direct du module : python utils/alarmes_mqtt.py
    
    Ce bloc permet de tester le déclenchement des alarmes sans lancer
    l'application complète.
    """
    import os
    import re
    import sys
    from dotenv import load_dotenv
    from configparser import ConfigParser
    
    # Détermination du chemin de base
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Chargement des variables d'environnement
    load_dotenv(os.path.join(base_dir, '.env'))
    
    def subst(v):
        """Fonction de substitution des variables ${VAR} par leurs valeurs."""
        if not v:
            return v
        return re.sub(r'\$\{([^}]+)\}', lambda m: os.getenv(m.group(1), ''), v).strip()
    
    # Chargement du fichier de configuration
    parser = ConfigParser()
    parser.read(os.path.join(base_dir, 'app_python', 'utils', 'configuration.cfg'))
    
    # Extraction des configurations avec substitution
    config_mqtt = {k: subst(v) for k, v in parser['MQTT'].items()}
    config_bdd = {k: subst(v) for k, v in parser['BDD'].items()}
    
    # Affichage des informations de connexion
    print(f"Broker: {config_mqtt.get('broker')}")
    print(f"Port: {config_mqtt.get('port')}")
    print()
    
    # Test de connexion et contrôle des gyrophares
    print("[1] Connexion...")
    controller = AlarmesMQTT(config_bdd, config_mqtt)
    print()
    
    # Test : allumer le gyrophare 2
    print("[2] Déclencher gyrophare 2...")
    result = controller.declencher_gyrophare(2)
    if result:
        print(f"Commande envoyée ! MID={result.mid}")
    else:
        print("Non connecté")
    print()
    
    # Test : allumer le gyrophare 1
    print("[3] Déclencher gyrophare 1...")
    result = controller.declencher_gyrophare(1)
    if result:
        print(f"Commande envoyée ! MID={result.mid}")
    else:
        print("Non connecté")
    print()
    
    # Arrêt propre
    controller.arreter()


# ============================================================
# Diagramme de classe UML - AlarmesMQTT
# ============================================================
#
# Pour générer le diagramme visuel, utilisez le fichier :
# diagramme_classe_alarmes_mqtt.puml avec un outil PlantUML
#
#   +-----------------------------------+
#   |       AlarmesMQTT                  |
#   +-----------------------------------+
#   | - connected: bool                  |
#   | - client: mqtt.Client              |
#   +-----------------------------------+
#   | + __init__(config_bdd, config_mqtt)|
#   | + declencher_gyrophare(numero_gyrophare): result |
#   | + demarrer()                       |
#   | + arreter()                        |
#   +-----------------------------------+
#   | utilise                           |
#   |   - mqtt.Client                    |
#   +-----------------------------------+
#
# ============================================================
