// ============================================
// Marais'R'Site - Fonctions personnalisées
// ============================================

// === GESTION DES MODALS ===
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = 'flex';
}
function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) modal.style.display = 'none';
}

// === SONDES ===
function addSonde() {
    const nom = document.getElementById('sondeNom')?.value;
    const localisation = document.getElementById('sondeLocalisation')?.value;
    const machine = document.getElementById('sondeMachine')?.value;
    if (!nom || !localisation || !machine) {
        alert('Veuillez remplir tous les champs');
        return;
    }
    fetch('/api/sondes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ nom, localisation, machine })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Sonde ajoutée');
            location.reload();
        } else {
            alert('Erreur : ' + (data.error || 'inconnue'));
        }
    });
}

// Ancienne fonction editSonde (remplacée par openEditSondeModal, on la garde pour compatibilité mais elle ne sera plus utilisée)
// function editSonde(id) { ... }  // on peut la supprimer ou la commenter

function deleteSonde(id) {
    if (confirm('Supprimer cette sonde ?')) {
        fetch(`/api/sondes/${id}`, {
            method: 'DELETE',
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Sonde supprimée');
                location.reload();
            } else {
                alert('Erreur');
            }
        });
    }
}

// NOUVELLES FONCTIONS POUR L'ÉDITION COMPLÈTE DES SONDES
function openEditSondeModal(id) {
    fetch(`/api/sondes/${id}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('editSondeId').value = data.sonde.id_sonde;
                document.getElementById('editSondeNom').value = data.sonde.nom_sonde || '';
                document.getElementById('editSondeLocalisation').value = data.sonde.localisation_principale || '';
                document.getElementById('editSondeZone').value = data.sonde.nom_emplacement || '';
                openModal('editSondeModal');
            } else {
                alert('Erreur : ' + (data.error || 'Impossible de charger la sonde'));
            }
        })
        .catch(err => alert('Erreur réseau lors du chargement de la sonde'));
}

function submitEditSonde() {
    const id = document.getElementById('editSondeId').value;
    const nom = document.getElementById('editSondeNom').value;
    const localisation_principale = document.getElementById('editSondeLocalisation').value;
    const nom_emplacement = document.getElementById('editSondeZone').value;

    fetch(`/api/sondes/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ nom, localisation_principale, nom_emplacement })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Sonde modifiée avec succès');
            location.reload();
        } else {
            alert('Erreur : ' + (data.error || 'Modification échouée'));
        }
    })
    .catch(err => alert('Erreur réseau lors de la modification'));
}

// === ALARMES ===
function addAlarme() {
    const nom = document.getElementById('alarmeNom')?.value;
    const id_emplacement = document.getElementById('alarmeEmplacement')?.value;
    if (!nom) {
        alert('Veuillez entrer un nom');
        return;
    }
    fetch('/api/alarmes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ nom, id_emplacement: id_emplacement || null })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Alarme ajoutée');
            location.reload();
        } else {
            alert('Erreur : ' + (data.error || 'inconnue'));
        }
    });
}

function editAlarme(id) {
    // Récupérer les données actuelles de l'alarme (nom et emplacement)
    fetch(`/api/alarmes/${id}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                document.getElementById('editAlarmeId').value = data.alarme.id_alarme;
                document.getElementById('editAlarmeNom').value = data.alarme.nom_alarme || '';
                // Sélectionner l'emplacement actuel dans le select
                const select = document.getElementById('editAlarmeEmplacement');
                select.value = data.alarme.id_emplacement || '';
                openModal('editAlarmeModal');
            } else {
                alert('Erreur : ' + (data.error || 'Impossible de charger l\'alarme'));
            }
        })
        .catch(err => alert('Erreur réseau lors du chargement de l\'alarme'));
}

function submitEditAlarme() {
    const id = document.getElementById('editAlarmeId').value;
    const nom = document.getElementById('editAlarmeNom').value;
    const id_emplacement = document.getElementById('editAlarmeEmplacement').value;

    if (!nom) {
        alert('Le nom de l\'alarme est requis');
        return;
    }

    fetch(`/api/alarmes/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ 
            nom: nom,
            id_emplacement: id_emplacement || null
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Alarme modifiée');
            location.reload();
        } else {
            alert('Erreur : ' + (data.error || 'Modification échouée'));
        }
    })
    .catch(err => alert('Erreur réseau lors de la modification'));
}

function deleteAlarme(id) {
    if (confirm('Supprimer cette alarme ?')) {
        fetch(`/api/alarmes/${id}`, {
            method: 'DELETE',
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Alarme supprimée');
                location.reload();
            } else {
                alert('Erreur');
            }
        });
    }
}

function testAlarme(id) {
    fetch('/api/alarmes/test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id_alarme: id })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(`✅ Commande envoyée pour l’alarme ${id}`);
        } else {
            alert(`❌ Erreur : ${data.error || "Échec de l'envoi"}`);
        }
    })
    .catch(error => {
        console.error('Erreur réseau :', error);
        alert('❌ Impossible de contacter le serveur');
    });
}

// === SEUILS ===
function saveSeuil(id) {
    const row = document.querySelector(`button[onclick="saveSeuil(${id})"]`)?.closest('tr');
    if (!row) return console.error('Ligne introuvable');
    const inputs = row.querySelectorAll('input[type="number"]');
    if (inputs.length < 2) return console.error('Champs non trouvés');
    const alerte = inputs[0].value;
    const danger = inputs[1].value;
    fetch(`/api/seuils/${id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ alerte, danger })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success)  alert('Seuil mis à jour');
        else alert('Erreur lors de la mise à jour');
    })
    .catch(error => console.error('Erreur:', error));
}

// === FERMETURE MODAL PAR CLIC EXTÉRIEUR ===
window.addEventListener('click', function(event) {
    if (event.target.classList?.contains('modal')) event.target.style.display = 'none';
});

// === INITIALISATION ===
document.addEventListener('DOMContentLoaded', function() {
    console.log('Marais\'R\'Site JS chargé');
    const path = window.location.pathname;
    if (path.includes('sondes.html')) console.log('Page sondes détectée');
    if (path.includes('alarmes.html')) console.log('Page alarmes détectée');
    if (path.includes('seuils.html')) console.log('Page seuils détectée');
});