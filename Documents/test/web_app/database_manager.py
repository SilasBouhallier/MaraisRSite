import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from datetime import datetime
import json

class WebDatabaseManager:
    """
    Classe de gestion des interactions avec la base de données pour l'application web.
    Utilise l'utilisateur web_user avec accès depuis n'importe où (%).
    """

    def __init__(self):
        """
        Initialisation des paramètres de connexion depuis le fichier config.env ou variables d'environnement Docker.
        """
        # Charger les variables d'environnement depuis config.env (pour le développement local)
        try:
            load_dotenv('config.env')
        except:
            pass
        
        # Priorité aux variables d'environnement Docker
        self.__host = os.getenv('MYSQL_HOST', '127.0.0.1')
        self.__database = os.getenv('MYSQL_DATABASE')
        self.__user = os.getenv('MYSQL_USER')
        self.__password = os.getenv('MYSQL_PASSWORD')

    def __creer_connexion(self):
        """
        Méthode interne pour créer la connexion à la base de données.
        """
        return mysql.connector.connect(
            host=self.__host,
            database=self.__database,
            user=self.__user,
            password=self.__password
        )

    def __creer_connexion_dict(self):
        """
        Méthode interne pour créer la connexion avec curseur dictionnaire.
        """
        connexion = self.__creer_connexion()
        cursor = connexion.cursor(dictionary=True)
        return connexion, cursor

    # ==================== MÉTHODES POUR L'APPLICATION WEB ====================
    
    def get_all_mesures(self, limite=50):
        """
        Récupère toutes les mesures avec informations associées.
        """
        connexion = None
        try:
            connexion, cursor = self.__creer_connexion_dict()
            
            requete = """
            SELECT m.id_mesure, m.id_emplacement, m.valeur_mesure, m.date_heure_mesure,
                   e.nom_emplacement, a.nom_alerte, a.id_alerte,
                   s.nom_sonde, te.nom_type_emplacement
            FROM mesure m
            LEFT JOIN emplacement e ON m.id_emplacement = e.id_emplacement
            LEFT JOIN alerte a ON m.id_alerte = a.id_alerte
            LEFT JOIN sonde s ON e.id_sonde = s.id_sonde
            LEFT JOIN type_emplacement te ON e.id_type_emplacement = te.id_type_emplacement
            ORDER BY m.date_heure_mesure DESC
            LIMIT %s
            """
            
            cursor.execute(requete, (limite,))
            return cursor.fetchall()
            
        except Error as e:
            print(f"Erreur lors de la récupération des mesures : {e}")
            return []
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def get_mesures_by_emplacement(self, id_emplacement, limite=100):
        """
        Récupère les mesures pour un emplacement spécifique.
        """
        connexion = None
        try:
            connexion, cursor = self.__creer_connexion_dict()
            
            requete = """
            SELECT m.id_mesure, m.id_emplacement, m.valeur_mesure, m.date_heure_mesure,
                   e.nom_emplacement, a.nom_alerte, a.id_alerte
            FROM mesure m
            LEFT JOIN emplacement e ON m.id_emplacement = e.id_emplacement
            LEFT JOIN alerte a ON m.id_alerte = a.id_alerte
            WHERE m.id_emplacement = %s
            ORDER BY m.date_heure_mesure DESC
            LIMIT %s
            """
            
            cursor.execute(requete, (id_emplacement, limite))
            return cursor.fetchall()
            
        except Error as e:
            print(f"Erreur lors de la récupération des mesures : {e}")
            return []
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def get_emplacements(self):
        """
        Récupère tous les emplacements avec leurs informations.
        """
        connexion = None
        try:
            connexion, cursor = self.__creer_connexion_dict()
            
            requete = """
            SELECT e.id_emplacement, e.id_type_emplacement, e.id_sonde, e.nom_emplacement, te.nom_type_emplacement, s.nom_sonde
            FROM emplacement e
            LEFT JOIN type_emplacement te ON e.id_type_emplacement = te.id_type_emplacement
            LEFT JOIN sonde s ON e.id_sonde = s.id_sonde
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
        """
        connexion = None
        try:
            connexion, cursor = self.__creer_connexion_dict()
            
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
        Récupère tous les types de mesure avec leurs seuils.
        """
        connexion = None
        try:
            connexion, cursor = self.__creer_connexion_dict()
            
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

    def get_alertes(self):
        """
        Récupère tous les niveaux d'alerte.
        """
        connexion = None
        try:
            connexion, cursor = self.__creer_connexion_dict()
            
            requete = "SELECT id_alerte, nom_alerte FROM alerte ORDER BY id_alerte"
            cursor.execute(requete)
            return cursor.fetchall()
            
        except Error as e:
            print(f"Erreur lors de la récupération des alertes : {e}")
            return []
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def get_types_emplacement(self):
        """
        Récupère tous les types d'emplacement.
        """
        connexion = None
        try:
            connexion, cursor = self.__creer_connexion_dict()
            
            requete = "SELECT id_type_emplacement, nom_type_emplacement FROM type_emplacement ORDER BY id_type_emplacement"
            cursor.execute(requete)
            return cursor.fetchall()
            
        except Error as e:
            print(f"Erreur lors de la récupération des types d'emplacement : {e}")
            return []
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    # ==================== MÉTHODES DE MODIFICATION ====================
    
    def update_mesure(self, id_mesure, nouvelle_valeur=None, nouvelle_date=None, nouvel_id_alerte=None):
        """
        Met à jour une mesure existante.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            # Construction dynamique de la requête
            champs = []
            valeurs = []
            
            if nouvelle_valeur is not None:
                champs.append("valeur_mesure = %s")
                valeurs.append(nouvelle_valeur)
            if nouvelle_date is not None:
                champs.append("date_heure_mesure = %s")
                valeurs.append(nouvelle_date)
            if nouvel_id_alerte is not None:
                champs.append("id_alerte = %s")
                valeurs.append(nouvel_id_alerte)
            
            if not champs:
                return False
            
            valeurs.append(id_mesprise)
            requete = f"UPDATE mesure SET {', '.join(champs)} WHERE id_mesure = %s"
            
            cursor.execute(requete, valeurs)
            connexion.commit()
            
            return cursor.rowcount > 0
            
        except Error as e:
            print(f"Erreur lors de la mise à jour de la mesure : {e}")
            return False
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def update_emplacement(self, id_emplacement, nouveau_nom=None, nouvel_id_type=None, nouvel_id_sonde=None):
        """
        Met à jour un emplacement existant.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            # Construction dynamique de la requête
            champs = []
            valeurs = []
            
            if nouveau_nom is not None:
                champs.append("nom_emplacement = %s")
                valeurs.append(nouveau_nom)
            if nouvel_id_type is not None:
                champs.append("id_type_emplacement = %s")
                valeurs.append(nouvel_id_type)
            if nouvel_id_sonde is not None:
                champs.append("id_sonde = %s")
                valeurs.append(nouvel_id_sonde)
            
            if not champs:
                return False
            
            valeurs.append(id_emplacement)
            requete = f"UPDATE emplacement SET {', '.join(champs)} WHERE id_emplacement = %s"
            
            cursor.execute(requete, valeurs)
            connexion.commit()
            
            return cursor.rowcount > 0
            
        except Error as e:
            print(f"Erreur lors de la mise à jour de l'emplacement : {e}")
            return False
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def update_sonde(self, id_sonde, nouveau_nom):
        """
        Met à jour le nom d'une sonde.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = "UPDATE sonde SET nom_sonde = %s WHERE id_sonde = %s"
            cursor.execute(requete, (nouveau_nom, id_sonde))
            connexion.commit()
            
            return cursor.rowcount > 0
            
        except Error as e:
            print(f"Erreur lors de la mise à jour de la sonde : {e}")
            return False
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def update_type_mesure(self, id_type_mesure, nouveau_nom=None, nouveau_seuil_danger=None, 
                         nouveau_seuil_alerte=None, nouvelle_unite=None):
        """
        Met à jour un type de mesure.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            # Construction dynamique de la requête
            champs = []
            valeurs = []
            
            if nouveau_nom is not None:
                champs.append("nom_type_mesure = %s")
                valeurs.append(nouveau_nom)
            if nouveau_seuil_danger is not None:
                champs.append("valeur_danger_seuil = %s")
                valeurs.append(nouveau_seuil_danger)
            if nouveau_seuil_alerte is not None:
                champs.append("valeur_alerte_seuil = %s")
                valeurs.append(nouveau_seuil_alerte)
            if nouvelle_unite is not None:
                champs.append("Unité = %s")
                valeurs.append(nouvelle_unite)
            
            if not champs:
                return False
            
            valeurs.append(id_type_mesure)
            requete = f"UPDATE type_info_mesure SET {', '.join(champs)} WHERE id_type_mesure = %s"
            
            cursor.execute(requete, valeurs)
            connexion.commit()
            
            return cursor.rowcount > 0
            
        except Error as e:
            print(f"Erreur lors de la mise à jour du type de mesure : {e}")
            return False
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    # ==================== MÉTHODES D'INSERTION ====================
    
    def insert_mesure(self, valeur, date_heure, id_emplacement, id_alerte):
        """
        Insère une nouvelle mesure.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = """
            INSERT INTO mesure (valeur_mesure, date_heure_mesure, id_emplacement, id_alerte) 
            VALUES (%s, %s, %s, %s)
            """
            
            cursor.execute(requete, (valeur, date_heure, id_emplacement, id_alerte))
            connexion.commit()
            
            return cursor.lastrowid
            
        except Error as e:
            print(f"Erreur lors de l'insertion de la mesure : {e}")
            return None
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def insert_emplacement(self, nom, id_type_emplacement, id_sonde):
        """
        Insère un nouvel emplacement.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = """
            INSERT INTO emplacement (nom_emplacement, id_type_emplacement, id_sonde) 
            VALUES (%s, %s, %s)
            """
            
            cursor.execute(requete, (nom, id_type_emplacement, id_sonde))
            connexion.commit()
            
            return cursor.lastrowid
            
        except Error as e:
            print(f"Erreur lors de l'insertion de l'emplacement : {e}")
            return None
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def insert_sonde(self, nom):
        """
        Insère une nouvelle sonde.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = "INSERT INTO sonde (nom_sonde) VALUES (%s)"
            cursor.execute(requete, (nom,))
            connexion.commit()
            
            return cursor.lastrowid
            
        except Error as e:
            print(f"Erreur lors de l'insertion de la sonde : {e}")
            return None
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    # ==================== MÉTHODES DE SUPPRESSION ====================
    
    def delete_mesure(self, id_mesure):
        """
        Supprime une mesure.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = "DELETE FROM mesure WHERE id_mesure = %s"
            cursor.execute(requete, (id_mesure,))
            connexion.commit()
            
            return cursor.rowcount > 0
            
        except Error as e:
            print(f"Erreur lors de la suppression de la mesure : {e}")
            return False
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def delete_emplacement(self, id_emplacement):
        """
        Supprime un emplacement (attention: contraintes de clé étrangère).
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = "DELETE FROM emplacement WHERE id_emplacement = %s"
            cursor.execute(requete, (id_emplacement,))
            connexion.commit()
            
            return cursor.rowcount > 0
            
        except Error as e:
            print(f"Erreur lors de la suppression de l'emplacement : {e}")
            return False
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    # ==================== STATISTIQUES ====================
    
    def get_statistiques_mesures(self):
        """
        Récupère des statistiques sur les mesures.
        """
        connexion = None
        try:
            connexion, cursor = self.__creer_connexion_dict()
            
            requete = """
            SELECT 
                COUNT(*) as total_mesures,
                AVG(valeur_mesure) as moyenne_valeur,
                MIN(valeur_mesure) as min_valeur,
                MAX(valeur_mesure) as max_valeur,
                COUNT(DISTINCT id_emplacement) as nb_emplacements,
                COUNT(DISTINCT id_alerte) as nb_types_alerte
            FROM mesure
            """
            
            cursor.execute(requete)
            return cursor.fetchone()
            
        except Error as e:
            print(f"Erreur lors de la récupération des statistiques : {e}")
            return None
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def get_mesures_recentes(self, heures=24):
        """
        Récupère les mesures des dernières heures.
        """
        connexion = None
        try:
            connexion, cursor = self.__creer_connexion_dict()
            
            requete = """
            SELECT m.id_mesure, m.id_emplacement, m.valeur_mesure, m.date_heure_mesure,
                   e.nom_emplacement, a.nom_alerte, a.id_alerte
            FROM mesure m
            LEFT JOIN emplacement e ON m.id_emplacement = e.id_emplacement
            LEFT JOIN alerte a ON m.id_alerte = a.id_alerte
            WHERE m.date_heure_mesure >= DATE_SUB(NOW(), INTERVAL %s HOUR)
            ORDER BY m.date_heure_mesure DESC
            """
            
            cursor.execute(requete, (heures,))
            return cursor.fetchall()
            
        except Error as e:
            print(f"Erreur lors de la récupération des mesures récentes : {e}")
            return []
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    # ==================== EXPORT DE DONNÉES ====================
    
    def export_mesures_json(self, id_emplacement=None, limite=100):
        """
        Exporte les mesures au format JSON.
        """
        if id_emplacement:
            mesures = self.get_mesures_by_emplacement(id_emplacement, limite)
        else:
            mesures = self.get_all_mesures(limite)
        
        # Conversion des objets datetime en string pour JSON
        for mesure in mesures:
            if 'date_heure_mesure' in mesure and mesure['date_heure_mesure']:
                mesure['date_heure_mesure'] = mesure['date_heure_mesure'].isoformat()
        
        return json.dumps(mesures, indent=2, ensure_ascii=False)

    def test_connexion(self):
        """
        Teste la connexion à la base de données.
        """
        try:
            connexion = self.__creer_connexion()
            if connexion.is_connected():
                print("✅ Connexion à la base de données réussie")
                return True
        except Error as e:
            print(f"❌ Erreur de connexion : {e}")
            return False
        finally:
            if 'connexion' in locals() and connexion.is_connected():
                connexion.close()


# Exemple d'utilisation pour tester
if __name__ == "__main__":
    db = WebDatabaseManager()
    
    # Test de connexion
    if db.test_connexion():
        print("🎉 Le gestionnaire de base de données web est prêt!")
        
        # Quelques exemples de requêtes
        print("\n📊 Statistiques des mesures:")
        stats = db.get_statistiques_mesures()
        if stats:
            print(f"Total mesures: {stats['total_mesures']}")
            print(f"Moyenne: {stats['moyenne_valeur']:.2f}")
        
        print("\n📍 Emplacements disponibles:")
        emplacements = db.get_emplacements()
        for emp in emplacements[:3]:  # Affiche les 3 premiers
            print(f"- {emp['nom_emplacement']} ({emp['nom_type_emplacement']})")
    else:
        print("❌ Impossible de se connecter à la base de données")
