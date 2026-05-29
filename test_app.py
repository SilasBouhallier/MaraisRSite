import unittest
import bcrypt
from app import verify_password
from app import app                        # Importe l'application Flask depuis app.py



class TestRoutes(unittest.TestCase):       # Définit une classe de tests pour les routes
    def setUp(self):                       # Méthode exécutée avant chaque test
        self.client = app.test_client()    # Crée un client de test (simule un navigateur)
        app.testing = True                 # Active le mode test (les erreurs s'affichent)

    def test_api_test_route(self):         # Test : vérifie que /api/test répond correctement
        response = self.client.get('/api/test')        # Envoie une requête GET à /api/test
        self.assertEqual(response.status_code, 200)    # Vérifie que le code HTTP est 200 (succès)
        self.assertEqual(response.json, {"message": "OK"})  # Vérifie que le JSON retourné est exactement {"message": "OK"}

class TestUserFunctions(unittest.TestCase):
    """
    Classe de test pour les fonctions utilitaires de l'utilisateur.
    Cette classe regroupe les tests qui vérifient le bon fonctionnement
    des fonctions liées aux mots de passe (hashage et vérification).
    """

    def test_verify_password_correct(self):
        """Teste la vérification d'un mot de passe correct."""
        plain_password = "mot_de_passe_123"                       # 1. Un mot de passe fictif en clair.
        # 1. Hash d'un mot de passe
        hashed = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())   # 2. On le hache avec bcrypt (encode en bytes, sel aléatoire).
        # 2. Vérification du mot de passe correct
        is_valid = verify_password(plain_password, hashed.decode())        # 3. On vérifie que le mot de passe correspond au hash.
        # 3. Assertion : Le résultat doit être True

        self.assertTrue(is_valid)                                          # 4. On s'assure que verify_password retourne True.

    def test_verify_password_incorrect(self):
        """Teste la vérification avec un mauvais mot de passe."""
        plain_password = "mot_de_passe_123"                       # 1. Un mot de passe fictif en clair.
        # 1. Hash du bon mot de passe
        hashed = bcrypt.hashpw(plain_password.encode(), bcrypt.gensalt())   # 2. On hache le bon mot de passe.
        # 2. Vérification avec un mauvais mot de passe
        is_valid = verify_password("wrong_password", hashed.decode())       # 3. On vérifie un mot de passe différent.
        # 3. Assertion : Le résultat doit être False
        self.assertFalse(is_valid)                                         # 4. On s'assure que verify_password retourne False.

    

if __name__ == "__main__":
    unittest.main()