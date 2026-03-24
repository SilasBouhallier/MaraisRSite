from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from database_manager import WebDatabaseManager
import json
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'votre_cle_secrete_ici'

# Initialisation du gestionnaire de base de données
db = WebDatabaseManager()

@app.route('/')
def index():
    """
    Page d'accueil avec aperçu des données.
    """
    try:
        stats = db.get_statistiques_mesures()
        recentes = db.get_mesures_recentes(24)
        emplacements = db.get_emplacements()
        
        return render_template('index.html', 
                             stats=stats, 
                             recentes=recentes, 
                             emplacements=emplacements)
    except Exception as e:
        flash(f'Erreur lors du chargement des données: {e}', 'error')
        return render_template('index.html', stats=None, recentes=[], emplacements=[])

@app.route('/dashboard')
def dashboard():
    """
    Tableau de bord analytique avec graphiques.
    """
    try:
        stats = db.get_statistiques_mesures()
        recentes = db.get_mesures_recentes(24)
        emplacements = db.get_emplacements()
        
        return render_template('dashboard.html', 
                             stats=stats, 
                             recentes=recentes, 
                             emplacements=emplacements)
    except Exception as e:
        flash(f'Erreur lors du chargement du dashboard: {e}', 'error')
        return render_template('dashboard.html', stats=None, recentes=[], emplacements=[])

@app.route('/realtime')
def realtime():
    """
    Page de monitoring en temps réel.
    """
    try:
        stats = db.get_statistiques_mesures()
        recentes = db.get_mesures_recentes(24)
        emplacements = db.get_emplacements()
        
        return render_template('realtime.html', 
                             stats=stats, 
                             recentes=recentes, 
                             emplacements=emplacements)
    except Exception as e:
        flash(f'Erreur lors du chargement du monitoring: {e}', 'error')
        return render_template('realtime.html', stats=None, recentes=[], emplacements=[])

@app.route('/analytics')
def analytics():
    """
    Page d'analytics avancées.
    """
    try:
        stats = db.get_statistiques_mesures()
        recentes = db.get_mesures_recentes(24)
        emplacements = db.get_emplacements()
        
        return render_template('analytics.html', 
                             stats=stats, 
                             recentes=recentes, 
                             emplacements=emplacements)
    except Exception as e:
        flash(f'Erreur lors du chargement des analytics: {e}', 'error')
        return render_template('analytics.html', stats=None, recentes=[], emplacements=[])

@app.route('/compare')
def compare():
    """
    Page de comparaison de périodes.
    """
    try:
        stats = db.get_statistiques_mesures()
        recentes = db.get_mesures_recentes(24)
        emplacements = db.get_emplacements()
        
        return render_template('compare.html', 
                             stats=stats, 
                             recentes=recentes, 
                             emplacements=emplacements)
    except Exception as e:
        flash(f'Erreur lors du chargement de la comparaison: {e}', 'error')
        return render_template('compare.html', stats=None, recentes=[], emplacements=[])

@app.route('/mesures')
def mesures():
    """
    Page affichant toutes les mesures.
    """
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 50
        offset = (page - 1) * per_page
        
        mesures = db.get_all_mesures(per_page)
        emplacements = db.get_emplacements()
        
        return render_template('mesures.html', 
                             mesures=mesures, 
                             emplacements=emplacements,
                             page=page)
    except Exception as e:
        flash(f'Erreur lors du chargement des mesures: {e}', 'error')
        return render_template('mesures.html', mesures=[], emplacements=[])

@app.route('/mesure/<int:id_mesure>')
def detail_mesure(id_mesure):
    """
    Détail d'une mesure spécifique.
    """
    try:
        mesures = db.get_all_mesures(1000)
        mesure = None
        for m in mesures:
            if m['id_mesure'] == id_mesure:
                mesure = m
                break
        
        if not mesure:
            flash('Mesure non trouvée', 'error')
            return redirect(url_for('mesures'))
        
        return render_template('detail_mesure.html', mesure=mesure)
    except Exception as e:
        flash(f'Erreur lors du chargement de la mesure: {e}', 'error')
        return redirect(url_for('mesures'))

