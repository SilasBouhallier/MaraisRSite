import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
from datetime import datetime

class DatabaseCommands:
    """
    Classe complète pour gérer les commandes d'insertion et modification 
    pour toutes les tables de la base de données Marais_R_Site.
    """

    def __init__(self):
        """
        Initialisation des paramètres de connexion depuis le fichier .env.
        """
        load_dotenv()
        
        self.__host = '127.0.0.1'
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

    # ==================== TABLE ALARME ====================
    
    def inserer_alarme(self, nom_alarme):
        """
        Insère une nouvelle alarme dans la table alarme.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = "INSERT INTO alarme (nom_alarme) VALUES (%s)"
            cursor.execute(requete, (nom_alarme,))
            connexion.commit()
            
            print(f"✅ Alarme '{nom_alarme}' insérée avec succès (ID: {cursor.lastrowid})")
            return cursor.lastrowid
            
        except Error as e:
            print(f"❌ Erreur lors de l'insertion de l'alarme : {e}")
            return None
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def modifier_alarme(self, id_alarme, nouveau_nom):
        """
        Modifie le nom d'une alarme existante.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = "UPDATE alarme SET nom_alarme = %s WHERE id_alarme = %s"
            cursor.execute(requete, (nouveau_nom, id_alarme))
            connexion.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Alarme ID {id_alarme} modifiée avec succès")
                return True
            else:
                print(f"⚠️ Aucune alarme trouvée avec l'ID {id_alarme}")
                return False
                
        except Error as e:
            print(f"❌ Erreur lors de la modification de l'alarme : {e}")
            return False
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    # ==================== TABLE ALERTE ====================
    
    def inserer_alerte(self, nom_alerte):
        """
        Insère une nouvelle alerte dans la table alerte.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = "INSERT INTO alerte (nom_alerte) VALUES (%s)"
            cursor.execute(requete, (nom_alerte,))
            connexion.commit()
            
            print(f"✅ Alerte '{nom_alerte}' insérée avec succès (ID: {cursor.lastrowid})")
            return cursor.lastrowid
            
        except Error as e:
            print(f"❌ Erreur lors de l'insertion de l'alerte : {e}")
            return None
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def modifier_alerte(self, id_alerte, nouveau_nom):
        """
        Modifie le nom d'une alerte existante.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = "UPDATE alerte SET nom_alerte = %s WHERE id_alerte = %s"
            cursor.execute(requete, (nouveau_nom, id_alerte))
            connexion.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Alerte ID {id_alerte} modifiée avec succès")
                return True
            else:
                print(f"⚠️ Aucune alerte trouvée avec l'ID {id_alerte}")
                return False
                
        except Error as e:
            print(f"❌ Erreur lors de la modification de l'alerte : {e}")
            return False
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    # ==================== TABLE SONDE ====================
    
    def inserer_sonde(self, nom_sonde):
        """
        Insère une nouvelle sonde dans la table sonde.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = "INSERT INTO sonde (nom_sonde) VALUES (%s)"
            cursor.execute(requete, (nom_sonde,))
            connexion.commit()
            
            print(f"✅ Sonde '{nom_sonde}' insérée avec succès (ID: {cursor.lastrowid})")
            return cursor.lastrowid
            
        except Error as e:
            print(f"❌ Erreur lors de l'insertion de la sonde : {e}")
            return None
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def modifier_sonde(self, id_sonde, nouveau_nom):
        """
        Modifie le nom d'une sonde existante.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = "UPDATE sonde SET nom_sonde = %s WHERE id_sonde = %s"
            cursor.execute(requete, (nouveau_nom, id_sonde))
            connexion.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Sonde ID {id_sonde} modifiée avec succès")
                return True
            else:
                print(f"⚠️ Aucune sonde trouvée avec l'ID {id_sonde}")
                return False
                
        except Error as e:
            print(f"❌ Erreur lors de la modification de la sonde : {e}")
            return False
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    # ==================== TABLE TYPE_EMPLACEMENT ====================
    
    def inserer_type_emplacement(self, nom_type_emplacement):
        """
        Insère un nouveau type d'emplacement dans la table type_emplacement.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = "INSERT INTO type_emplacement (nom_type_emplacement) VALUES (%s)"
            cursor.execute(requete, (nom_type_emplacement,))
            connexion.commit()
            
            print(f"✅ Type emplacement '{nom_type_emplacement}' inséré avec succès (ID: {cursor.lastrowid})")
            return cursor.lastrowid
            
        except Error as e:
            print(f"❌ Erreur lors de l'insertion du type d'emplacement : {e}")
            return None
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def modifier_type_emplacement(self, id_type_emplacement, nouveau_nom):
        """
        Modifie le nom d'un type d'emplacement existant.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = "UPDATE type_emplacement SET nom_type_emplacement = %s WHERE id_type_emplacement = %s"
            cursor.execute(requete, (nouveau_nom, id_type_emplacement))
            connexion.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Type emplacement ID {id_type_emplacement} modifié avec succès")
                return True
            else:
                print(f"⚠️ Aucun type d'emplacement trouvé avec l'ID {id_type_emplacement}")
                return False
                
        except Error as e:
            print(f"❌ Erreur lors de la modification du type d'emplacement : {e}")
            return False
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    # ==================== TABLE TYPE_INFO_MESURE ====================
    
    def inserer_type_info_mesure(self, nom_type_mesure, valeur_danger_seuil, valeur_alerte_seuil, unite):
        """
        Insère un nouveau type de mesure dans la table type_info_mesure.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = """
            INSERT INTO type_info_mesure (nom_type_mesure, valeur_danger_seuil, valeur_alerte_seuil, Unité) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(requete, (nom_type_mesure, valeur_danger_seuil, valeur_alerte_seuil, unite))
            connexion.commit()
            
            print(f"✅ Type mesure '{nom_type_mesure}' inséré avec succès (ID: {cursor.lastrowid})")
            return cursor.lastrowid
            
        except Error as e:
            print(f"❌ Erreur lors de l'insertion du type de mesure : {e}")
            return None
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def modifier_type_info_mesure(self, id_type_mesure, nom_type_mesure=None, valeur_danger_seuil=None, 
                                 valeur_alerte_seuil=None, unite=None):
        """
        Modifie un type de mesure existant. Seuls les paramètres non None sont modifiés.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            # Construction dynamique de la requête
            champs = []
            valeurs = []
            
            if nom_type_mesure is not None:
                champs.append("nom_type_mesure = %s")
                valeurs.append(nom_type_mesure)
            if valeur_danger_seuil is not None:
                champs.append("valeur_danger_seuil = %s")
                valeurs.append(valeur_danger_seuil)
            if valeur_alerte_seuil is not None:
                champs.append("valeur_alerte_seuil = %s")
                valeurs.append(valeur_alerte_seuil)
            if unite is not None:
                champs.append("Unité = %s")
                valeurs.append(unite)
            
            if not champs:
                print("⚠️ Aucun champ à modifier")
                return False
            
            valeurs.append(id_type_mesure)
            requete = f"UPDATE type_info_mesure SET {', '.join(champs)} WHERE id_type_mesure = %s"
            
            cursor.execute(requete, valeurs)
            connexion.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Type mesure ID {id_type_mesure} modifié avec succès")
                return True
            else:
                print(f"⚠️ Aucun type de mesure trouvé avec l'ID {id_type_mesure}")
                return False
                
        except Error as e:
            print(f"❌ Erreur lors de la modification du type de mesure : {e}")
            return False
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    # ==================== TABLE UTILISATEUR ====================
    
    def inserer_utilisateur(self, nom_utilisateur, mot_de_passe, role_utilisateur):
        """
        Insère un nouvel utilisateur dans la table utilisateur.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = """
            INSERT INTO utilisateur (nom_utilisateur, mot_de_passe_utilisateur, role_utilisateur) 
            VALUES (%s, %s, %s)
            """
            cursor.execute(requete, (nom_utilisateur, mot_de_passe, role_utilisateur))
            connexion.commit()
            
            print(f"✅ Utilisateur '{nom_utilisateur}' inséré avec succès (ID: {cursor.lastrowid})")
            return cursor.lastrowid
            
        except Error as e:
            print(f"❌ Erreur lors de l'insertion de l'utilisateur : {e}")
            return None
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def modifier_utilisateur(self, id_utilisateur, nom_utilisateur=None, mot_de_passe=None, role_utilisateur=None):
        """
        Modifie un utilisateur existant. Seuls les paramètres non None sont modifiés.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            # Construction dynamique de la requête
            champs = []
            valeurs = []
            
            if nom_utilisateur is not None:
                champs.append("nom_utilisateur = %s")
                valeurs.append(nom_utilisateur)
            if mot_de_passe is not None:
                champs.append("mot_de_passe_utilisateur = %s")
                valeurs.append(mot_de_passe)
            if role_utilisateur is not None:
                champs.append("role_utilisateur = %s")
                valeurs.append(role_utilisateur)
            
            if not champs:
                print("⚠️ Aucun champ à modifier")
                return False
            
            valeurs.append(id_utilisateur)
            requete = f"UPDATE utilisateur SET {', '.join(champs)} WHERE id_utilisateur = %s"
            
            cursor.execute(requete, valeurs)
            connexion.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Utilisateur ID {id_utilisateur} modifié avec succès")
                return True
            else:
                print(f"⚠️ Aucun utilisateur trouvé avec l'ID {id_utilisateur}")
                return False
                
        except Error as e:
            print(f"❌ Erreur lors de la modification de l'utilisateur : {e}")
            return False
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    # ==================== TABLE EMPLACEMENT ====================
    
    def inserer_emplacement(self, nom_emplacement, id_type_emplacement, id_sonde):
        """
        Insère un nouvel emplacement dans la table emplacement.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = """
            INSERT INTO emplacement (nom_emplacement, id_type_emplacement, id_sonde) 
            VALUES (%s, %s, %s)
            """
            cursor.execute(requete, (nom_emplacement, id_type_emplacement, id_sonde))
            connexion.commit()
            
            print(f"✅ Emplacement '{nom_emplacement}' inséré avec succès (ID: {cursor.lastrowid})")
            return cursor.lastrowid
            
        except Error as e:
            print(f"❌ Erreur lors de l'insertion de l'emplacement : {e}")
            return None
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def modifier_emplacement(self, id_emplacement, nom_emplacement=None, id_type_emplacement=None, id_sonde=None):
        """
        Modifie un emplacement existant. Seuls les paramètres non None sont modifiés.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            # Construction dynamique de la requête
            champs = []
            valeurs = []
            
            if nom_emplacement is not None:
                champs.append("nom_emplacement = %s")
                valeurs.append(nom_emplacement)
            if id_type_emplacement is not None:
                champs.append("id_type_emplacement = %s")
                valeurs.append(id_type_emplacement)
            if id_sonde is not None:
                champs.append("id_sonde = %s")
                valeurs.append(id_sonde)
            
            if not champs:
                print("⚠️ Aucun champ à modifier")
                return False
            
            valeurs.append(id_emplacement)
            requete = f"UPDATE emplacement SET {', '.join(champs)} WHERE id_emplacement = %s"
            
            cursor.execute(requete, valeurs)
            connexion.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Emplacement ID {id_emplacement} modifié avec succès")
                return True
            else:
                print(f"⚠️ Aucun emplacement trouvé avec l'ID {id_emplacement}")
                return False
                
        except Error as e:
            print(f"❌ Erreur lors de la modification de l'emplacement : {e}")
            return False
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    # ==================== TABLE MESURE ====================
    
    def inserer_mesure(self, valeur_mesure, date_heure_mesure, id_emplacement, id_alerte):
        """
        Insère une nouvelle mesure dans la table mesure.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = """
            INSERT INTO mesure (valeur_mesure, date_heure_mesure, id_emplacement, id_alerte) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(requete, (valeur_mesure, date_heure_mesure, id_emplacement, id_alerte))
            connexion.commit()
            
            print(f"✅ Mesure insérée avec succès (ID: {cursor.lastrowid})")
            return cursor.lastrowid
            
        except Error as e:
            print(f"❌ Erreur lors de l'insertion de la mesure : {e}")
            return None
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def modifier_mesure(self, id_mesure, valeur_mesure=None, date_heure_mesure=None, id_emplacement=None, id_alerte=None):
        """
        Modifie une mesure existante. Seuls les paramètres non None sont modifiés.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            # Construction dynamique de la requête
            champs = []
            valeurs = []
            
            if valeur_mesure is not None:
                champs.append("valeur_mesure = %s")
                valeurs.append(valeur_mesure)
            if date_heure_mesure is not None:
                champs.append("date_heure_mesure = %s")
                valeurs.append(date_heure_mesure)
            if id_emplacement is not None:
                champs.append("id_emplacement = %s")
                valeurs.append(id_emplacement)
            if id_alerte is not None:
                champs.append("id_alerte = %s")
                valeurs.append(id_alerte)
            
            if not champs:
                print("⚠️ Aucun champ à modifier")
                return False
            
            valeurs.append(id_mesure)
            requete = f"UPDATE mesure SET {', '.join(champs)} WHERE id_mesure = %s"
            
            cursor.execute(requete, valeurs)
            connexion.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Mesure ID {id_mesure} modifiée avec succès")
                return True
            else:
                print(f"⚠️ Aucune mesure trouvée avec l'ID {id_mesure}")
                return False
                
        except Error as e:
            print(f"❌ Erreur lors de la modification de la mesure : {e}")
            return False
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    # ==================== TABLES DE JOINTURE ====================
    
    def inserer_installe(self, id_alarme, id_emplacement):
        """
        Insère une relation dans la table installe (table de jointure).
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = "INSERT INTO installe (id_alarme, id_emplacement) VALUES (%s, %s)"
            cursor.execute(requete, (id_alarme, id_emplacement))
            connexion.commit()
            
            print(f"✅ Relation alarme-emplacement insérée avec succès")
            return True
            
        except Error as e:
            print(f"❌ Erreur lors de l'insertion de la relation : {e}")
            return False
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def supprimer_installe(self, id_alarme, id_emplacement):
        """
        Supprime une relation dans la table installe.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = "DELETE FROM installe WHERE id_alarme = %s AND id_emplacement = %s"
            cursor.execute(requete, (id_alarme, id_emplacement))
            connexion.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Relation alarme-emplacement supprimée avec succès")
                return True
            else:
                print(f"⚠️ Aucune relation trouvée pour ces IDs")
                return False
                
        except Error as e:
            print(f"❌ Erreur lors de la suppression de la relation : {e}")
            return False
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def inserer_type_info_mesure_as_mesure(self, id_type_mesure, id_mesure):
        """
        Insère une relation dans la table type_info_mesure_as_mesure.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = "INSERT INTO type_info_mesure_as_mesure (id_type_mesure, id_mesure) VALUES (%s, %s)"
            cursor.execute(requete, (id_type_mesure, id_mesure))
            connexion.commit()
            
            print(f"✅ Relation type_mesure-mesure insérée avec succès")
            return True
            
        except Error as e:
            print(f"❌ Erreur lors de l'insertion de la relation : {e}")
            return False
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def supprimer_type_info_mesure_as_mesure(self, id_type_mesure, id_mesure):
        """
        Supprime une relation dans la table type_info_mesure_as_mesure.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            requete = "DELETE FROM type_info_mesure_as_mesure WHERE id_type_mesure = %s AND id_mesure = %s"
            cursor.execute(requete, (id_type_mesure, id_mesure))
            connexion.commit()
            
            if cursor.rowcount > 0:
                print(f"✅ Relation type_mesure-mesure supprimée avec succès")
                return True
            else:
                print(f"⚠️ Aucune relation trouvée pour ces IDs")
                return False
                
        except Error as e:
            print(f"❌ Erreur lors de la suppression de la relation : {e}")
            return False
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    # ==================== MÉTHODES UTILITAIRES ====================
    
    def afficher_donnees_table(self, nom_table, limite=10):
        """
        Affiche les données d'une table spécifique.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor(dictionary=True)
            
            requete = f"SELECT * FROM {nom_table} LIMIT {limite}"
            cursor.execute(requete)
            resultats = cursor.fetchall()
            
            if resultats:
                print(f"\n📋 Données de la table '{nom_table}' (limite: {limite}):")
                for ligne in resultats:
                    print(ligne)
            else:
                print(f"📭 Table '{nom_table}' vide")
                
        except Error as e:
            print(f"❌ Erreur lors de l'affichage des données : {e}")
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()

    def lister_tables(self):
        """
        Liste toutes les tables de la base de données.
        """
        connexion = None
        try:
            connexion = self.__creer_connexion()
            cursor = connexion.cursor()
            
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            print("\n📚 Tables disponibles dans la base de données:")
            for table in tables:
                print(f"  - {table[0]}")
                
        except Error as e:
            print(f"❌ Erreur lors de la liste des tables : {e}")
        
        finally:
            if connexion and connexion.is_connected():
                cursor.close()
                connexion.close()


def menu_principal():
    """
    Interface utilisateur interactive pour choisir les tables et les actions.
    """
    db = DatabaseCommands()
    
    while True:
        print("\n" + "="*60)
        print("🗄️  SYSTÈME DE GESTION DE BASE DE DONNÉES")
        print("="*60)
        print("1. 👀 Lister les tables")
        print("2. 📋 Afficher les données d'une table")
        print("3. ➕ Insérer des données")
        print("4. ✏️  Modifier des données")
        print("5. 🔗 Gérer les relations (tables de jointure)")
        print("6. ❌ Supprimer des relations")
        print("0. 🚪 Quitter")
        
        choix = input("\n👉 Choisissez une option (0-6): ").strip()
        
        if choix == "0":
            print("\n👋 Au revoir!")
            break
        
        elif choix == "1":
            db.lister_tables()
        
        elif choix == "2":
            table = input("👉 Nom de la table: ").strip()
            limite = input("👉 Limite de résultats (défaut: 10): ").strip()
            limite = int(limite) if limite.isdigit() else 10
            db.afficher_donnees_table(table, limite)
        
        elif choix == "3":
            menu_insertion(db)
        
        elif choix == "4":
            menu_modification(db)
        
        elif choix == "5":
            menu_relations(db)
        
        elif choix == "6":
            menu_suppression_relations(db)
        
        else:
            print("❌ Option invalide. Veuillez réessayer.")


def menu_insertion(db):
    """
    Menu pour les opérations d'insertion.
    """
    print("\n➕ MENU D'INSERTION")
    print("-"*30)
    tables = [
        ("alarme", "Alarme"),
        ("alerte", "Alerte"),
        ("sonde", "Sonde"),
        ("type_emplacement", "Type d'emplacement"),
        ("type_info_mesure", "Type de mesure"),
        ("utilisateur", "Utilisateur"),
        ("emplacement", "Emplacement"),
        ("mesure", "Mesure")
    ]
    
    for i, (table, description) in enumerate(tables, 1):
        print(f"{i}. {description}")
    
    choix = input("\n👉 Choisissez une table (1-8): ").strip()
    
    try:
        index = int(choix) - 1
        if 0 <= index < len(tables):
            table, description = tables[index]
            inserer_donnees_table(db, table)
        else:
            print("❌ Choix invalide")
    except ValueError:
        print("❌ Veuillez entrer un nombre")


def inserer_donnees_table(db, table):
    """
    Interface d'insertion pour une table spécifique.
    """
    if table == "alarme":
        nom = input("👉 Nom de l'alarme: ").strip()
        db.inserer_alarme(nom)
    
    elif table == "alerte":
        nom = input("👉 Nom de l'alerte: ").strip()
        db.inserer_alerte(nom)
    
    elif table == "sonde":
        nom = input("👉 Nom de la sonde: ").strip()
        db.inserer_sonde(nom)
    
    elif table == "type_emplacement":
        nom = input("👉 Nom du type d'emplacement: ").strip()
        db.inserer_type_emplacement(nom)
    
    elif table == "type_info_mesure":
        nom = input("👉 Nom du type de mesure: ").strip()
        danger = input("👉 Seuil danger: ").strip()
        alerte = input("👉 Seuil alerte: ").strip()
        unite = input("👉 Unité: ").strip()
        db.inserer_type_info_mesure(nom, float(danger), float(alerte), unite)
    
    elif table == "utilisateur":
        nom = input("👉 Nom d'utilisateur: ").strip()
        mdp = input("👉 Mot de passe: ").strip()
        role = input("👉 Rôle: ").strip()
        db.inserer_utilisateur(nom, mdp, role)
    
    elif table == "emplacement":
        nom = input("👉 Nom de l'emplacement: ").strip()
        type_empl = input("👉 ID type emplacement: ").strip()
        sonde = input("👉 ID sonde: ").strip()
        db.inserer_emplacement(nom, int(type_empl), int(sonde))
    
    elif table == "mesure":
        valeur = input("👉 Valeur mesurée: ").strip()
        date = input("👉 Date et heure (YYYY-MM-DD HH:MM:SS): ").strip()
        emplacement = input("👉 ID emplacement: ").strip()
        alerte = input("👉 ID alerte: ").strip()
        db.inserer_mesure(float(valeur), date, int(emplacement), int(alerte))


def menu_modification(db):
    """
    Menu pour les opérations de modification.
    """
    print("\n✏️ MENU DE MODIFICATION")
    print("-"*30)
    tables = [
        ("alarme", "Alarme"),
        ("alerte", "Alerte"),
        ("sonde", "Sonde"),
        ("type_emplacement", "Type d'emplacement"),
        ("type_info_mesure", "Type de mesure"),
        ("utilisateur", "Utilisateur"),
        ("emplacement", "Emplacement"),
        ("mesure", "Mesure")
    ]
    
    for i, (table, description) in enumerate(tables, 1):
        print(f"{i}. {description}")
    
    choix = input("\n👉 Choisissez une table (1-8): ").strip()
    
    try:
        index = int(choix) - 1
        if 0 <= index < len(tables):
            table, description = tables[index]
            modifier_donnees_table(db, table)
        else:
            print("❌ Choix invalide")
    except ValueError:
        print("❌ Veuillez entrer un nombre")


def modifier_donnees_table(db, table):
    """
    Interface de modification pour une table spécifique.
    """
    id_enregistrement = input(f"👉 ID de l'enregistrement à modifier: ").strip()
    
    if table == "alarme":
        nouveau_nom = input("👉 Nouveau nom (laisser vide pour ne pas changer): ").strip()
        if nouveau_nom:
            db.modifier_alarme(int(id_enregistrement), nouveau_nom)
    
    elif table == "alerte":
        nouveau_nom = input("👉 Nouveau nom (laisser vide pour ne pas changer): ").strip()
        if nouveau_nom:
            db.modifier_alerte(int(id_enregistrement), nouveau_nom)
    
    elif table == "sonde":
        nouveau_nom = input("👉 Nouveau nom (laisser vide pour ne pas changer): ").strip()
        if nouveau_nom:
            db.modifier_sonde(int(id_enregistrement), nouveau_nom)
    
    elif table == "type_emplacement":
        nouveau_nom = input("👉 Nouveau nom (laisser vide pour ne pas changer): ").strip()
        if nouveau_nom:
            db.modifier_type_emplacement(int(id_enregistrement), nouveau_nom)
    
    elif table == "type_info_mesure":
        nom = input("👉 Nouveau nom (laisser vide): ").strip() or None
        danger = input("👉 Nouveau seuil danger (laisser vide): ").strip()
        alerte = input("👉 Nouveau seuil alerte (laisser vide): ").strip()
        unite = input("👉 Nouvelle unité (laisser vide): ").strip() or None
        
        danger = float(danger) if danger else None
        alerte = float(alerte) if alerte else None
        
        db.modifier_type_info_mesure(int(id_enregistrement), nom, danger, alerte, unite)
    
    elif table == "utilisateur":
        nom = input("👉 Nouveau nom (laisser vide): ").strip() or None
        mdp = input("👉 Nouveau mot de passe (laisser vide): ").strip() or None
        role = input("👉 Nouveau rôle (laisser vide): ").strip() or None
        
        db.modifier_utilisateur(int(id_enregistrement), nom, mdp, role)
    
    elif table == "emplacement":
        nom = input("👉 Nouveau nom (laisser vide): ").strip() or None
        type_empl = input("👉 Nouvel ID type emplacement (laisser vide): ").strip()
        sonde = input("👉 Nouvel ID sonde (laisser vide): ").strip()
        
        type_empl = int(type_empl) if type_empl else None
        sonde = int(sonde) if sonde else None
        
        db.modifier_emplacement(int(id_enregistrement), nom, type_empl, sonde)
    
    elif table == "mesure":
        valeur = input("👉 Nouvelle valeur (laisser vide): ").strip()
        date = input("👉 Nouvelle date (laisser vide): ").strip() or None
        emplacement = input("👉 Nouvel ID emplacement (laisser vide): ").strip()
        alerte = input("👉 Nouvel ID alerte (laisser vide): ").strip()
        
        valeur = float(valeur) if valeur else None
        emplacement = int(emplacement) if emplacement else None
        alerte = int(alerte) if alerte else None
        
        db.modifier_mesure(int(id_enregistrement), valeur, date, emplacement, alerte)


def menu_relations(db):
    """
    Menu pour gérer les relations (tables de jointure).
    """
    print("\n🔗 MENU DES RELATIONS")
    print("-"*30)
    print("1. Ajouter une relation alarme-emplacement")
    print("2. Ajouter une relation type_mesure-mesure")
    
    choix = input("\n👉 Choisissez une option (1-2): ").strip()
    
    if choix == "1":
        id_alarme = input("👉 ID alarme: ").strip()
        id_emplacement = input("👉 ID emplacement: ").strip()
        db.inserer_installe(int(id_alarme), int(id_emplacement))
    
    elif choix == "2":
        id_type_mesure = input("👉 ID type mesure: ").strip()
        id_mesure = input("👉 ID mesure: ").strip()
        db.inserer_type_info_mesure_as_mesure(int(id_type_mesure), int(id_mesure))
    
    else:
        print("❌ Option invalide")


def menu_suppression_relations(db):
    """
    Menu pour supprimer des relations.
    """
    print("\n❌ MENU DE SUPPRESSION DES RELATIONS")
    print("-"*30)
    print("1. Supprimer une relation alarme-emplacement")
    print("2. Supprimer une relation type_mesure-mesure")
    
    choix = input("\n👉 Choisissez une option (1-2): ").strip()
    
    if choix == "1":
        id_alarme = input("👉 ID alarme: ").strip()
        id_emplacement = input("👉 ID emplacement: ").strip()
        db.supprimer_installe(int(id_alarme), int(id_emplacement))
    
    elif choix == "2":
        id_type_mesure = input("👉 ID type mesure: ").strip()
        id_mesure = input("👉 ID mesure: ").strip()
        db.supprimer_type_info_mesure_as_mesure(int(id_type_mesure), int(id_mesure))
    
    else:
        print("❌ Option invalide")


if __name__ == "__main__":
    menu_principal()
