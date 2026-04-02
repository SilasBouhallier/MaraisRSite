// ============================================
// Marais'R'Site - Fonctions personnalisées
// ============================================

// === GESTION DES MODALS (Commun à toutes les pages) ===
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

// === PAGE SONDES : Mise à jour des machines selon localisation ===
function updateMachineOptions() {
    const localisation = document.getElementById('sondeLocalisation')?.value;
    const machineSelect = document.getElementById('sondeMachine');
    
    if (!machineSelect) return;
    
    machineSelect.disabled = false;
    machineSelect.innerHTML = '';
    
    const options = {
        'Atelier bois': ['Scie circulaire', 'Dégauchisseuse', 'Toupie', 'Ponceuse'],
        'Zone peinture': ['Cabine peinture', 'Table préparation', 'Zone séchage'],
        'Zone collage': ['Presse à bois', 'Table encollage', 'Zone serrage']
    };
    
    if (localisation && options[localisation]) {
        machineSelect.innerHTML = '<option value="">Sélectionner</option>' +
            options[localisation].map(m => `<option value="${m}">${m}</option>`).join('');
    } else {
        machineSelect.disabled = true;
        machineSelect.innerHTML = '<option value="">Choisir d\'abord la localisation</option>';
    }
}

// === PAGE SONDES : Ajouter une sonde ===
function addSonde() {
    const ref = document.getElementById('sondeRef')?.value;
    const localisation = document.getElementById('sondeLocalisation')?.value;
    const machine = document.getElementById('sondeMachine')?.value;
    
    if (!ref || !localisation || !machine) {
        alert('Veuillez remplir tous les champs');
        return;
    }
    
    // Ici tu pourras plus tard envoyer à la BDD
    console.log('Sonde ajoutée :', { ref, localisation, machine });
    alert('Sonde ajoutée avec succès !');
    closeModal('sondeModal');
}

// === PAGE ALARMES : Mise à jour des machines selon localisation ===
function updateAlarmeMachineOptions() {
    const localisation = document.getElementById('alarmeLocalisation')?.value;
    const machineSelect = document.getElementById('alarmeMachine');
    
    if (!machineSelect) return;
    
    machineSelect.disabled = false;
    machineSelect.innerHTML = '';
    
    const options = {
        'Atelier bois': ['Scie circulaire', 'Dégauchisseuse', 'Toupie', 'Ponceuse'],
        'Zone peinture': ['Cabine peinture', 'Table préparation', 'Zone séchage'],
        'Zone collage': ['Presse à bois', 'Table encollage', 'Zone serrage']
    };
    
    if (localisation && options[localisation]) {
        machineSelect.innerHTML = '<option value="">Sélectionner</option>' +
            options[localisation].map(m => `<option value="${m}">${m}</option>`).join('');
    } else {
        machineSelect.disabled = true;
        machineSelect.innerHTML = '<option value="">Choisir d\'abord la localisation</option>';
    }
}

// === PAGE ALARMES : Ajouter une alarme ===
function addAlarme() {
    const ref = document.getElementById('alarmeRef')?.value;
    const localisation = document.getElementById('alarmeLocalisation')?.value;
    const machine = document.getElementById('alarmeMachine')?.value;
    
    if (!ref || !localisation || !machine) {
        alert('Veuillez remplir tous les champs');
        return;
    }
    
    console.log('Alarme ajoutée :', { ref, localisation, machine });
    alert('Alarme ajoutée avec succès !');
    closeModal('alarmeModal');
}

// === PAGE SEUILS : Enregistrer un seul seuil ===
function saveSeuil(id) {
    // Récupère la ligne correspondante
    const row = document.querySelector(`button[onclick="saveSeuil(${id})"]`)?.closest('tr');
    if (!row) {
        console.error('Ligne introuvable');
        return;
    }
    
    // Récupère les deux champs de saisie (alerte et danger)
    const inputs = row.querySelectorAll('input[type="number"]');
    if (inputs.length < 2) {
        console.error('Champs non trouvés');
        return;
    }
    
    const alerte = inputs[0].value;
    const danger = inputs[1].value;
    
    fetch(`/api/seuils/${id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ alerte, danger })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Seuil mis à jour');
        } else {
            alert('Erreur lors de la mise à jour');
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        alert('Erreur de communication avec le serveur');
    });
}

// === PAGE SEUILS : Enregistrer tous les seuils ===
function saveAllSeuils() {
    const rows = document.querySelectorAll('table tbody tr');
    const seuilsData = [];
    
    rows.forEach(row => {
        const idButton = row.querySelector('button[onclick^="saveSeuil"]');
        if (!idButton) return;
        
        // Extraire l'id du bouton
        const onclick = idButton.getAttribute('onclick');
        const match = onclick.match(/saveSeuil\((\d+)\)/);
        if (!match) return;
        
        const id = match[1];
        const inputs = row.querySelectorAll('input[type="number"]');
        if (inputs.length < 2) return;
        
        seuilsData.push({
            id: id,
            alerte: inputs[1].value,
            danger: inputs[0].value
        });
    });
    
    if (seuilsData.length === 0) {
        alert('Aucun seuil à enregistrer');
        return;
    }
    
    fetch('/api/seuils/all', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ seuils: seuilsData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Tous les seuils ont été enregistrés');
        } else {
            alert('Erreur lors de l’enregistrement');
        }
    })
    .catch(error => {
        console.error('Erreur:', error);
        alert('Erreur de communication avec le serveur');
    });
}

// === FERMETURE DES MODALS en cliquant à l’extérieur ===
window.addEventListener('click', function(event) {
    if (event.target.classList?.contains('modal')) {
        event.target.style.display = 'none';
    }
});

// === INITIALISATION AU CHARGEMENT DE LA PAGE ===
document.addEventListener('DOMContentLoaded', function() {
    console.log('Marais\'R\'Site JS chargé');
    
    // Vérifier sur quelle page on est
    const path = window.location.pathname;
    
    if (path.includes('sondes.html')) {
        console.log('Page sondes détectée');
        // Initialisations spécifiques aux sondes si besoin
    }
    
    if (path.includes('alarmes.html')) {
        console.log('Page alarmes détectée');
        // Initialisations spécifiques aux alarmes si besoin
    }
    
    if (path.includes('seuils.html')) {
        console.log('Page seuils détectée');
        // Initialisations spécifiques aux seuils si besoin
    }
});