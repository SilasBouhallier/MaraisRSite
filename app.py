from flask import Flask, send_from_directory, request, session, redirect, url_for, make_response, render_template, jsonify
import mysql.connector
import bcrypt
import logging
from functools import wraps

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.secret_key = 'une_cle_secrete_tres_longue_pour_la_session_2026'
app.config['SESSION_COOKIE_NAME'] = 'marais_session'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.permanent_session_lifetime = 600

DB_CONFIG = {
    'host': 'mariadb',
    'user': 'Marais_R_Site_User',
    'password': 'Marais_R_Site_User/123',
    'database': 'Marais_R_Site',
    'port': 3306,
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci'
}

def hash_password(password):
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()

def verify_password(password, stored_hash):
    return bcrypt.checkpw(password.encode(), stored_hash.encode())

def get_db():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        print(f"Erreur BDD: {err}")
        return None

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    
    # Nombre de sondes
    cursor.execute("SELECT COUNT(*) as total FROM sonde")
    nb_sondes = cursor.fetchone()['total']
    # Nombre d'alarmes
    cursor.execute("SELECT COUNT(*) as total FROM alarme")
    nb_alarmes = cursor.fetchone()['total']
    # Nombre de seuils
    cursor.execute("SELECT COUNT(*) as total FROM type_info_mesure")
    nb_seuils = cursor.fetchone()['total']
    
    # 5 dernières mesures avec le type de mesure
    cursor.execute("""
        SELECT m.valeur_mesure, m.date_heure_mesure, t.nom_type_mesure, e.nom_emplacement
        FROM mesure m
        JOIN type_info_mesure t ON m.id_type_mesure = t.id_type_mesure
        LEFT JOIN emplacement e ON m.id_emplacement = e.id_emplacement
        ORDER BY m.date_heure_mesure DESC
        LIMIT 5
    """)
    mesures = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return render_template('index.html',
                           nb_sondes=nb_sondes,
                           nb_alarmes=nb_alarmes,
                           nb_seuils=nb_seuils,
                           mesures=mesures)

@app.route('/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return "<script>alert('Remplis tous les champs'); window.location.href='/login';</script>"
        conn = get_db()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM utilisateur WHERE nom_utilisateur = %s", (username,))
            user = cursor.fetchone()
            cursor.close()
            conn.close()
            if user and verify_password(password, user['mot_de_passe_utilisateur']):
                session.permanent = True
                session['user_id'] = user['id_utilisateur']
                session['username'] = user['nom_utilisateur']
                session['role'] = user['role_utilisateur']
                return redirect(url_for('index'))
            else:
                return "<script>alert('Identifiants incorrects'); window.location.href='/login';</script>"
        else:
            return "<script>alert('Erreur de connexion BDD'); window.location.href='/login';</script>"
    return send_from_directory('static', 'login.html')

@app.route('/logout')
def logout():
    session.clear()
    response = redirect(url_for('login'))
    response.set_cookie('session', '', expires=0, path='/')
    response.set_cookie('marais_session', '', expires=0, path='/')
    return response

# ========== SEUILS ==========
@app.route('/seuils.html')
@login_required
def seuils():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM type_info_mesure")
    seuils = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('seuils.html', seuils=seuils)

@app.route('/api/seuils/<int:id_type_mesure>', methods=['POST'])
@login_required
def update_seuil(id_type_mesure):
    data = request.get_json()
    alerte = data.get('alerte')
    danger = data.get('danger')
    if alerte is None or danger is None:
        return jsonify({'error': 'Valeurs manquantes'}), 400
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE type_info_mesure
        SET valeur_alerte_seuil = %s, valeur_danger_seuil = %s
        WHERE id_type_mesure = %s
    """, (alerte, danger, id_type_mesure))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/seuils/all', methods=['POST'])
@login_required
def update_all_seuils():
    data = request.get_json()
    seuils = data.get('seuils', [])
    if not seuils:
        return jsonify({'error': 'Aucune donnée'}), 400
    conn = get_db()
    cursor = conn.cursor()
    for s in seuils:
        cursor.execute("""
            UPDATE type_info_mesure
            SET valeur_alerte_seuil = %s, valeur_danger_seuil = %s
            WHERE id_type_mesure = %s
        """, (s['alerte'], s['danger'], s['id']))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

# ========== SONDES ==========
@app.route('/sondes.html')
@login_required
def sondes():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT s.id_sonde, s.nom_sonde, e.nom_emplacement
        FROM sonde s
        LEFT JOIN emplacement e ON s.id_sonde = e.id_sonde
    """)
    sondes = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('sondes.html', sondes=sondes)

