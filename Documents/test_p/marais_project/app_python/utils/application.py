
from configparser import ConfigParser
import os
from .controleur import ControleurMQTT
from .maraisRSenseData import MaraisRSenseData


class Application:
    def __init__(self,fichier_config):
        parser = ConfigParser()
        # Convertir en chemin absolu si relatif
        if not os.path.isabs(fichier_config):
            fichier_config = os.path.join(os.path.dirname(__file__), '..', fichier_config)
            fichier_config = os.path.abspath(fichier_config)
        parser.read(fichier_config)
        
        # Fonction pour substituer les variables ${VAR} par les valeurs d'environnement
        def substituer_env(section):
            result = {}
            for key, value in parser.items(section):
                import re
                def remplacer(match):
                    var_name = match.group(1)
                    env_value = os.getenv(var_name)
                    # Garder la valeur d'environnement telle quelle (mosquitto ou autre)
                    if env_value:
                        return env_value
                    # Sinon retourner la valeur telle quelle
                    return match.group(0)
                result[key] = re.sub(r'\$\{([^}]+)\}', remplacer, value)
            return result
        
        config_mqtt = substituer_env('MQTT')
        config_bdd = substituer_env('BDD')
        
        self.controleur = ControleurMQTT(config_mqtt, config_bdd)
        self.mqtt = MaraisRSenseData(config_mqtt, self.controleur)
    
    def start(self):
        self.mqtt.start()
        


    
    def stop(self):
        self.mqtt.stop()
  