import sys
import os

# Gestion de l'import pour fonctionner en module ou directement
try:
    from .sql import DatabaseManager
    from .traitement_donnees import TraitementDonnees
except ImportError:
    from sql import DatabaseManager
    from traitement_donnees import TraitementDonnees


class ControleurMQTT:
    def __init__(self, config_MQTT, config_BDD):
        self.config_MQTT = config_MQTT
        self.config_BDD = config_BDD
        self.db = DatabaseManager(config_BDD)

    def traiter(self, topic, message):
        # Extraire MAC depuis le topic
        mac_from_topic = TraitementDonnees.extraire_mac(topic)
        # Extraire données depuis le message JSON
        mesures, timestamp, mac_from_json = TraitementDonnees.extraire_donnees(message)

        if mesures is None or len(mesures) == 0:
            print("Données invalides, message ignoré")
            return

        # Utiliser le MAC du JSON si présent, sinon celui du topic
        mac = mac_from_json if mac_from_json else mac_from_topic
        if not mac:
            print("MAC non trouvé, message ignoré")
            return

        # Affichage structuré
        print("===== Données extraites de la trame MQTT =====")
        print(f"Adresse MAC     : {mac}")
        print(f"Timestamp       : {timestamp}")
        print("Mesures :")
        for mesure in mesures:
            for nom_type, valeur in mesure.items():
                print(f"  {nom_type} : {valeur}")
                # Insérer directement dans la BDD via DatabaseManager
                success = self.db.ajouter_mesure_automatique(
                    valeur=float(valeur),
                    date_heure=timestamp,
                    nom_sonde=mac,
                    nom_type_mesure=nom_type
                )
                if success is not False:
                    print(f"  ✓ Inséré: {nom_type}={valeur}")
                else:
                    print(f"  ✗ Erreur: {nom_type}={valeur}")
        print("=============================================\n")