@app.route('/api/sondes', methods=['POST'])
@login_required
def add_sonde():
    data = request.get_json()
    nom = data.get('nom')
    localisation = data.get('localisation')
    machine = data.get('machine')
    if not nom or not localisation or not machine:
        return jsonify({'success': False, 'error': 'Champs manquants'}), 400
    type_mapping = {'Atelier bois': 1, 'Zone peinture': 2, 'Zone collage': 2}
    id_type = type_mapping.get(localisation, 1)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO sonde (nom_sonde) VALUES (%s)", (nom,))
    sonde_id = cursor.lastrowid
    cursor.execute("""
        INSERT INTO emplacement (nom_emplacement, id_type_emplacement, id_sonde)
        VALUES (%s, %s, %s)
    """, (machine, id_type, sonde_id))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True, 'id': sonde_id})

@app.route('/api/sondes/<int:id_sonde>', methods=['PUT'])
@login_required
def update_sonde(id_sonde):
    data = request.get_json()
    nom = data.get('nom')
    if not nom:
        return jsonify({'success': False, 'error': 'Nom manquant'}), 400
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE sonde SET nom_sonde = %s WHERE id_sonde = %s", (nom, id_sonde))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/sondes/<int:id_sonde>', methods=['DELETE'])
@login_required
def delete_sonde(id_sonde):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM emplacement WHERE id_sonde = %s", (id_sonde,))
    cursor.execute("DELETE FROM sonde WHERE id_sonde = %s", (id_sonde,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

# ========== ALARMES ==========
@app.route('/alarmes.html')
@login_required
def alarmes():
    conn = get_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT a.id_alarme, a.nom_alarme, e.nom_emplacement
        FROM alarme a
        LEFT JOIN emplacement e ON a.id_alarme = e.id_alarme
    """)
    alarmes = cursor.fetchall()
    cursor.execute("SELECT id_emplacement, nom_emplacement FROM emplacement")
    emplacements = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('alarmes.html', alarmes=alarmes, emplacements=emplacements)

@app.route('/api/alarmes', methods=['POST'])
@login_required
def add_alarme():
    data = request.get_json()
    nom = data.get('nom')
    id_emplacement = data.get('id_emplacement')
    if not nom:
        return jsonify({'success': False, 'error': 'Nom manquant'}), 400
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO alarme (nom_alarme) VALUES (%s)", (nom,))
    alarme_id = cursor.lastrowid
    if id_emplacement:
        cursor.execute("""
            INSERT INTO installe (id_alarme, id_emplacement)
            VALUES (%s, %s)
        """, (alarme_id, id_emplacement))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/alarmes/<int:id_alarme>', methods=['PUT'])
@login_required
def update_alarme(id_alarme):
    data = request.get_json()
    nom = data.get('nom')
    if not nom:
        return jsonify({'success': False, 'error': 'Nom manquant'}), 400
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE alarme SET nom_alarme = %s WHERE id_alarme = %s", (nom, id_alarme))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/alarmes/<int:id_alarme>', methods=['DELETE'])
@login_required
def delete_alarme(id_alarme):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM installe WHERE id_alarme = %s", (id_alarme,))
    cursor.execute("DELETE FROM alarme WHERE id_alarme = %s", (id_alarme,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True})

# ========== AUTRES ==========
@app.route('/settings.html')
@login_required
def settings():
    return send_from_directory('static', 'settings.html')

@app.route('/api/test')
def test():
    return {"message": "OK"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)