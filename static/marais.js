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
    
    // Activer le select
    machineSelect.disabled = false;
    machineSelect.innerHTML = '';
    
    // Options selon localisation
    const options = {
        'Atelier bois': [
            'Scie circulaire',
            'Dégauchisseuse',
            'Toupie',
            'Ponceuse'
        ],
        'Zone peinture': [
            'Cabine peinture',
            'Table préparation',
            'Zone séchage'
        ],
        'Zone collage': [
            'Presse à bois',
            'Table encollage',
            'Zone serrage'
        ]
    };
    
    if (localisation && options[localisation]) {
        machineSelect.innerHTML = '<option value="">Sélectionner</option>';
        options[localisation].forEach(machine => {
            machineSelect.innerHTML += `<option value="${machine}">${machine}</option>`;
        });
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
    
    // Activer le select
    machineSelect.disabled = false;
    machineSelect.innerHTML = '';
    
    // Options selon localisation (mêmes que pour sondes)
    const options = {
        'Atelier bois': [
            'Scie circulaire',
            'Dégauchisseuse',
            'Toupie',
            'Ponceuse'
        ],
        'Zone peinture': [
            'Cabine peinture',
            'Table préparation',
            'Zone séchage'
        ],
        'Zone collage': [
            'Presse à bois',
            'Table encollage',
            'Zone serrage'
        ]
    };
    
    if (localisation && options[localisation]) {
        machineSelect.innerHTML = '<option value="">Sélectionner</option>';
        options[localisation].forEach(machine => {
            machineSelect.innerHTML += `<option value="${machine}">${machine}</option>`;
        });
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
    
    // Ici tu pourras plus tard envoyer à la BDD
    console.log('Alarme ajoutée :', { ref, localisation, machine });
    alert('Alarme ajoutée avec succès !');
    closeModal('alarmeModal');
}

// === PAGE SEUILS : Enregistrer un seuil individuel ===
function saveSeuil(sondeId, type) {
    // À compléter plus tard
    console.log('Seuil enregistré pour :', sondeId, type);
    alert('Seuil enregistré !');
}

// === PAGE SEUILS : Enregistrer tous les seuils ===
function saveAllSeuils() {
    // À compléter plus tard
    console.log('Tous les seuils enregistrés');
    alert('Tous les seuils ont été enregistrés !');
}

// === FERMETURE DES MODALS en cliquant à l'extérieur ===
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