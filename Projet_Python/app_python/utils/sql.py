import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

class DatabaseManager:
    """
    Gestion des interactions avec la base MariaDB 'Marais_R_Site'.
    """

    def __init__(self, config_bdd=None):
        # Priorité 1: Config passée
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
        return mysql.connector.connect(
            host=self.__host,
            port=self.__port,
            database=self.__database,
            user=self.__user,
            password=self.__password
        )

    def trouver_id_emplacement_par_sonde(self, nom_sonde):
        """Retourne l'id_emplacement via la jointure avec la table sonde"""
        conn = None
        try:
            conn = self.__creer_connexion()
            cursor = conn.cursor()
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
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def trouver_id_type_mesure(self, nom_type_mesure):
        """Retourne l'ID du type de mesure (CO2, Température, etc.)"""
        conn = None
        try:
            conn = self.__creer_connexion()
            cursor = conn.cursor()
            query = "SELECT id_type_mesure FROM type_info_mesure WHERE nom_type_mesure = %s"
            cursor.execute(query, (nom_type_mesure,))
            result = cursor.fetchone()
            return result[0] if result else 1  # 1 par défaut
        except Error as e:
            print(f"Erreur recherche type mesure : {e}")
            return 1
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def determiner_id_alerte(self, valeur, nom_type_mesure):
        """
        Détermine l'id_alerte (1: Normal/NULL, 2: Attention, 3: Danger) 
        selon les seuils de type_info_mesure.
        """
        conn = None
        try:
            conn = self.__creer_connexion()
            cursor = conn.cursor(dictionary=True)
            # Récupération des seuils dans type_info_mesure
            query = "SELECT valeur_alerte_seuil, valeur_danger_seuil FROM type_info_mesure WHERE nom_type_mesure = %s"
            cursor.execute(query, (nom_type_mesure,))
            seuils = cursor.fetchone()
            
            if not seuils:
                return 1 # Normal par défaut

            if valeur >= seuils['valeur_danger_seuil']:
                return 3  # Danger
            elif valeur >= seuils['valeur_alerte_seuil']:
                return 2  # Attention
            else:
                return 1  # Normal (nom_alerte est NULL pour l'ID 1)
        except Error as e:
            print(f"Erreur détermination alerte : {e}")
            return 1
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()

    def ajouter_mesure_automatique(self, valeur, date_heure, nom_sonde, nom_type_mesure):
        id_emplacement = self.trouver_id_emplacement_par_sonde(nom_sonde)
        if id_emplacement is None:
            print(f"Erreur : Sonde '{nom_sonde}' non reconnue.")
            return False

        id_alerte = self.determiner_id_alerte(valeur, nom_type_mesure)
        id_type_mesure = self.trouver_id_type_mesure(nom_type_mesure)
        
        return self.ajouter_mesure(valeur, date_heure, id_emplacement, id_alerte, id_type_mesure)

    def ajouter_mesure(self, valeur, date_heure, id_emplacement, id_alerte, id_type_mesure):
        """Insertion dans la table 'mesure'"""
        conn = None
        try:
            conn = self.__creer_connexion()
            cursor = conn.cursor()
            query = """
                INSERT INTO mesure (valeur_mesure, date_heure_mesure, id_emplacement, id_alerte, id_type_mesure)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (valeur, date_heure, id_emplacement, id_alerte, id_type_mesure))
            conn.commit()
            return True
        except Error as e:
            print(f"Erreur insertion SQL : {e}")
            return False
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()