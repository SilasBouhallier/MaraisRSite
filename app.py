from flask import Flask, send_from_directory, request, session, redirect, url_for, make_response
import mysql.connector
import bcrypt
import logging
from functools import wraps

# Configuration des logs
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = 'une_cle_secrete_tres_longue_pour_la_session_2026'
app.config['SESSION_COOKIE_NAME'] = 'marais_session'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False  # True en production avec HTTPS
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.permanent_session_lifetime = 600  # 10 minutes

# Configuration de la base de données
DB_CONFIG = {
    'host': 'mariadb',
    'user': 'Marais_R_Site_User',
    'password': 'Marais_R_Site_User/123',
    'database': 'Marais_R_Site',
    'port': 3306,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}

# Fonctions de hashage avec bcrypt
def hash_password(password):
    """Génère un hash bcrypt (sel inclus)"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password, stored_hash):
    """Vérifie le mot de passe avec bcrypt"""
    return bcrypt.checkpw(password.encode(), stored_hash.encode())

# Connexion à la base de données
def get_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"Erreur BDD: {err}")
        return None

# Décorateur pour protéger les pages
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# Routes pour les fichiers statiques
@app.route('/')
def index():
    if 'user_id' in session:
        return send_from_directory('static', 'index.html')
    return redirect(url_for('login'))

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

# Route de connexion
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Départ propre : on vide toute session résiduelle
    session.clear()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return "<script>alert('Remplis tous les champs'); window.location.href='/login';</script>"

        conn = get_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            # On récupère l'utilisateur
            cursor.execute(
                "SELECT * FROM utilisateur WHERE nom_utilisateur = %s",
                (username,)
            )
            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user and verify_password(password, user['mot_de_passe_utilisateur']):
                session.permanent = True
                session['user_id'] = user['id_utilisateur']
                session['username'] = user['nom_utilisateur']
                session['role'] = user['role_utilisateur']
                app.logger.info("✅ Session créée avec succès")
                app.logger.info(session)
                return redirect(url_for('index'))
            else:
                return "<script>alert('Identifiants incorrects'); window.location.href='/login';</script>"
        else:
            return "<script>alert('Erreur de connexion BDD'); window.location.href='/login';</script>"

    return send_from_directory('static', 'login.html')

# Route de déconnexion
@app.route('/logout')
def logout():
    session.clear()
    response = redirect(url_for('login'))
    response.set_cookie('session', '', expires=0, path='/')
    response.set_cookie('marais_session', '', expires=0, path='/')
    return response

# Pages protégées
@app.route('/sondes.html')
@login_required
def sondes():
    return send_from_directory('static', 'sondes.html')

@app.route('/alarmes.html')
@login_required
def alarmes():
    return send_from_directory('static', 'alarmes.html')

@app.route('/seuils.html')
@login_required
def seuils():
    return send_from_directory('static', 'seuils.html')

@app.route('/settings.html')
@login_required
def settings():
    return send_from_directory('static', 'settings.html')

# API de test
@app.route('/api/test')
def test():
    return {"message": "OK"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)