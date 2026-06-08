# maraisRSenseData.py
# Auteur : [Sejourne Antoine]
# BTS CIEL 2ème année - Projet Marais R Site
# Client MQTT : reçoit les messages des sondes et les transmet au contrôleur pour traitement




"""
Module maraisRSenseData.py - Client MQTT pour la réception des données des sondes.
"""
import os
import ssl
import paho.mqtt.client as mqtt


class MaraisRSenseData:
    """
    Client MQTT :
    - se connecte au broker
    - s'abonne aux topics des sondes
    - transmet les messages au contrôleur
    """

    def __init__(self, configuration, controleur=None):
        self.broker     = configuration["broker"]
        self.port       = int(configuration["port"])
        self.topics     = configuration["topics_sonde"]
        self.username   = configuration.get("username")
        self.password   = configuration.get("password")
        self.controleur = controleur

        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)

        if self.port == 8883:
            self._configurer_tls()

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def _configurer_tls(self):
        """
        Cherche le CA dans l'ordre :
        1. /app/certs/ca.crt       (Docker)
        2. ../certs/ca.crt         (local, relatif à utils/)
        3. Variable d'env MQTT_CA_CERT
        4. Fallback sans vérification
        """
        chemins_candidats = [
            "/app/certs/ca.crt",
            os.path.normpath(os.path.join(
                os.path.dirname(os.path.abspath(__file__)), '..', 'certs', 'ca.crt'
            )),
            os.getenv("MQTT_CA_CERT", ""),
        ]

        ca_path = None
        for chemin in chemins_candidats:
            if chemin and os.path.exists(chemin):
                ca_path = chemin
                break

        if ca_path:
            self.client.tls_set(ca_certs=ca_path)
            print(f"[TLS] OK - certificat : {ca_path}")
        else:
            print("[TLS] CA introuvable, connexion sans vérification")
            self.client.tls_set(cert_reqs=ssl.CERT_NONE)
            self.client.tls_insecure_set(True)

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"[MQTT] Connecté à {self.broker}:{self.port}")
            client.subscribe(self.topics)
            print(f"[MQTT] Abonné au topic : {self.topics}")
        else:
            print(f"[MQTT] Erreur connexion, code : {rc}")

    def on_message(self, client, userdata, msg):
        message = msg.payload.decode(errors="ignore")
        print(f"[MQTT] {msg.topic} -> {message[:100]}")
        if self.controleur:
            self.controleur.traiter(msg.topic, message)
        else:
            print("[MQTT] Aucun contrôleur défini")

    def start(self):
        print(f"[MQTT] Connexion à {self.broker}:{self.port} ...")
        self.client.connect(self.broker, self.port, keepalive=60)
        self.client.loop_forever()

    def stop(self):
        print("[MQTT] Déconnexion ...")
        self.client.loop_stop()
        self.client.disconnect()


if __name__ == "__main__":
    """
    Test direct du module : python utils/maraisRSenseData.py
    
    Ce bloc permet de tester la connexion au broker MQTT et la réception
    des messages des sondes sans lancer l'application complète.
    """
    import time
    import re
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
    
    try:
        # [1] Affichage des paramètres de connexion
        print("[1] Paramètres de connexion :")
        print(f"    - Broker : {config_mqtt.get('broker')}")
        print(f"    - Port : {config_mqtt.get('port')}")
        print(f"    - Topics : {config_mqtt.get('topics_sonde')}")
        print()
        
        # [2] Initialisation du client MQTT (sans contrôleur)
        print("[2] Initialisation du client MQTT...")
        client = MaraisRSenseData(config_mqtt, controleur=None)
        print("    ✓ Client créé avec succès")
        print()
        
        # [3] Information sur la configuration TLS
        print("[3] Configuration TLS :")
        if int(config_mqtt.get('port')) == 8883:
            print("    - Mode TLS/SSL activé (port 8883)")
        else:
            print("    - Mode TLS/SSL désactivé")
        print()
        
        # [4] Tentative de connexion (30 secondes max)
        print("[4] Connexion au broker...")
        print("    (Ctrl+C pour arrêter)")
        print()
        
        # Start dans un thread pour pouvoir contrôler le timeout
        import threading
        thread = threading.Thread(target=client.start, daemon=True)
        thread.start()
        
        # Attente de 30 secondes ou jusqu'à Ctrl+C
        try:
            for i in range(30):
                time.sleep(1)
                if i % 5 == 0 and i > 0:
                    print(f"    ⏱ Écoute en cours... ({i}s)")
        except KeyboardInterrupt:
            print("\n    ⚠ Arrêt demandé par l'utilisateur")
        
        # [5] Arrêt du client
        print()
        print("[5] Arrêt du client...")
        client.stop()
        time.sleep(1)
        print("    ✓ Client arrêté proprement")
        print()
        
        print("✓ Test terminé avec succès !")
        
    except Exception as e:
        print(f"✗ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc()


# ============================================================
# Diagramme de classe UML - MaraisRSenseData
# ============================================================
#
# Pour générer le diagramme visuel, utilisez un outil PlantUML
#
#   +------------------------------------------------+
#   |         MaraisRSenseData                       |
#   +------------------------------------------------+
#   | - broker: str                                  |
#   | - port: int                                    |
#   | - topics: str                                  |
#   | - username: str                                |
#   | - password: str                                |
#   | - controleur: ControleurMQTT                   |
#   | - client: mqtt.Client                          |
#   +------------------------------------------------+
#   | + __init__(configuration: dict, controleur)   |
#   | + start(): void                                |
#   | + stop(): void                                 |
#   | + on_connect(client, userdata, flags, rc)     |
#   | + on_message(client, userdata, msg)           |
#   | - _configurer_tls(): void                      |
#   +------------------------------------------------+
#   |            Dépendances                         |
#   +------------------------------------------------+
#   |   MaraisRSenseData  ------>  mqtt.Client      |
#   |   MaraisRSenseData  ------>  ControleurMQTT   |
#   |   MaraisRSenseData  ------>  ssl              |
#   +------------------------------------------------+
#
# ============================================================