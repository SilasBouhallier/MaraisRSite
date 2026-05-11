from configparser import ConfigParser, NoSectionError
import os
import logging
from .controleur import ControleurMQTT
from .maraisRSenseData import MaraisRSenseData
from .envoie_seuils import EnvoiSeuils


class Application:
    def __init__(self, fichier_config):
        # Logger
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.parser = ConfigParser()

        try:
            # Gestion du chemin
            if not os.path.isabs(fichier_config):
                fichier_config = os.path.abspath(
                    os.path.join(os.path.dirname(__file__), '..', fichier_config)
                )

            if not os.path.exists(fichier_config):
                raise FileNotFoundError(f"Fichier config introuvable : {fichier_config}")

            self.parser.read(fichier_config)
            self.logger.info(f"Config chargée : {fichier_config}")

            # Chargement configs
            config_mqtt = self._get_config('MQTT')
            config_bdd = self._get_config('BDD')

            # Initialisation des modules
            self.controleur = ControleurMQTT(config_mqtt, config_bdd)
            self.mqtt = MaraisRSenseData(config_mqtt, self.controleur)
            self.envoi_seuils = EnvoiSeuils(config_bdd, config_mqtt)

            self.logger.info("Application initialisée")

        except Exception as e:
            self.logger.error(f"Erreur init : {e}")
            raise

    def _substituer_env(self, value):
        """Remplace les ${VAR} par les variables d'environnement."""
        while "${" in value:
            debut = value.find("${")
            fin = value.find("}", debut)
            if fin == -1:
                break

            var = value[debut+2:fin]
            env_value = os.getenv(var)

            if env_value is None:
                self.logger.warning(f"Variable d'env non trouvée : {var}")
                env_value = "${" + var + "}"

            value = value.replace("${" + var + "}", env_value)

        return value

    def _get_config(self, section):
        """Récupère une section avec substitution."""
        try:
            return {
                k: self._substituer_env(v)
                for k, v in self.parser.items(section)
            }
        except NoSectionError:
            self.logger.error(f"Section manquante : {section}")
            raise

    def start(self):
        self.envoi_seuils.demarrer()
        self.mqtt.start()

    def stop(self):
        self.logger.info("Arrêt")
        self.envoi_seuils.arreter()
        self.mqtt.stop()