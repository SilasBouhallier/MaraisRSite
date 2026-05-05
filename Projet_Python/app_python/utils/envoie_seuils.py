import time
import json
import os
import threading
import mysql.connector
import paho.mqtt.client as mqtt
from datetime import datetime


class EnvoiSeuils:
    """Synchronise les seuils BDD avec fichier JSON et envoie uniquement si changement"""
    
    def __init__(self, config_bdd, config_mqtt):
        self.config_bdd = config_bdd
        self.config_mqtt = config_mqtt
        self.mqtt_client = None
        self.thread = None
        self.actif = False
        self.intervalle = 60  # Vérifie toutes les 60 secondes
        
        # Fichier JSON pour stocker les seuils localement
        self.fichier_seuils = os.path.join(
            os.path.dirname(__file__), '..', 'seuils_cache.json'
        )
        
        # Cache en mémoire des seuils
        self.seuils_cache = {}
        
        # Charger les seuils existants
        self._charger_cache()
    
    def _connecter_mqtt(self):
        """Connexion au broker MQTT"""
        try:
            self.mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
            broker = self.config_mqtt.get('broker', 'localhost')
            port = int(self.config_mqtt.get('port', 1883))
            username = self.config_mqtt.get('username')
            password = self.config_mqtt.get('password')
            
            if username and password:
                self.mqtt_client.username_pw_set(username, password)
            
            # TLS si port 8883
            if port == 8883:
                import os
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                self.mqtt_client.tls_set(
                    ca_certs=os.path.join(base_dir, "mosquitto/config/ca.crt"),
                    certfile=os.path.join(base_dir, "mosquitto/config/server.crt"),
                    keyfile=os.path.join(base_dir, "mosquitto/config/server.key")
                )
            self.mqtt_client.connect(broker, port, 60)
            self.mqtt_client.loop_start()
            return True
        except Exception as e:
            print(f"[SEUILS] ERREUR connexion MQTT: {e}")
            return False
    
    def _charger_cache(self):
        """Charge les seuils depuis le fichier JSON local"""
        try:
            if os.path.exists(self.fichier_seuils):
                with open(self.fichier_seuils, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.seuils_cache = data.get('seuils', {})
            else:
                self.seuils_cache = {}
        except Exception:
            self.seuils_cache = {}
    
    def _sauvegarder_cache(self):
        """Sauvegarde les seuils dans le fichier JSON local"""
        try:
            data = {
                'derniere_mise_a_jour': datetime.now().isoformat(),
                'seuils': self.seuils_cache
            }
            with open(self.fichier_seuils, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception:
            pass
    
    def _recuperer_seuils_bdd(self):
        """Récupère les seuils depuis la BDD"""
        conn = None
        try:
            conn = mysql.connector.connect(
                host=self.config_bdd.get('host'),
                user=self.config_bdd.get('user'),
                password=self.config_bdd.get('password'),
                database=self.config_bdd.get('database')
            )
            cursor = conn.cursor(dictionary=True)
            
            query = """
                SELECT nom_type_mesure, valeur_alerte_seuil, valeur_danger_seuil
                FROM type_info_mesure
            """
            cursor.execute(query)
            seuils = cursor.fetchall()
            
            cursor.close()
            conn.close()
            
            # Convertir en dictionnaire
            result = {}
            for seuil in seuils:
                result[seuil['nom_type_mesure']] = {
                    'valeur_alerte_seuil': float(seuil['valeur_alerte_seuil']),
                    'valeur_danger_seuil': float(seuil['valeur_danger_seuil'])
                }
            return result
            
        except Exception:
            if conn:
                conn.close()
            return None
    
    def _comparer_seuils(self, seuils_bdd):
        """Compare les seuils BDD avec le cache, retourne True si différence"""
        changements = []
        
        for nom_type, valeurs in seuils_bdd.items():
            if nom_type not in self.seuils_cache:
                changements.append({
                    'type': nom_type,
                    'action': 'nouveau',
                    'valeurs': valeurs
                })
            else:
                cache_vals = self.seuils_cache[nom_type]
                if (cache_vals['valeur_alerte_seuil'] != valeurs['valeur_alerte_seuil'] or
                    cache_vals['valeur_danger_seuil'] != valeurs['valeur_danger_seuil']):
                    changements.append({
                        'type': nom_type,
                        'action': 'modifie',
                        'ancien': cache_vals,
                        'nouveau': valeurs
                    })
        
        # Types supprimés
        for nom_type in list(self.seuils_cache.keys()):
            if nom_type not in seuils_bdd:
                changements.append({
                    'type': nom_type,
                    'action': 'supprime'
                })
        
        return changements
    
    def _envoyer_seuils_mqtt(self, seuils):
        """Envoie les seuils via MQTT"""
        try:
            payload = {
                'timestamp': datetime.now().isoformat(),
                'seuils': seuils
            }
            self.mqtt_client.publish("marais/seuils", json.dumps(payload))
            return True
        except Exception:
            return False
    
    def _verifier_et_envoyer(self):
        """Vérifie les seuils BDD et envoie uniquement si changement"""
        seuils_bdd = self._recuperer_seuils_bdd()
        
        if seuils_bdd is None:
            return
        
        changements = self._comparer_seuils(seuils_bdd)
        
        if changements:
            print(f"\n🔄 [SEUILS] {len(changements)} changement(s) détecté(s):")
            for chg in changements:
                if chg['action'] == 'nouveau':
                    print(f"   + {chg['type']}: alerte={chg['valeurs']['valeur_alerte_seuil']}, danger={chg['valeurs']['valeur_danger_seuil']}")
                elif chg['action'] == 'modifie':
                    print(f"   ~ {chg['type']}: alerte {chg['ancien']['valeur_alerte_seuil']}→{chg['nouveau']['valeur_alerte_seuil']}, danger {chg['ancien']['valeur_danger_seuil']}→{chg['nouveau']['valeur_danger_seuil']}")
                elif chg['action'] == 'supprime':
                    print(f"   - {chg['type']} supprimé")
            
            # Mettre à jour le cache
            self.seuils_cache = seuils_bdd
            self._sauvegarder_cache()
            
            # Envoyer les nouveaux seuils via MQTT
            if self._envoyer_seuils_mqtt(seuils_bdd):
                print(f"✅ [SEUILS] {len(seuils_bdd)} seuils envoyés sur marais/seuils\n")
    
    def _boucle_verification(self):
        """Boucle de vérification périodique"""
        while self.actif:
            try:
                self._verifier_et_envoyer()
                time.sleep(self.intervalle)
            except Exception:
                time.sleep(self.intervalle)
    
    def demarrer(self):
        """Démarre le service d'envoi des seuils"""
        if self.actif:
            return
        if not self._connecter_mqtt():
            return
        
        self.actif = True
        
        # Première vérification immédiate
        self._verifier_et_envoyer()
        
        # Boucle périodique
        self.thread = threading.Thread(target=self._boucle_verification, daemon=True)
        self.thread.start()
    
    def arreter(self):
        """Arrête le service"""
        self.actif = False
        if self.thread:
            self.thread.join(timeout=5)
        if self.mqtt_client:
            self.mqtt_client.loop_stop()
            self.mqtt_client.disconnect()
