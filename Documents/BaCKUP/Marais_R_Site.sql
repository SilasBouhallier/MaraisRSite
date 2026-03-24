-- phpMyAdmin SQL Dump
-- version 5.2.3
-- https://www.phpmyadmin.net/
--
-- Hôte : mariadb
-- Généré le : lun. 23 mars 2026 à 15:29
-- Version du serveur : 10.11.16-MariaDB-ubu2204
-- Version de PHP : 8.3.26

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `Marais_R_Site`
--

-- --------------------------------------------------------

--
-- Structure de la table `alarme`
--

CREATE TABLE `alarme` (
  `id_alarme` int(11) NOT NULL,
  `nom_alarme` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `alarme`
--

INSERT INTO `alarme` (`id_alarme`, `nom_alarme`) VALUES
(1, 'BBB'),
(2, 'BBBB');

-- --------------------------------------------------------

--
-- Structure de la table `alerte`
--

CREATE TABLE `alerte` (
  `id_alerte` int(11) NOT NULL,
  `nom_alerte` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `alerte`
--

INSERT INTO `alerte` (`id_alerte`, `nom_alerte`) VALUES
(1, 'normal'),
(2, 'Attention'),
(3, 'Danger');

-- --------------------------------------------------------

--
-- Structure de la table `archive_moyennes_mensuelles`
--

CREATE TABLE `archive_moyennes_mensuelles` (
  `id_archive` int(11) NOT NULL,
  `date_jour` date NOT NULL,
  `id_emplacement` int(11) NOT NULL,
  `moyenne_valeur` float NOT NULL,
  `max_valeur` float NOT NULL,
  `min_valeur` float NOT NULL,
  `nb_mesures_compactees` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `archive_moyennes_mensuelles`
--

INSERT INTO `archive_moyennes_mensuelles` (`id_archive`, `date_jour`, `id_emplacement`, `moyenne_valeur`, `max_valeur`, `min_valeur`, `nb_mesures_compactees`) VALUES
(69, '2025-12-02', 3, 49.0161, 49.0161, 49.0161, 1),
(70, '2025-12-03', 3, 44.6806, 45.4838, 43.8775, 2),
(71, '2025-12-04', 2, 32.8104, 32.8104, 32.8104, 1),
(72, '2025-12-05', 3, 39.9631, 49.4155, 30.5108, 2),
(73, '2025-12-07', 1, 858.955, 949.472, 738.865, 3),
(74, '2025-12-12', 2, 7.74021, 7.74021, 7.74021, 1),
(75, '2025-12-13', 1, 923.694, 923.694, 923.694, 1),
(76, '2025-12-14', 2, 21.8998, 21.8998, 21.8998, 1),
(77, '2025-12-15', 3, 35.1151, 35.1151, 35.1151, 1),
(78, '2025-12-17', 3, 47.8661, 56.7705, 38.9617, 2),
(79, '2025-12-19', 2, 29.7521, 29.7521, 29.7521, 1),
(80, '2025-12-20', 2, 5.85042, 5.85042, 5.85042, 1),
(81, '2025-12-20', 3, 36.9073, 36.9073, 36.9073, 1),
(82, '2025-12-22', 2, 12.1033, 12.1033, 12.1033, 1),
(83, '2025-12-23', 2, 12.5302, 12.5302, 12.5302, 1),
(84, '2025-12-23', 3, 30.3475, 30.3475, 30.3475, 1),
(85, '2025-12-24', 1, 504.732, 504.732, 504.732, 1),
(86, '2025-12-24', 2, 34.0434, 34.0434, 34.0434, 1),
(87, '2025-12-24', 3, 27.9373, 46.5148, 10.7352, 3),
(88, '2025-12-29', 1, 698.61, 698.61, 698.61, 1),
(89, '2025-12-30', 2, 26.2743, 26.2743, 26.2743, 1),
(90, '2025-12-30', 3, 34.1249, 34.1249, 34.1249, 1),
(91, '2025-12-31', 1, 666.756, 666.756, 666.756, 1),
(92, '2026-01-01', 1, 600.37, 600.37, 600.37, 1),
(93, '2026-01-01', 2, 22.6718, 32.8141, 12.5295, 2),
(94, '2026-01-01', 3, 42.3451, 47.4668, 37.2235, 2),
(95, '2026-01-02', 3, 58.5343, 58.5343, 58.5343, 1),
(96, '2026-01-03', 1, 969.777, 969.777, 969.777, 1),
(97, '2026-01-03', 2, 26.7122, 26.7122, 26.7122, 1),
(98, '2026-01-04', 2, 27.7053, 27.7053, 27.7053, 1),
(99, '2026-01-06', 1, 691.005, 691.005, 691.005, 1),
(100, '2026-01-06', 2, 30.0992, 30.0992, 30.0992, 1),
(101, '2026-01-06', 3, 51.7752, 51.7752, 51.7752, 1),
(102, '2026-01-07', 2, 15.1026, 15.1026, 15.1026, 1),
(103, '2026-01-11', 2, 18.9456, 18.9456, 18.9456, 1),
(104, '2026-01-11', 3, 14.1486, 14.1486, 14.1486, 1),
(105, '2026-01-12', 1, 398.357, 398.357, 398.357, 1),
(106, '2026-01-12', 3, 22.9273, 22.9273, 22.9273, 1),
(107, '2026-01-13', 3, 11.4887, 11.4887, 11.4887, 1),
(108, '2026-01-14', 1, 686.532, 686.532, 686.532, 1),
(109, '2026-01-15', 2, 21.9383, 21.9383, 21.9383, 1),
(110, '2026-01-15', 3, 18.7404, 18.7404, 18.7404, 1),
(111, '2026-01-16', 1, 628.525, 628.525, 628.525, 1),
(112, '2026-01-17', 1, 826.04, 993.42, 707.575, 3),
(113, '2026-01-19', 2, 31.0101, 34.0517, 27.9684, 2),
(114, '2026-01-21', 1, 787.62, 787.62, 787.62, 1),
(115, '2026-01-22', 1, 369.752, 369.752, 369.752, 1),
(116, '2026-01-24', 1, 792.802, 792.802, 792.802, 1),
(117, '2026-01-24', 2, 18.2009, 26.9178, 9.48395, 2),
(118, '2026-01-24', 3, 58.7147, 58.7147, 58.7147, 1),
(119, '2026-01-25', 1, 883.639, 883.639, 883.639, 1),
(120, '2026-01-26', 2, 30.1941, 30.2813, 30.1069, 2),
(121, '2026-01-27', 2, 23.9102, 24.0482, 23.7722, 2),
(122, '2026-01-27', 3, 51.1676, 51.1676, 51.1676, 1),
(123, '2026-01-28', 1, 395.499, 395.499, 395.499, 1),
(124, '2026-01-30', 1, 478.37, 478.37, 478.37, 1),
(125, '2026-01-31', 1, 683.127, 683.127, 683.127, 1),
(126, '2026-01-31', 3, 15.8375, 15.8375, 15.8375, 1),
(127, '2026-02-02', 1, 623.186, 623.186, 623.186, 1),
(128, '2026-02-03', 3, 28.8188, 46.2292, 11.4084, 2),
(129, '2026-02-04', 2, 17.8219, 17.8219, 17.8219, 1),
(130, '2026-02-06', 2, 31.778, 31.778, 31.778, 1),
(131, '2026-02-06', 3, 55.1723, 59.9695, 50.3751, 2),
(132, '2026-02-10', 1, 450.33, 450.33, 450.33, 1),
(133, '2026-02-10', 2, 23.4935, 23.4935, 23.4935, 1),
(134, '2026-02-10', 3, 19.0192, 19.0192, 19.0192, 1),
(135, '2026-02-11', 3, 39.9643, 39.9643, 39.9643, 1),
(136, '2026-02-12', 1, 995.862, 995.862, 995.862, 1),
(137, '2026-02-12', 3, 55.5903, 55.5903, 55.5903, 1),
(138, '2026-02-13', 3, 51.2742, 51.2742, 51.2742, 1),
(139, '2026-02-14', 2, 7.00955, 7.00955, 7.00955, 1),
(140, '2026-02-15', 3, 31.463, 31.463, 31.463, 1),
(141, '2026-02-16', 1, 867.2, 867.2, 867.2, 1),
(142, '2026-02-20', 2, 31.4031, 31.4031, 31.4031, 1),
(143, '2026-02-21', 1, 428.493, 428.493, 428.493, 1),
(144, '2026-02-21', 3, 56.6726, 56.6726, 56.6726, 1),
(145, '2026-02-22', 1, 331.503, 331.503, 331.503, 1),
(146, '2026-02-23', 2, 13.3849, 13.3849, 13.3849, 1),
(147, '2026-02-24', 3, 20.2535, 20.2535, 20.2535, 1),
(148, '2026-02-26', 2, 24.7485, 32.7969, 16.7002, 2),
(149, '2026-02-27', 1, 465.284, 465.284, 465.284, 1),
(150, '2026-02-27', 3, 29.0728, 29.0728, 29.0728, 1);

-- --------------------------------------------------------

--
-- Structure de la table `emplacement`
--

CREATE TABLE `emplacement` (
  `id_emplacement` int(11) NOT NULL,
  `nom_emplacement` varchar(50) NOT NULL,
  `id_type_emplacement` int(11) NOT NULL,
  `id_sonde` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `emplacement`
--

INSERT INTO `emplacement` (`id_emplacement`, `nom_emplacement`, `id_type_emplacement`, `id_sonde`) VALUES
(1, 'Zone machine', 1, 1),
(2, 'Zone Peinture', 2, 2),
(3, 'Zone solvant', 1, 3);

-- --------------------------------------------------------

--
-- Structure de la table `installe`
--

CREATE TABLE `installe` (
  `id_alarme` int(11) NOT NULL,
  `id_emplacement` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `installe`
--

INSERT INTO `installe` (`id_alarme`, `id_emplacement`) VALUES
(1, 1),
(1, 3),
(2, 1),
(2, 2);

-- --------------------------------------------------------

--
-- Structure de la table `mesure`
--

CREATE TABLE `mesure` (
  `id_mesure` int(11) NOT NULL,
  `valeur_mesure` float DEFAULT NULL,
  `date_heure_mesure` datetime DEFAULT NULL,
  `id_emplacement` int(11) NOT NULL,
  `id_alerte` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `mesure`
--

INSERT INTO `mesure` (`id_mesure`, `valeur_mesure`, `date_heure_mesure`, `id_emplacement`, `id_alerte`) VALUES
(8, 4400, '2026-03-09 10:30:00', 2, 3),
(9, 386.24, '2026-03-07 07:18:17', 2, 3),
(10, 96.23, '2026-03-09 09:20:17', 3, 3),
(11, 720.4, '2026-03-03 06:21:17', 1, 3),
(12, 302.29, '2026-03-04 16:41:17', 2, 2),
(13, 333.99, '2026-03-05 03:30:17', 1, 2),
(14, 74.02, '2026-03-09 05:34:17', 3, 2),
(15, 333.95, '2026-03-06 04:59:17', 1, 2),
(16, 550.59, '2026-03-05 22:45:17', 3, 3),
(17, 803.33, '2026-03-09 02:30:17', 3, 3),
(18, 944.97, '2026-03-08 13:25:17', 3, 2),
(19, 53.5, '2026-03-03 10:45:17', 1, 2),
(20, 808.63, '2026-03-02 20:38:17', 1, 3),
(21, 25.4, '2026-03-06 13:14:17', 3, 3),
(22, 214.02, '2026-03-08 01:03:17', 1, 2),
(23, 350.38, '2026-03-05 14:17:17', 3, 3),
(24, 845.46, '2026-03-03 05:22:17', 3, 3),
(25, 613.2, '2026-03-06 03:43:17', 2, 2),
(26, 843.7, '2026-03-09 05:14:17', 2, 3),
(27, 721.49, '2026-03-03 03:01:17', 2, 2),
(28, 131.92, '2026-03-05 13:19:17', 2, 2),
(29, 809.24, '2026-03-05 22:29:17', 1, 3),
(30, 884.26, '2026-03-02 14:06:17', 1, 2),
(31, 753.42, '2026-03-03 08:41:17', 1, 3),
(32, 797.36, '2026-03-05 12:19:17', 2, 2),
(33, 466.88, '2026-03-07 02:26:17', 1, 2),
(34, 553.77, '2026-03-02 13:07:17', 1, 2),
(35, 126.81, '2026-03-06 02:29:17', 3, 3),
(36, 641.38, '2026-03-04 22:21:17', 1, 3),
(37, 720.52, '2026-03-09 01:08:17', 1, 2),
(38, 186.85, '2026-03-08 22:50:17', 3, 3),
(39, 728.17, '2026-03-03 13:39:17', 1, 3);

-- --------------------------------------------------------

--
-- Structure de la table `sonde`
--

CREATE TABLE `sonde` (
  `id_sonde` int(11) NOT NULL,
  `nom_sonde` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `sonde`
--

INSERT INTO `sonde` (`id_sonde`, `nom_sonde`) VALUES
(1, '62:03:57:41:38:23'),
(2, 'a2:c4:cb:3d:e9:1a'),
(3, 'Numéro 3'),
(4, 'Numéro 4');

-- --------------------------------------------------------

--
-- Structure de la table `type_emplacement`
--

CREATE TABLE `type_emplacement` (
  `id_type_emplacement` int(11) NOT NULL,
  `nom_type_emplacement` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `type_emplacement`
--

INSERT INTO `type_emplacement` (`id_type_emplacement`, `nom_type_emplacement`) VALUES
(1, 'machine'),
(2, 'salle');

-- --------------------------------------------------------

--
-- Structure de la table `type_info_mesure`
--

CREATE TABLE `type_info_mesure` (
  `id_type_mesure` int(11) NOT NULL,
  `nom_type_mesure` varchar(50) DEFAULT NULL,
  `valeur_danger_seuil` float DEFAULT NULL,
  `valeur_alerte_seuil` float DEFAULT NULL,
  `Unité` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `type_info_mesure`
--

INSERT INTO `type_info_mesure` (`id_type_mesure`, `nom_type_mesure`, `valeur_danger_seuil`, `valeur_alerte_seuil`, `Unité`) VALUES
(1, 'CO2', 1000, 2000, 'ppm'),
(2, 'PM 2.5', 10, 25, 'µg/m³'),
(3, 'PM 10', 20, 50, 'µg/m³'),
(4, 'TVOC', 250, 1000, 'µg/m³');

-- --------------------------------------------------------

--
-- Structure de la table `type_info_mesure_as_mesure`
--

CREATE TABLE `type_info_mesure_as_mesure` (
  `id_type_mesure` int(11) NOT NULL,
  `id_mesure` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Structure de la table `utilisateur`
--

CREATE TABLE `utilisateur` (
  `id_utilisateur` int(11) NOT NULL,
  `nom_utilisateur` varchar(50) DEFAULT NULL,
  `mot_de_passe_utilisateur` varchar(255) DEFAULT NULL,
  `role_utilisateur` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Déchargement des données de la table `utilisateur`
--

INSERT INTO `utilisateur` (`id_utilisateur`, `nom_utilisateur`, `mot_de_passe_utilisateur`, `role_utilisateur`) VALUES
(1, 'USER_TEST', 'ADMIN', 'ADMIN');

--
-- Index pour les tables déchargées
--

--
-- Index pour la table `alarme`
--
ALTER TABLE `alarme`
  ADD PRIMARY KEY (`id_alarme`),
  ADD UNIQUE KEY `alarme_nom_alarme_IDX` (`nom_alarme`) USING BTREE;

--
-- Index pour la table `alerte`
--
ALTER TABLE `alerte`
  ADD PRIMARY KEY (`id_alerte`);

--
-- Index pour la table `archive_moyennes_mensuelles`
--
ALTER TABLE `archive_moyennes_mensuelles`
  ADD PRIMARY KEY (`id_archive`);

--
-- Index pour la table `emplacement`
--
ALTER TABLE `emplacement`
  ADD PRIMARY KEY (`id_emplacement`),
  ADD KEY `id_type_emplacement` (`id_type_emplacement`),
  ADD KEY `id_sonde` (`id_sonde`);

--
-- Index pour la table `installe`
--
ALTER TABLE `installe`
  ADD PRIMARY KEY (`id_alarme`,`id_emplacement`),
  ADD KEY `id_emplacement` (`id_emplacement`);

--
-- Index pour la table `mesure`
--
ALTER TABLE `mesure`
  ADD PRIMARY KEY (`id_mesure`),
  ADD KEY `id_emplacement` (`id_emplacement`),
  ADD KEY `id_alerte` (`id_alerte`);

--
-- Index pour la table `sonde`
--
ALTER TABLE `sonde`
  ADD PRIMARY KEY (`id_sonde`);

--
-- Index pour la table `type_emplacement`
--
ALTER TABLE `type_emplacement`
  ADD PRIMARY KEY (`id_type_emplacement`);

--
-- Index pour la table `type_info_mesure`
--
ALTER TABLE `type_info_mesure`
  ADD PRIMARY KEY (`id_type_mesure`);

--
-- Index pour la table `type_info_mesure_as_mesure`
--
ALTER TABLE `type_info_mesure_as_mesure`
  ADD PRIMARY KEY (`id_type_mesure`,`id_mesure`),
  ADD KEY `id_mesure` (`id_mesure`);

--
-- Index pour la table `utilisateur`
--
ALTER TABLE `utilisateur`
  ADD PRIMARY KEY (`id_utilisateur`);

--
-- AUTO_INCREMENT pour les tables déchargées
--

--
-- AUTO_INCREMENT pour la table `alarme`
--
ALTER TABLE `alarme`
  MODIFY `id_alarme` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `alerte`
--
ALTER TABLE `alerte`
  MODIFY `id_alerte` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT pour la table `archive_moyennes_mensuelles`
--
ALTER TABLE `archive_moyennes_mensuelles`
  MODIFY `id_archive` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=196;

--
-- AUTO_INCREMENT pour la table `emplacement`
--
ALTER TABLE `emplacement`
  MODIFY `id_emplacement` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `mesure`
--
ALTER TABLE `mesure`
  MODIFY `id_mesure` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=336;

--
-- AUTO_INCREMENT pour la table `sonde`
--
ALTER TABLE `sonde`
  MODIFY `id_sonde` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `type_emplacement`
--
ALTER TABLE `type_emplacement`
  MODIFY `id_type_emplacement` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `type_info_mesure`
--
ALTER TABLE `type_info_mesure`
  MODIFY `id_type_mesure` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT pour la table `utilisateur`
--
ALTER TABLE `utilisateur`
  MODIFY `id_utilisateur` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- Contraintes pour les tables déchargées
--

--
-- Contraintes pour la table `emplacement`
--
ALTER TABLE `emplacement`
  ADD CONSTRAINT `emplacement_ibfk_1` FOREIGN KEY (`id_type_emplacement`) REFERENCES `type_emplacement` (`id_type_emplacement`),
  ADD CONSTRAINT `emplacement_ibfk_2` FOREIGN KEY (`id_sonde`) REFERENCES `sonde` (`id_sonde`);

--
-- Contraintes pour la table `installe`
--
ALTER TABLE `installe`
  ADD CONSTRAINT `installe_ibfk_1` FOREIGN KEY (`id_alarme`) REFERENCES `alarme` (`id_alarme`),
  ADD CONSTRAINT `installe_ibfk_2` FOREIGN KEY (`id_emplacement`) REFERENCES `emplacement` (`id_emplacement`);

--
-- Contraintes pour la table `mesure`
--
ALTER TABLE `mesure`
  ADD CONSTRAINT `mesure_ibfk_1` FOREIGN KEY (`id_emplacement`) REFERENCES `emplacement` (`id_emplacement`),
  ADD CONSTRAINT `mesure_ibfk_2` FOREIGN KEY (`id_alerte`) REFERENCES `alerte` (`id_alerte`);

--
-- Contraintes pour la table `type_info_mesure_as_mesure`
--
ALTER TABLE `type_info_mesure_as_mesure`
  ADD CONSTRAINT `type_info_mesure_as_mesure_ibfk_1` FOREIGN KEY (`id_type_mesure`) REFERENCES `type_info_mesure` (`id_type_mesure`),
  ADD CONSTRAINT `type_info_mesure_as_mesure_ibfk_2` FOREIGN KEY (`id_mesure`) REFERENCES `mesure` (`id_mesure`);

DELIMITER $$
--
-- Évènements
--
CREATE DEFINER=`Marais_R_Site_User`@`%` EVENT `archiver_mesures_mensuelles` ON SCHEDULE EVERY 1 MONTH STARTS '2026-03-17 11:13:05' ON COMPLETION NOT PRESERVE ENABLE DO BEGIN
    -- Étape 1: Insérer les données archivées avec moyenne, max et min
    INSERT INTO `archive_moyennes_mensuelles` (`date_jour`, `id_emplacement`, `moyenne_valeur`, `max_valeur`, `min_valeur`, `nb_mesures_compactees`)
    SELECT 
        DATE(`date_heure_mesure`) as jour, 
        `id_emplacement`, 
        AVG(`valeur_mesure`),
        MAX(`valeur_mesure`),
        MIN(`valeur_mesure`),
        COUNT(*)
    FROM `mesure`
    WHERE `date_heure_mesure` < DATE_FORMAT(NOW() ,'%Y-%m-01')
    GROUP BY jour, `id_emplacement`;

    -- Étape 2: Supprimer les associations de type_info_mesure
    DELETE FROM `type_info_mesure_as_mesure` 
    WHERE `id_mesure` IN (
        SELECT `id_mesure` FROM `mesure` 
        WHERE `date_heure_mesure` < DATE_FORMAT(NOW() ,'%Y-%m-01')
    );

    -- Étape 3: Supprimer les anciennes mesures
    DELETE FROM `mesure` 
    WHERE `date_heure_mesure` < DATE_FORMAT(NOW() ,'%Y-%m-01');
END$$

DELIMITER ;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