@app.route('/emplacement/<int:id_emplacement>')
def detail_emplacement(id_emplacement):
    """
    Détail d'un emplacement avec ses mesures.
    """
    try:
        emplacements = db.get_emplacements()
        emplacement = None
        for emp in emplacements:
            if emp['id_emplacement'] == id_emplacement:
                emplacement = emp
                break
        
        if not emplacement:
            flash('Emplacement non trouvé', 'error')
            return redirect(url_for('index'))
        
        mesures = db.get_mesures_by_emplacement(id_emplacement, 100)
        
        return render_template('detail_emplacement.html', 
                             emplacement=emplacement, 
                             mesures=mesures)
    except Exception as e:
        flash(f'Erreur lors du chargement de l\'emplacement: {e}', 'error')
        return redirect(url_for('index'))

@app.route('/admin')
def admin():
    """
    Panneau d'administration.
    """
    try:
        emplacements = db.get_emplacements()
        sondes = db.get_sondes()
        types_mesure = db.get_types_mesure()
        alertes = db.get_alertes()
        types_emplacement = db.get_types_emplacement()
        
        return render_template('admin.html',
                             emplacements=emplacements,
                             sondes=sondes,
                             types_mesure=types_mesure,
                             alertes=alertes,
                             types_emplacement=types_emplacement)
    except Exception as e:
        flash(f'Erreur lors du chargement du panneau d\'administration: {e}', 'error')
        return render_template('admin.html')

# ==================== ROUTES D'ÉDITION ====================

@app.route('/edit/mesure/<int:id_mesure>', methods=['GET', 'POST'])
def edit_mesure(id_mesure):
    """
    Modifier une mesure.
    """
    if request.method == 'POST':
        try:
            nouvelle_valeur = request.form.get('valeur')
            nouvelle_date = request.form.get('date_heure')
            nouvel_id_alerte = request.form.get('id_alerte')
            
            # Conversion des types
            nouvelle_valeur = float(nouvelle_valeur) if nouvelle_valeur else None
            nouvel_id_alerte = int(nouvel_id_alerte) if nouvel_id_alerte else None
            
            success = db.update_mesure(
                id_mesure, 
                nouvelle_valeur=nouvelle_valeur,
                nouvelle_date=nouvelle_date,
                nouvel_id_alerte=nouvel_id_alerte
            )
            
            if success:
                flash('Mesure modifiée avec succès', 'success')
                return redirect(url_for('detail_mesure', id_mesure=id_mesure))
            else:
                flash('Erreur lors de la modification', 'error')
                
        except ValueError:
            flash('Valeurs invalides', 'error')
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
    
    # GET: afficher le formulaire
    try:
        mesures = db.get_all_mesures(1000)
        mesure = None
        for m in mesures:
            if m['id_mesure'] == id_mesure:
                mesure = m
                break
        
        if not mesure:
            flash('Mesure non trouvée', 'error')
            return redirect(url_for('mesures'))
        
        alertes = db.get_alertes()
        
        return render_template('edit_mesure.html', mesure=mesure, alertes=alertes)
    except Exception as e:
        flash(f'Erreur: {e}', 'error')
        return redirect(url_for('mesures'))

