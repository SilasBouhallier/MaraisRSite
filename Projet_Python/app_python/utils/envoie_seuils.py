"""Service FT6 : Publication des seuils via MQTT."""

import paho.mqtt.client as mqtt
import json
import time
import ssl


class EnvoiSeuils:
    """Publisher MQTT des seuils vers les sondes."""

    def __init__(self, config_bdd, config_mqtt):
        cfg = config_mqtt
        self.topic = cfg.get('topics_sonde', '').replace('/#', '') + '/seuils'
        self.client = mqtt.Client(
            callback_api_version=mqtt.CallbackAPIVersion.VERSION1,
            client_id="marais_seuils_publisher"
        )
        self.client.on_connect = lambda c, u, f, rc: setattr(self, 'connected', rc == 0)
        self.client.on_disconnect = lambda c, u, rc: setattr(self, 'connected', False)
        if cfg.get('username') and cfg.get('password'):
            self.client.username_pw_set(cfg['username'], cfg['password'])
        if int(cfg.get('port', 1883)) == 8883:
            self.client.tls_set(cert_reqs=ssl.CERT_NONE)
        self.client.connect(cfg.get('broker'), int(cfg.get('port')), 60)
        self.client.loop_start()
        time.sleep(0.5)

    def publier(self, payload):
        """Publie un message JSON sur le topic seuils."""
        if not getattr(self, 'connected', False):
            return None
        return self.client.publish(self.topic, json.dumps(payload, separators=(',', ':')), qos=1, retain=True)

    def demarrer(self):
        """Démarrage (compatibilité application.py)."""
        pass

    def arreter(self):
        """Arrêt (compatibilité application.py)."""
        self.client.loop_stop()


if __name__ == "__main__":
    """Test direct: python utils/envoie_seuils.py"""
    import os
    import re
    import sys
    from dotenv import load_dotenv
    from configparser import ConfigParser
    
    # Déterminer le chemin de base (remonter de 2 niveaux: utils/ -> app_python/)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Charger .env (au même niveau que app_python/)
    load_dotenv(os.path.join(base_dir, '.env'))
    
    def subst(v):
        if not v:
            return v
        return re.sub(r'\$\{([^}]+)\}', lambda m: os.getenv(m.group(1), ''), v).strip()
    
    parser = ConfigParser()
    parser.read(os.path.join(base_dir, 'app_python', 'utils', 'configuration.cfg'))
    
    config_mqtt = {k: subst(v) for k, v in parser['MQTT'].items()}
    config_bdd = {k: subst(v) for k, v in parser['BDD'].items()}
    
   
    print(f"Broker: {config_mqtt.get('broker')}")
    print(f"Port: {config_mqtt.get('port')}")
    print(f"Topic: marais/sondes/seuils")
    print()
    
    print("[1] Connexion...")
    publisher = EnvoiSeuils(config_bdd, config_mqtt)
    print()
    result = publisher.publier({
        "Seuils": {"valeur_alerte_seuil": 150.0, "valeur_danger_seuil": 200.0}
    })
    if result:
        print(f"Publié ! MID={result.mid}")
    else:
        print("❌ Non connecté")
    print()
    
    import time
    time.sleep(2)
    
    publisher.arreter()