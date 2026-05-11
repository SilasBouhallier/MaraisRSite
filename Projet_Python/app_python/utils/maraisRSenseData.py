import paho.mqtt.client as mqtt


class MaraisRSenseData:
    def __init__(self, configuration, controleur = None):
        self.broker = configuration["broker"]
        self.port = int(configuration["port"])
        self.topics = configuration["topics_sonde"]
        self.username = configuration.get("username")
        self.password = configuration.get("password")
        self.controleur = controleur
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

        # Authentification si credentials présents
        if self.username and self.password:
            self.client.username_pw_set(self.username, self.password)
        
        # TLS si port 8883
        if self.port == 8883:
            import os
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            self.client.tls_set(
                ca_certs=os.path.join(base_dir, "mosquitto/config/ca.crt"),
                certfile=os.path.join(base_dir, "mosquitto/config/server.crt"),
                keyfile=os.path.join(base_dir, "mosquitto/config/server.key")
            )
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Connecté au broker {self.broker}:{self.port}")
            print(f"Abonné au topic : {self.topics}")
            print(f"Code de retour : {rc}")

        
            client.subscribe(self.topics)
            
        else:
            print(f"Erreur connexion : {rc}")


    def on_message(self, client, userdata, msg):
        message = msg.payload.decode()
        print(f"[REÇU {msg.topic}] {message[:100]}...")
        
        # Envoie le message au contrôleur si disponible
        if self.controleur:
            self.controleur.traiter(msg.topic, message)
        else:
            print("[WARN] Pas de contrôleur défini")

    def start(self):
        print("Connexion au broker...")
        print (self.broker)
        self.client.connect(self.broker, self.port, 60)
        self.client.loop_forever()

    def stop(self):
        """Arrête proprement le client MQTT."""
        self.client.loop_stop()
        self.client.disconnect()


