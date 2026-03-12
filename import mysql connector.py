import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

class DatabaseManager:
    """
    Classe de gestion des interactions avec le serveur MariaDB.
    Cette couche applicative assure le transport sécurisé des mesures du marais.
    """

    def __init__(self):
        """
        Initialisation des paramètres de connexion depuis le fichier .env.
        L'utilisation de '__' empêche l'accès direct à ces données sensibles.
        """
        # Charger les variables d'environnement depuis le fichier .env
        load_dotenv()
        
        self.__host = '127.0.0.1'
        self.__database = os.getenv('MYSQL_DATABASE')
        self.__user = os.getenv('MYSQL_USER')
        self.__password = os.getenv('MYSQL_PASSWORD')

    def __creer_connexion(self):
        """
        Méthode interne pour l'instanciation de la connexion réseau.
        """
        return mysql.connector.connect(
            host=self.__host,
            database=self.__database,
            user=self.__user,
            password=self.__password
        )

    def get_emplacements(self):
        """
        Récupère tous les emplacements disponibles avec leurs informations.
        Retourne une liste de dictionnaires avec id_emplacement, nom_emplacement, etc.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor(dictionary=True)
            
            requete = """
            SELECT e.id_emplacement, e.nom_emplacement, te.nom_type_emplacement, s.nom_sonde
            FROM emplacement e
            JOIN type_emplacement te ON e.id_type_emplacement = te.id_type_emplacement
            JOIN sonde s ON e.id_sonde = s.id_sonde
            ORDER BY e.id_emplacement
            """
            
            cursor.execute(requete)
            return cursor.fetchall()
            
        except Error as e:
            print(f"Erreur lors de la récupération des emplacements : {e}")
            return []
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def get_sondes(self):
        """
        Récupère toutes les sondes disponibles.
        Retourne une liste de dictionnaires avec id_sonde et nom_sonde.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor(dictionary=True)
            
            requete = "SELECT id_sonde, nom_sonde FROM sonde ORDER BY id_sonde"
            cursor.execute(requete)
            return cursor.fetchall()
            
        except Error as e:
            print(f"Erreur lors de la récupération des sondes : {e}")
            return []
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def get_types_mesure(self):
        """
        Récupère tous les types de mesure avec leurs seuils d'alerte.
        Retourne une liste de dictionnaires avec les informations de type_info_mesure.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor(dictionary=True)
            
            requete = """
            SELECT id_type_mesure, nom_type_mesure, valeur_danger_seuil, 
                   valeur_alerte_seuil, Unité
            FROM type_info_mesure
            ORDER BY id_type_mesure
            """
            
            cursor.execute(requete)
            return cursor.fetchall()
            
        except Error as e:
            print(f"Erreur lors de la récupération des types de mesure : {e}")
            return []
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def determiner_id_alerte(self, valeur, nom_type_mesure):
        """
        Détermine l'ID d'alerte en fonction de la valeur et du type de mesure.
        
        Arguments :
        - valeur : La valeur mesurée
        - nom_type_mesure : Le nom du type de mesure (ex: 'CO2', 'PM 2.5')
        
        Retourne :
        - 1 : Normal (valeur < seuil alerte)
        - 2 : Alerte (seuil alerte <= valeur < seuil danger)
        - 3 : Danger (valeur >= seuil danger)
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor(dictionary=True)
            
            requete = """
            SELECT valeur_alerte_seuil, valeur_danger_seuil
            FROM type_info_mesure
            WHERE nom_type_mesure = %s
            """
            
            cursor.execute(requete, (nom_type_mesure,))
            resultat = cursor.fetchone()
            
            if not resultat:
                print(f"Type de mesure '{nom_type_mesure}' non trouvé")
                return 1  # Normal par défaut
            
            seuil_alerte = resultat['valeur_alerte_seuil']
            seuil_danger = resultat['valeur_danger_seuil']
            
            if valeur >= seuil_danger:
                return 3  # Danger
            elif valeur >= seuil_alerte:
                return 2  # Alerte
            else:
                return 1  # Normal
                
        except Error as e:
            print(f"Erreur lors de la détermination de l'alerte : {e}")
            return 1  # Normal par défaut
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def trouver_id_emplacement_par_sonde(self, nom_sonde):
        """
        Trouve l'ID d'emplacement correspondant à une sonde.
        
        Arguments :
        - nom_sonde : Le nom ou l'identifiant de la sonde
        
        Retourne l'ID d'emplacement ou None si non trouvé
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = """
            SELECT e.id_emplacement
            FROM emplacement e
            JOIN sonde s ON e.id_sonde = s.id_sonde
            WHERE s.nom_sonde = %s
            """
            
            cursor.execute(requete, (nom_sonde,))
            resultat = cursor.fetchone()
            
            return resultat[0] if resultat else None
            
        except Error as e:
            print(f"Erreur lors de la recherche de l'emplacement : {e}")
            return None
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def ajouter_mesure_automatique(self, valeur, date_heure, nom_sonde, nom_type_mesure):
        """
        Ajoute une mesure en déterminant automatiquement l'emplacement et l'alerte.
        
        Arguments :
        - valeur : Donnée numérique du capteur
        - date_heure : Date fournie par le capteur (Format 'YYYY-MM-DD HH:MM:SS')
        - nom_sonde : Nom ou identifiant de la sonde
        - nom_type_mesure : Type de mesure (ex: 'CO2', 'PM 2.5')
        """
        # Déterminer automatiquement l'ID d'emplacement
        id_emplacement = self.trouver_id_emplacement_par_sonde(nom_sonde)
        if id_emplacement is None:
            print(f"Erreur : Sonde '{nom_sonde}' non trouvée")
            return False
        
        # Déterminer automatiquement l'ID d'alerte
        id_alerte = self.determiner_id_alerte(valeur, nom_type_mesure)
        
        # Ajouter la mesure avec les IDs déterminés
        return self.ajouter_mesure(valeur, date_heure, id_emplacement, id_alerte)

    def ajouter_mesure(self, valeur, date_heure, id_emplacement, id_alerte):
        """
        Insertion d'une mesure complète dans la table 'mesure'.
        
        Arguments reçus :
        - valeur : Donnée numérique du capteur.
        - date_heure : Date fournie le capteur (Format 'YYYY-MM-DD HH:MM:SS').
        
        Correspondance des ID Emplacement (id_emplacement) :
        - 1 : Zone Machine (Local technique / Serveurs)
        - 2 : Zone Peinture (Entrée du marais)
        - 3 : Zone solvant (Zone profonde)
        
        Correspondance des ID Alerte (id_alerte) :
        - 1 : Normal (Fonctionnement nominal)
        - 2 : Alerte (Seuil de vigilance atteint)
        - 3 : Danger (Action immédiate requise)
        """
        connexion = None
        try:
            # Ouverture du canal de communication
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            # Requête préparée : id_mesure est omis car géré en AUTO_INCREMENT par la BDD.
            # L'utilisation de %s garantit une protection contre les injections SQL.
            requete = """
            INSERT INTO mesure (valeur_mesure, date_heure_mesure, id_emplacement, id_alerte) 
            VALUES (%s, %s, %s, %s)
            """
            
            # Organisation des données dans l'ordre des colonnes SQL
            donnees = (valeur, date_heure, id_emplacement, id_alerte)
            
            # Exécution et validation de la transaction
            cursor.execute(requete, donnees)
            connexion.commit()

        except Error as e:
            # Capture et affichage des erreurs SQL pour le débogage
            print(f"Erreur lors de l'insertion SQL : {e}")
        
        finally:
            # Libération systématique des ressources pour éviter la saturation du serveur
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()
