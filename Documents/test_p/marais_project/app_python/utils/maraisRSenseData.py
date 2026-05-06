import paho.mqtt.client as mqtt


class MaraisRSenseData:
    def __init__(self, configuration, controleur = None):
        self.broker = configuration["broker"]
        self.port = int(configuration["port"])
        self.topics = configuration["topics_sonde"]
        self.controleur = controleur
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)

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



# if __name__ == "__main__":
#     broker = "localhost"
#     port = 1883
#     topics = ["test/topic", "sensor/data"]
    
#     # Create and start subscriber
#     subscriber = Subscriber(broker, port, topics)
    
#     try:
#         subscriber.start()
#     except KeyboardInterrupt:
#         print("\nArrêt du subscriber...")
#     except Exception as e:
#         print(f"Erreur: {e}")

