# sql.py
# Auteur : [Sejourne Antoine]
# BTS CIEL 2ème année - Projet Marais R Site
# Gestionnaire de base de données MariaDB




"""
Module sql.py - Gestionnaire de base de données MariaDB.

Ce module définit la classe DatabaseManager qui gère toutes les interactions
avec la base de données MariaDB 'Marais_R_Site'. Elle permet :
- La connexion à la base de données
- L'insertion des mesures
- La gestion des alertes selon les seuils configurés
- La résolution des IDs (emplacement, type de mesure)
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

class DatabaseManager:
    """
    Gestionnaire des interactions avec la base de données MariaDB.
    
    Cette classe gère :
    - La connexion à la base de données avec fallback sur variables d'env
    - L'insertion des mesures avec détermination automatique des IDs
    - La gestion des niveaux d'alerte selon les seuils
    - La résolution des identifiants (emplacement, type de mesure)
    """

    def __init__(self, config_bdd=None):
        """
        Initialise le gestionnaire de base de données.
        
        L'ordre de priorité pour la configuration est :
        1. Paramètre config_bdd passé directement
        2. Variables d'environnement Docker (MYSQL_MQTT_*)
        3. Variables d'environnement standard (MYSQL_*)
        
        Args:
            config_bdd: Dictionnaire de configuration optionnel
        """
        # Priorité 1: Config passée directement
        if config_bdd:
            self.__host = config_bdd.get('host', 'localhost')
            self.__port = int(config_bdd.get('port', '3306'))
            self.__database = config_bdd.get('database', 'Marais_R_Site')
            self.__user = config_bdd.get('user')
            self.__password = config_bdd.get('password')
        # Priorité 2: Variables d'environnement Docker
        elif os.getenv('MYSQL_MQTT_HOST'):
            self.__host = os.getenv('MYSQL_MQTT_HOST')
            self.__port = int(os.getenv('MYSQL_MQTT_PORT', '3306'))
            self.__database = os.getenv('MYSQL_MQTT_DATABASE', 'Marais_R_Site')
            self.__user = os.getenv('MYSQL_MQTT_USER')
            self.__password = os.getenv('MYSQL_MQTT_PASSWORD')
        # Priorité 3: .env
        else:
            load_dotenv()
            self.__host = os.getenv('MYSQL_HOST', 'localhost')
            self.__port = int(os.getenv('MYSQL_PORT', '3306'))
            self.__database = os.getenv('MYSQL_DATABASE', 'Marais_R_Site')
            self.__user = os.getenv('MYSQL_USER')
            self.__password = os.getenv('MYSQL_PASSWORD')

    def __creer_connexion(self):
        """
        Crée et retourne une connexion à la base de données.
        
        Returns:
            Objet connexion mysql.connector
        """
        return mysql.connector.connect(
            host=self.__host,
            port=self.__port,
            database=self.__database,
            user=self.__user,
            password=self.__password
        )

    def trouver_id_emplacement_par_sonde(self, nom_sonde):
        """
        Retourne l'id_emplacement via la jointure avec la table sonde.

        Recherche l'emplacement associé à une sonde par son nom (MAC).

        Args:
            nom_sonde: Nom de la sonde (généralement l'adresse MAC)

        Returns:
            L'ID de l'emplacement ou None si non trouvé
        """
        conn = None
        try:
            conn = self.__creer_connexion()
            cursor = conn.cursor()
            # Jointure entre emplacement et sonde pour trouver l'ID
            query = """
                SELECT e.id_emplacement
                FROM emplacement e
                JOIN sonde s ON e.id_sonde = s.id_sonde
                WHERE s.nom_sonde = %s
            """
            cursor.execute(query, (nom_sonde,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            print(f"Erreur recherche emplacement : {e}")
            return None
        finally:
            # Fermeture propre de la connexion
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def trouver_alarme_par_sonde(self, nom_sonde):
        """
        Retourne l'adresse MAC de l'alarme (gyrophare) assignée à la même emplacement que la sonde.

        Recherche l'alarme associée à l'emplacement de la sonde.

        Args:
            nom_sonde: Nom de la sonde (adresse MAC)

        Returns:
            L'adresse MAC de l'alarme ou None si non trouvé
        """
        conn = None
        try:
            conn = self.__creer_connexion()
            cursor = conn.cursor()
            # Jointure entre sonde, emplacement et alarme pour trouver l'alarme
            query = """
                SELECT a.nom_alarme
                FROM sonde s
                JOIN emplacement e ON s.id_sonde = e.id_sonde
                JOIN alarme a ON e.id_emplacement = a.id_emplacement
                WHERE s.nom_sonde = %s
            """
            cursor.execute(query, (nom_sonde,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            print(f"Erreur recherche alarme : {e}")
            return None
        finally:
            # Fermeture propre de la connexion
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def trouver_id_alarme_par_mac(self, mac_alarme):
        """
        Retourne l'ID de l'alarme à partir de son adresse MAC.

        Args:
            mac_alarme: Adresse MAC de l'alarme

        Returns:
            L'ID de l'alarme ou None si non trouvé
        """
        conn = None
        try:
            conn = self.__creer_connexion()
            cursor = conn.cursor()
            # Recherche de l'ID de l'alarme par adresse MAC
            query = """
                SELECT id_alarme
                FROM alarme
                WHERE nom_alarme = %s
            """
            cursor.execute(query, (mac_alarme,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Error as e:
            print(f"Erreur recherche ID alarme : {e}")
            return None
        finally:
            # Fermeture propre de la connexion
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def trouver_id_type_mesure(self, nom_type_mesure):
        """
        Retourne l'ID du type de mesure (CO2, Température, etc.).
        
        Args:
            nom_type_mesure: Nom du type de mesure
            
        Returns:
            L'ID du type de mesure ou 1 (défaut) si non trouvé
        """
        conn = None
        try:
            conn = self.__creer_connexion()
            cursor = conn.cursor()
            query = "SELECT id_type_mesure FROM type_info_mesure WHERE nom_type_mesure = %s"
            cursor.execute(query, (nom_type_mesure,))
            result = cursor.fetchone()
            return result[0] if result else 1  # 1 = type par défaut
        except Error as e:
            print(f"Erreur recherche type mesure : {e}")
            return 1
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def determiner_id_alerte(self, valeur, nom_type_mesure):
        """
        Détermine le niveau d'alerte selon les seuils configurés.
        
        IDs d'alerte :
        - 1: Normal (nom_alerte est NULL)
        - 2: Attention (valeur >= seuil alerte)
        - 3: Danger (valeur >= seuil danger)
        
        Args:
            valeur: Valeur numérique de la mesure
            nom_type_mesure: Type de mesure pour récupérer les seuils
            
        Returns:
            ID du niveau d'alerte (1, 2 ou 3)
        """
        conn = None
        try:
            conn = self.__creer_connexion()
            cursor = conn.cursor(dictionary=True)
            # Récupération des seuils pour ce type de mesure
            query = "SELECT valeur_alerte_seuil, valeur_danger_seuil FROM type_info_mesure WHERE nom_type_mesure = %s"
            cursor.execute(query, (nom_type_mesure,))
            seuils = cursor.fetchone()
            
            # Si pas de seuils configurés, retourner Normal
            if not seuils:
                return 1

            # Détermination du niveau d'alerte
            if valeur >= seuils['valeur_danger_seuil']:
                return 3  # Danger
            elif valeur >= seuils['valeur_alerte_seuil']:
                return 2  # Attention
            else:
                return 1  # Normal
        except Error as e:
            print(f"Erreur détermination alerte : {e}")
            return 1  # En cas d'erreur, considérer comme Normal
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def ajouter_mesure_automatique(self, valeur, date_heure, nom_sonde, nom_type_mesure):
        """
        Ajoute une mesure avec détermination automatique des IDs.
        
        Cette méthode orchestre :
        1. Recherche de l'emplacement via la sonde
        2. Détermination du niveau d'alerte selon les seuils
        3. Résolution du type de mesure
        4. Insertion dans la table mesure
        
        Args:
            valeur: Valeur de la mesure (numérique)
            date_heure: Timestamp de la mesure
            nom_sonde: Identifiant de la sonde (MAC)
            nom_type_mesure: Type de la mesure (CO2, Température, etc.)
            
        Returns:
            True si insertion réussie, False sinon
        """
        # Résolution des IDs nécessaires
        id_emplacement = self.trouver_id_emplacement_par_sonde(nom_sonde)
        if id_emplacement is None:
            print(f"Erreur : La sonde '{nom_sonde}' n'a pas d'emplacement associé.")
            return False

        id_alerte = self.determiner_id_alerte(valeur, nom_type_mesure)
        id_type_mesure = self.trouver_id_type_mesure(nom_type_mesure)
        
        # Insertion finale
        return self.ajouter_mesure(valeur, date_heure, id_emplacement, id_alerte, id_type_mesure)

    def ajouter_mesure(self, valeur, date_heure, id_emplacement, id_alerte, id_type_mesure):
        """
        Insère une mesure dans la table 'mesure'.
        
        Args:
            valeur: Valeur numérique de la mesure
            date_heure: Timestamp de la mesure
            id_emplacement: ID de l'emplacement
            id_alerte: ID du niveau d'alerte
            id_type_mesure: ID du type de mesure
            
        Returns:
            True si insertion réussie, False sinon
        """
        conn = None
        try:
            conn = self.__creer_connexion()
            cursor = conn.cursor()
            # Requête d'insertion avec tous les champs nécessaires (uniquement la date, sans l'heure)
            query = """
                INSERT INTO mesure (valeur_mesure, date_heure_mesure, id_emplacement, id_alerte, id_type_mesure)
                VALUES (%s, NOW(), %s, %s, %s)
            """
            cursor.execute(query, (valeur, id_emplacement, id_alerte, id_type_mesure))
            conn.commit()
            return True
        except Error as e:
            print(f"Erreur insertion SQL : {e}")
            return False
        finally:
            # Fermeture propre des ressources
            if conn and conn.is_connected():
                cursor.close()
                conn.close()


# ============================================================
# Diagramme de classe UML - DatabaseManager
# ============================================================
#
#   +-----------------------------------+
#   |       DatabaseManager              |
#   +-----------------------------------+
#   | - __host: str                      |
#   | - __port: int                      |
#   | - __database: str                  |
#   | - __user: str                      |
#   | - __password: str                  |
#   +-----------------------------------+
#   | + __init__(config_bdd)             |
#   | + trouver_id_emplacement_par_sonde(nom_sonde): int |
#   | + trouver_id_type_mesure(nom_type_mesure): int |
#   | + determiner_id_alerte(valeur, nom_type_mesure): int |
#   | + ajouter_mesure_automatique(valeur, date_heure, nom_sonde, nom_type_mesure): bool |
#   | + ajouter_mesure(valeur, date_heure, id_emplacement, id_alerte, id_type_mesure): bool |
#   | - __creer_connexion(): Connection   |
#   | - _lire_section(section): dict      |
#   | - _remplacer_variables_env(valeur): str |
#   +-----------------------------------+
#
# ============================================================

if __name__ == "__main__":
    """
    Test direct de la classe DatabaseManager.
    """
    import os
    from dotenv import load_dotenv
    from configparser import ConfigParser

    # Chargement de la configuration
    load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..', '.env'))
    
    parser = ConfigParser()
    parser.read(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'utils', 'configuration.cfg'))
    
    config_bdd = {k: v for k, v in parser['BDD'].items()}
    
    # Test du gestionnaire de base de données
    db = DatabaseManager(config_bdd)
    print("DatabaseManager initialisé")
    
    # Test de recherche d'emplacement
    id_emplacement = db.trouver_id_emplacement_par_sonde("62:03:57:41:38:23")
    print(f"ID emplacement pour la sonde: {id_emplacement}")
