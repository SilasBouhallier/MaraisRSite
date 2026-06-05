# application.py
# Auteur : [Sejourne Antoine]
# BTS CIEL 2ème année - Projet Marais R Site
# application principale : charge la config, initialise les modules et démarre tout


from configparser import ConfigParser, NoSectionError
import os
import logging

try:
    from .controleur import ControleurMQTT
    from .maraisRSenseData import MaraisRSenseData
except ImportError:
    from controleur import ControleurMQTT
    from maraisRSenseData import MaraisRSenseData


class Application:
    """
    Classe principale de l'application.
    Elle charge la config, initialise les modules et démarre tout.
    """

    def __init__(self, fichier_config):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.parser = ConfigParser()

        if not os.path.isabs(fichier_config):
            fichier_config = os.path.abspath(
                os.path.join(os.path.dirname(__file__), '..', fichier_config)
            )

        if not os.path.exists(fichier_config):
            self.logger.error(f"Fichier introuvable : {fichier_config}")
            raise FileNotFoundError(f"Fichier introuvable : {fichier_config}")

        self.parser.read(fichier_config)
        self.logger.info(f"Config chargée depuis : {fichier_config}")

        config_mqtt = self._lire_section('MQTT')
        config_bdd  = self._lire_section('BDD')

        self.controleur = ControleurMQTT(config_mqtt, config_bdd)
        self.mqtt       = MaraisRSenseData(config_mqtt, self.controleur)

        self.logger.info("Tous les modules sont initialisés")

    def _remplacer_variables_env(self, valeur):
        while "${" in valeur:
            debut = valeur.find("${")
            fin   = valeur.find("}", debut)
            if fin == -1:
                break
            nom_var = valeur[debut + 2:fin]
            contenu = os.getenv(nom_var)
            if contenu is None:
                self.logger.warning(f"Variable d'environnement non trouvée : {nom_var}")
                contenu = "${" + nom_var + "}"
            valeur = valeur.replace("${" + nom_var + "}", contenu)
        return valeur

    def _lire_section(self, section):
        try:
            return {
                cle: self._remplacer_variables_env(valeur)
                for cle, valeur in self.parser.items(section)
            }
        except NoSectionError:
            self.logger.error(f"Section '{section}' absente du fichier de config")
            raise

    def start(self):
        self.logger.info("Démarrage de l'application...")
        self.mqtt.start()

    def stop(self):
        self.logger.info("Arrêt en cours...")
        self.mqtt.stop()
