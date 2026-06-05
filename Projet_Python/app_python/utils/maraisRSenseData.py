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