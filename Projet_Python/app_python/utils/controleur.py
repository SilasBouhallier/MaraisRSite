# controleur.py
# Auteur : [Sejourne Antoine]
# BTS CIEL 2ème année - Projet Marais R Site
# Contrôleur MQTT : reçoit les messages, extrait les données et les stocke en BDD

import sys
import os

# Ce bloc permet d'importer les modules que ce soit en mode "package" ou en mode script direct
# En mode package (import depuis application.py) : on utilise les imports relatifs (.sql)
# En mode script direct (python controleur.py) : on utilise les imports simples
try:
    from .sql import DatabaseManager
    from .traitement_donnees import TraitementDonnees
    from .alarmes_mqtt import AlarmesMQTT
except ImportError:
    from sql import DatabaseManager
    from traitement_donnees import TraitementDonnees
    from alarmes_mqtt import AlarmesMQTT


class ControleurMQTT:
    """
    Reçoit les messages MQTT et orchestre leur traitement :
    extraction de l'adresse MAC, parsing JSON, insertion en base de données.
    """

    def __init__(self, config_mqtt, config_bdd):
        # On sauvegarde les configurations pour une utilisation future si besoin
        self.config_mqtt = config_mqtt
        self.config_bdd  = config_bdd

        # Création du gestionnaire de base de données avec la config fournie
        self.db = DatabaseManager(config_bdd)
        print("Contrôleur MQTT initialisé")


    def declencher_gyrophare_automatique(self, numero_gyrophare=1):
        """
        Déclenche automatiquement le gyrophare via MQTT quand un seuil est dépassé.
        """
        try:
            # Création de l'instance AlarmesMQTT
            controller = AlarmesMQTT(self.config_bdd, self.config_mqtt)
            controller.demarrer()

            # Déclenchement du gyrophare
            result = controller.declencher_gyrophare(numero_gyrophare)

            # Arrêt
            controller.arreter()

            if result:
                print(f"[ALERTE] Gyrophare {numero_gyrophare} déclenché automatiquement, MID={result.mid}")
            else:
                print("[ERREUR] Échec du déclenchement automatique du gyrophare")

        except Exception as e:
            print(f"[ERREUR] Impossible de déclencher le gyrophare automatiquement: {e}")


    def traiter(self, topic, message):
        """
        Traite un message MQTT reçu depuis une sonde.
        Étapes : extraction MAC → parsing JSON → insertion BDD pour chaque mesure.

        Args:
            topic   : le topic MQTT (ex: "marais/sondes/AA:BB:CC:DD:EE:FF")
            message : le contenu du message au format JSON
        """
        # Étape 1 : on essaie d'extraire l'adresse MAC depuis le topic MQTT
        mac_topic = TraitementDonnees.extraire_mac(topic)

        # Étape 2 : on parse le JSON pour récupérer les mesures, l'horodatage et le MAC
        mesures, timestamp, mac_json = TraitementDonnees.extraire_donnees(message)

        # Vérification : si aucune mesure n'a été extraite, on abandonne
        if not mesures:
            print("[WARN] Aucune mesure extraite, message ignoré")
            return

        # On privilégie le MAC présent dans le JSON, sinon on prend celui du topic
        mac = mac_json if mac_json else mac_topic
        if not mac:
            print("[WARN] Adresse MAC introuvable, message ignoré")
            return

        # Affichage des données reçues pour vérification (utile en débogage)
        print("===== Données extraites de la trame MQTT =====")
        print(f"  MAC       : {mac}")
        print(f"  Timestamp : {timestamp}")
        print(f"  Mesures   :")

        # Étape 3 : on insère chaque mesure une par une dans la base de données
        for mesure in mesures:
            for nom_type, valeur in mesure.items():
                print(f"    {nom_type} = {valeur}")

                # La méthode ajouter_mesure_automatique gère elle-même la
                # recherche des IDs (emplacement, type de mesure, seuils d'alerte)
                succes = self.db.ajouter_mesure_automatique(
                    valeur          = float(valeur),
                    date_heure      = timestamp,
                    nom_sonde       = mac,
                    nom_type_mesure = nom_type
                )

                # On affiche si l'insertion s'est bien passée ou non
                if succes is not False:
                    print(f" {nom_type} = {valeur} inséré en BDD")

                    # Vérification du niveau d'alerte après l'insertion
                    id_alerte = self.db.determiner_id_alerte(
                        valeur=float(valeur),
                        nom_type_mesure=nom_type
                    )

                    # Si alerte (ATTENTION ou DANGER), déclencher le gyrophare automatiquement
                    if id_alerte in [2, 3]:  # ATTENTION (id=2) ou DANGER (id=3)
                        niveau = "ATTENTION" if id_alerte == 2 else "DANGER"
                        print(f"[ALERTE] Seuil {niveau} dépassé pour {nom_type}={valeur} !")

                        # Trouver l'alarme (gyrophare) assignée à la même emplacement que la sonde
                        mac_alarme = self.db.trouver_alarme_par_sonde(mac)
                        if mac_alarme:
                            # Trouver l'ID de l'alarme à partir de son adresse MAC
                            id_alarme = self.db.trouver_id_alarme_par_mac(mac_alarme)
                            if id_alarme:
                                print(f"[INFO] Déclenchement de l'alarme #{id_alarme} (MAC: {mac_alarme}) pour la sonde {mac}")
                                self.declencher_gyrophare_automatique(numero_gyrophare=id_alarme)
                            else:
                                print(f"[ERREUR] ID de l'alarme non trouvé pour MAC: {mac_alarme}")
                        else:
                            print(f"[ERREUR] Aucune alarme assignée à l'emplacement de la sonde: {mac}")
                else:
                    print(f"Impossible d'insérer {nom_type} = {valeur}")


# ============================================================
# Diagramme de classe UML - ControleurMQTT
# ============================================================
#
#   +-----------------------------------+
#   |       ControleurMQTT               |
#   +-----------------------------------+
#   | - config_mqtt: dict                |
#   | - config_bdd: dict                 |
#   | - db: DatabaseManager              |
#   +-----------------------------------+
#   | + __init__(config_mqtt, config_bdd)|
#   | + traiter(topic, message)          |
#   +-----------------------------------+
#   | utilise                           |
#   |   - DatabaseManager                |
#   |   - TraitementDonnees              |
#   +-----------------------------------+
#
# ============================================================

if __name__ == "__main__":
    """
    Test direct de la classe ControleurMQTT.
    """
    import os
    from dotenv import load_dotenv
    from configparser import ConfigParser

    # Chargement de la configuration
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', '.env'))
    
    parser = ConfigParser()
    parser.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'utils', 'configuration.cfg'))
    
    config_mqtt = {k: v for k, v in parser['MQTT'].items()}
    config_bdd = {k: v for k, v in parser['BDD'].items()}
    
    # Test du contrôleur
    controleur = ControleurMQTT(config_mqtt, config_bdd)
    
    # Test de traitement d'un message
    test_topic = "marais/sondes/62:03:57:41:38:23"
    test_message = '{"timestamp":"2026-06-03T10:00:00","mesure":[{"ECO2":1200,"TVOC":100}]}'
    controleur.traiter(test_topic, test_message)
