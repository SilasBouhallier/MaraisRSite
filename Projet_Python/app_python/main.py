import sys
import os
import signal
import logging
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '.env'), override=True)

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.application import Application

def signal_handler(signum, frame):
    """Gestionnaire de signaux pour arrêt propre."""
    print(f"Signal reçu: {signum}")
    if 'app' in globals():
        app.stop()
    sys.exit(0)

def main():
    """Fonction principale avec gestion des erreurs."""
    global app
    
    # Configuration du logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)
    
    try:
        # Configuration des signaux
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Initialisation de l'application
        logger.info("Initialisation de l'application...")
        app = Application("utils/configuration.cfg")
        
        # Démarrage
        logger.info("Démarrage de l'application...")
        app.start()
        
    except FileNotFoundError as e:
        logger.error(f"Fichier de configuration non trouvé: {e}")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Erreur lors du démarrage: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