@app.route('/edit/emplacement/<int:id_emplacement>', methods=['GET', 'POST'])
def edit_emplacement(id_emplacement):
    """
    Modifier un emplacement.
    """
    if request.method == 'POST':
        try:
            nouveau_nom = request.form.get('nom')
            nouvel_id_type = request.form.get('id_type_emplacement')
            nouvel_id_sonde = request.form.get('id_sonde')
            
            # Conversion des types
            nouvel_id_type = int(nouvel_id_type) if nouvel_id_type else None
            nouvel_id_sonde = int(nouvel_id_sonde) if nouvel_id_sonde else None
            
            success = db.update_emplacement(
                id_emplacement,
                nouveau_nom=nouveau_nom,
                nouvel_id_type=nouvel_id_type,
                nouvel_id_sonde=nouvel_id_sonde
            )
            
            if success:
                flash('Emplacement modifié avec succès', 'success')
                return redirect(url_for('detail_emplacement', id_emplacement=id_emplacement))
            else:
                flash('Erreur lors de la modification', 'error')
                
        except ValueError:
            flash('Valeurs invalides', 'error')
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
    
    # GET: afficher le formulaire
    try:
        emplacements = db.get_emplacements()
        emplacement = None
        for emp in emplacements:
            if emp['id_emplacement'] == id_emplacement:
                emplacement = emp
                break
        
        if not emplacement:
            flash('Emplacement non trouvé', 'error')
            return redirect(url_for('admin'))
        
        sondes = db.get_sondes()
        types_emplacement = db.get_types_emplacement()
        
        return render_template('edit_emplacement.html', 
                             emplacement=emplacement,
                             sondes=sondes,
                             types_emplacement=types_emplacement)
    except Exception as e:
        flash(f'Erreur: {e}', 'error')
        return redirect(url_for('admin'))

@app.route('/edit/sonde/<int:id_sonde>', methods=['GET', 'POST'])
def edit_sonde(id_sonde):
    """
    Modifier une sonde.
    """
    if request.method == 'POST':
        try:
            nouveau_nom = request.form.get('nom')
            
            success = db.update_sonde(id_sonde, nouveau_nom)
            
            if success:
                flash('Sonde modifiée avec succès', 'success')
                return redirect(url_for('admin'))
            else:
                flash('Erreur lors de la modification', 'error')
                
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
    
    # GET: afficher le formulaire
    try:
        sondes = db.get_sondes()
        sonde = None
        for s in sondes:
            if s['id_sonde'] == id_sonde:
                sonde = s
                break
        
        if not sonde:
            flash('Sonde non trouvée', 'error')
            return redirect(url_for('admin'))
        
        return render_template('edit_sonde.html', sonde=sonde)
    except Exception as e:
        flash(f'Erreur: {e}', 'error')
        return redirect(url_for('admin'))

# ==================== ROUTES D'AJOUT ====================

@app.route('/add/mesure', methods=['GET', 'POST'])
def add_mesure():
    """
    Ajouter une nouvelle mesure.
    """
    if request.method == 'POST':
        try:
            valeur = float(request.form.get('valeur'))
            date_heure = request.form.get('date_heure')
            id_emplacement = int(request.form.get('id_emplacement'))
            id_alerte = int(request.form.get('id_alerte'))
            
            new_id = db.insert_mesure(valeur, date_heure, id_emplacement, id_alerte)
            
            if new_id:
                flash('Mesure ajoutée avec succès', 'success')
                return redirect(url_for('detail_mesure', id_mesure=new_id))
            else:
                flash('Erreur lors de l\'ajout', 'error')
                
        except ValueError:
            flash('Valeurs invalides', 'error')
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
    
    # GET: afficher le formulaire
    try:
        emplacements = db.get_emplacements()
        alertes = db.get_alertes()
        
        return render_template('add_mesure.html', 
                             emplacements=emplacements,
                             alertes=alertes)
    except Exception as e:
        flash(f'Erreur: {e}', 'error')
        return redirect(url_for('mesures'))

