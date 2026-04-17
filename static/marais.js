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

function editSonde(id) {
    const nouveauNom = prompt("Nouveau nom de la sonde :");
    if (!nouveauNom) return;
    fetch(`/api/sondes/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ nom: nouveauNom })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Sonde modifiée');
            location.reload();
        } else {
            alert('Erreur');
        }
    });
}

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
    const nouveauNom = prompt("Nouveau nom de l'alarme :");
    if (!nouveauNom) return;
    fetch(`/api/alarmes/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ nom: nouveauNom })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Alarme modifiée');
            location.reload();
        } else {
            alert('Erreur');
        }
    });
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
    alert(`Test de l'alarme ${id} (simulation)`);
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
        if (data.success) alert('Seuil mis à jour');
        else alert('Erreur lors de la mise à jour');
    })
    .catch(error => console.error('Erreur:', error));
}

function saveAllSeuils() {
    const rows = document.querySelectorAll('table tbody tr');
    const seuilsData = [];
    rows.forEach(row => {
        const idButton = row.querySelector('button[onclick^="saveSeuil"]');
        if (!idButton) return;
        const onclick = idButton.getAttribute('onclick');
        const match = onclick.match(/saveSeuil\((\d+)\)/);
        if (!match) return;
        const id = match[1];
        const inputs = row.querySelectorAll('input[type="number"]');
        if (inputs.length < 2) return;
        seuilsData.push({ id, alerte: inputs[1].value, danger: inputs[0].value });
    });
    if (seuilsData.length === 0) return alert('Aucun seuil à enregistrer');
    fetch('/api/seuils/all', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin',
        body: JSON.stringify({ seuils: seuilsData })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) alert('Tous les seuils ont été enregistrés');
        else alert('Erreur lors de l’enregistrement');
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