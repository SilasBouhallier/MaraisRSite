-- Requête SQL pour tester dans phpMyAdmin
-- Remplacer '62:03:57:41:38:23' par le nom de sonde souhaité

SELECT e.id_emplacement
FROM emplacement e
JOIN sonde s ON e.id_sonde = s.id_sonde
WHERE s.nom_sonde = '62:03:57:41:38:23';
