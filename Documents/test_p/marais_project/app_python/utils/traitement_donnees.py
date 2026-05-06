import json


class TraitementDonnees:

    @staticmethod
    def tester_seuil(donnees):
        """Teste le seuil"""
        pass

    @staticmethod
    def extraire_mac(topic):
        """Extrait le MAC de l'adresse MQTT"""
        # Prendre le dernier segment du topic
        last_segment = topic.split("/")[-1]
        # Vérifier si c'est un format MAC (contient des :)
        if ":" in last_segment:
            return last_segment
        # Sinon chercher un MAC dans tout le topic
        import re
        mac_match = re.search(r'[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}:[0-9a-fA-F]{2}', topic)
        if mac_match:
            return mac_match.group(0)
        return None

    @staticmethod
    def extraire_donnees(message):
        try:
            # Supprimer les espaces et newlines au début
            message = message.strip()
            
            # Format avec = : "MAC = {...}"
            if '=' in message:
                parts = message.split('=', 1)
                mac = parts[0].strip()
                json_part = parts[1].strip()
            else:
                # Format sans = : juste le JSON
                mac = None  # Sera extrait du topic
                json_part = message
            
            # Parser le JSON
            data = json.loads(json_part)
            
            # Extraire les champs
            timestamp = data.get("timestamp")
            mesures = data.get("mesure")
            
            if mesures is None:
                return None, None, None
            
            # Convertir en liste si c'est un dict
            if isinstance(mesures, dict):
                mesures = [mesures]
            
            return mesures, timestamp, mac

        except (json.JSONDecodeError, KeyError) as e:
            return None, None, None