@app.route('/add/emplacement', methods=['GET', 'POST'])
def add_emplacement():
    """
    Ajouter un nouvel emplacement.
    """
    if request.method == 'POST':
        try:
            nom = request.form.get('nom')
            id_type_emplacement = int(request.form.get('id_type_emplacement'))
            id_sonde = int(request.form.get('id_sonde'))
            
            new_id = db.insert_emplacement(nom, id_type_emplacement, id_sonde)
            
            if new_id:
                flash('Emplacement ajouté avec succès', 'success')
                return redirect(url_for('detail_emplacement', id_emplacement=new_id))
            else:
                flash('Erreur lors de l\'ajout', 'error')
                
        except ValueError:
            flash('Valeurs invalides', 'error')
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
    
    # GET: afficher le formulaire
    try:
        sondes = db.get_sondes()
        types_emplacement = db.get_types_emplacement()
        
        return render_template('add_emplacement.html',
                             sondes=sondes,
                             types_emplacement=types_emplacement)
    except Exception as e:
        flash(f'Erreur: {e}', 'error')
        return redirect(url_for('admin'))

@app.route('/add/sonde', methods=['GET', 'POST'])
def add_sonde():
    """
    Ajouter une nouvelle sonde.
    """
    if request.method == 'POST':
        try:
            nom = request.form.get('nom')
            
            new_id = db.insert_sonde(nom)
            
            if new_id:
                flash('Sonde ajoutée avec succès', 'success')
                return redirect(url_for('admin'))
            else:
                flash('Erreur lors de l\'ajout', 'error')
                
        except Exception as e:
            flash(f'Erreur: {e}', 'error')
    
    return render_template('add_sonde.html')

# ==================== ROUTES DE SUPPRESSION ====================

@app.route('/delete/mesure/<int:id_mesure>', methods=['POST'])
def delete_mesure(id_mesure):
    """
    Supprimer une mesure.
    """
    try:
        success = db.delete_mesure(id_mesure)
        
        if success:
            flash('Mesure supprimée avec succès', 'success')
        else:
            flash('Erreur lors de la suppression', 'error')
            
    except Exception as e:
        flash(f'Erreur: {e}', 'error')
    
    return redirect(url_for('mesures'))

@app.route('/delete/emplacement/<int:id_emplacement>', methods=['POST'])
def delete_emplacement(id_emplacement):
    """
    Supprimer un emplacement.
    """
    try:
        success = db.delete_emplacement(id_emplacement)
        
        if success:
            flash('Emplacement supprimé avec succès', 'success')
        else:
            flash('Erreur lors de la suppression (possible contrainte de clé étrangère)', 'error')
            
    except Exception as e:
        flash(f'Erreur: {e}', 'error')
    
    return redirect(url_for('admin'))

# ==================== API JSON ====================

@app.route('/api/mesures')
def api_mesures():
    """
    API pour récupérer les mesures au format JSON.
    """
    try:
        id_emplacement = request.args.get('id_emplacement', type=int)
        limite = request.args.get('limite', 100, type=int)
        
        if id_emplacement:
            mesures = db.get_mesures_by_emplacement(id_emplacement, limite)
        else:
            mesures = db.get_all_mesures(limite)
        
        # Conversion des datetime en string
        for mesure in mesures:
            if 'date_heure_mesure' in mesure and mesure['date_heure_mesure']:
                mesure['date_heure_mesure'] = mesure['date_heure_mesure'].isoformat()
        
        return jsonify(mesures)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/statistiques')
def api_statistiques():
    """
    API pour récupérer les statistiques.
    """
    try:
        stats = db.get_statistiques_mesures()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/export/mesures')
def api_export_mesures():
    """
    API pour exporter les mesures en JSON.
    """
    try:
        id_emplacement = request.args.get('id_emplacement', type=int)
        json_data = db.export_mesures_json(id_emplacement)
        
        response = app.response_class(
            response=json_data,
            status=200,
            mimetype='application/json'
        )
        
        filename = f"mesures_{id_emplacement if id_emplacement else 'all'}.json"
        response.headers['Content-Disposition'] = f'attachment; filename={filename}'
        
        return response
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ==================== GESTION D'ERREURS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Démarrage de l'application
    app.run(debug=True, host='0.0.0.0', port=5000)
