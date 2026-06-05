# envoie_seuils.py
# Auteur : [Antoine Sejourne]
# BTS CIEL 2ème année - Projet Marais R Site
# Service FT6 : publie les seuils d'alerte vers les sondes via MQTT

import paho.mqtt.client as mqtt
import json
import time
import ssl


class EnvoiSeuils:
    """
    Publie les seuils de configuration sur le broker MQTT.
    Les sondes s'y abonnent pour savoir quand déclencher une alerte.
    """

    def __init__(self, config_bdd, config_mqtt):
        # On garde une référence à la config pour l'utiliser dans les méthodes
        self.config = config_mqtt

        # Construction du topic de publication des seuils
        # Exemple : "marais/sondes/#" → "marais/sondes/seuils"
        base_topic  = config_mqtt.get('topics_sonde', '').replace('/#', '')
        self.topic  = base_topic + '/seuils'

        # Indicateur de connexion, mis à jour par les callbacks
        self.connecte = False

        # Création du client MQTT avec un identifiant reconnaissable dans les logs du broker
        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION1,
            client_id="marais_seuils_publisher"
        )

        # On associe nos méthodes aux événements de connexion / déconnexion
        self.client.on_connect    = self.on_connect
        self.client.on_disconnect = self.on_disconnect

        # Si un login est présent dans la config, on l'utilise pour s'authentifier
        if config_mqtt.get('username') and config_mqtt.get('password'):
            self.client.username_pw_set(config_mqtt['username'], config_mqtt['password'])

        # Si le port est 8883, on active le chiffrement TLS (sans vérif de certificat ici)
        if int(config_mqtt.get('port', 1883)) == 8883:
            self.client.tls_set(cert_reqs=ssl.CERT_NONE)
            print("TLS activé (port 8883)")

        # Connexion au broker puis démarrage de la boucle réseau en arrière-plan
        self.client.connect(config_mqtt.get('broker'), int(config_mqtt.get('port')), keepalive=60)
        # self.client.loop_start()

        # Petite pause pour laisser le temps à la connexion de s'établir
        time.sleep(0.5)


    def on_connect(self, client, userdata, flags, rc):
        """Callback appelé quand le client se connecte au broker."""
        if rc == 0:
            self.connecte = True
            print(f"[EnvoiSeuils] Connecté au broker, topic : {self.topic}")
        else:
            self.connecte = False
            print(f"[EnvoiSeuils] Echec de connexion, code : {rc}")


    def on_disconnect(self, client, userdata, rc):
        """Callback appelé quand le client se déconnecte du broker."""
        self.connecte = False
        print("[EnvoiSeuils] Déconnecté du broker")


    def publier(self, payload):
        """
        Publie un dictionnaire de seuils en JSON sur le topic MQTT.

        QoS 1  : le message est garanti d'arriver au moins une fois.
        retain : mis à False ici (le broker ne conserve pas le message pour les nouveaux abonnés).

        Args:
            payload : dictionnaire Python contenant les seuils à envoyer

        Returns:
            Le résultat MQTT (avec .mid pour tracer le message), ou None si pas connecté
        """
        if not self.connecte:
            print("[EnvoiSeuils] Pas connecté, publication annulée")
            return None

        # json.dumps convertit le dict Python en chaîne JSON
        # separators=(',', ':') supprime les espaces pour un JSON compact
        message_json = json.dumps(payload, separators=(',', ':'))

        resultat = self.client.publish(
            self.topic,
            message_json,
            qos=1,
            retain=False
        )
        return resultat


    def demarrer(self):
        """
        Méthode appelée par application.py au démarrage.
        La connexion est déjà faite dans __init__, donc rien à faire ici.
        """
        print("[EnvoiSeuils] Service démarré")


    def arreter(self):
        """Arrête proprement la boucle réseau MQTT."""
        print("[EnvoiSeuils] Arrêt du service...")
        self.client.loop_stop()
        self.client.disconnect()


# ============================================================
# Bloc de test : exécuté uniquement si on lance ce fichier
# directement avec "python envoie_seuils.py"
# (pas exécuté quand importé depuis application.py)
# ============================================================
if __name__ == "__main__":
    import os
    import re
    from dotenv import load_dotenv
    from configparser import ConfigParser

    # On remonte de 2 niveaux pour trouver la racine du projet
    racine = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    # Chargement du fichier .env (contient les mots de passe, IPs, etc.)
    load_dotenv(os.path.join(racine, '.env'))

    def remplacer_variables(valeur):
        """Remplace ${NOM_VAR} par la vraie valeur de la variable d'environnement."""
        if not valeur:
            return valeur
        return re.sub(r'\$\{([^}]+)\}', lambda m: os.getenv(m.group(1), ''), valeur).strip()

    # Lecture du fichier de configuration
    parser = ConfigParser()
    parser.read(os.path.join(racine, 'app_python', 'utils', 'configuration.cfg'))

    config_mqtt = {k: remplacer_variables(v) for k, v in parser['MQTT'].items()}
    config_bdd  = {k: remplacer_variables(v) for k, v in parser['BDD'].items()}

    print(f"Broker : {config_mqtt.get('broker')}")
    print(f"Port   : {config_mqtt.get('port')}")
    print()

    # Test de connexion et de publication
    print("[1] Connexion...")
    publisher = EnvoiSeuils(config_bdd, config_mqtt)

    print("[2] Publication des seuils de test...")
    resultat = publisher.publier({
        "Seuils": {
            "valeur_alerte_seuil": 150.0,
            "valeur_danger_seuil": 200.0
        }
    })

    if resultat:
        print(f"[OK] Message publié, MID = {resultat.mid}")
    else:
        print("[ERREUR] Publication échouée (pas connecté ?)")

    # Arrêt propre du client
    publisher.arreter()


# ============================================================
# Diagramme de classe UML - EnvoiSeuils
# ============================================================
#
#   +-----------------------------------+
#   |       EnvoiSeuils                  |
#   +-----------------------------------+
#   | - config: dict                     |
#   | - topic: str                       |
#   | - connecte: bool                   |
#   | - client: mqtt.Client              |
#   +-----------------------------------+
#   | + __init__(config_bdd, config_mqtt)|
#   | + on_connect(client, userdata, flags, rc) |
#   | + on_disconnect(client, userdata, rc) |
#   | + publier(payload): result         |
#   | + demarrer()                       |
#   | + arreter()                        |
#   +-----------------------------------+
#
# ============================================================
