-- Supprimer la base de données si elle existe
DROP DATABASE IF EXISTS ad_ecommerce;

-- Créer la base de données
CREATE DATABASE ad_ecommerce;

-- Se connecter à la base de données (à exécuter manuellement dans psql)
\c ad_ecommerce

-- Création des tables
CREATE TABLE produit (
    idProduit SERIAL PRIMARY KEY,
    nom VARCHAR(25),
    prix REAL
);

CREATE TABLE client (
    idClient SERIAL PRIMARY KEY,
    nom VARCHAR(25),
    mdp VARCHAR(25)
);

CREATE TABLE achat (
    idAchat SERIAL PRIMARY KEY,
    idClient INT REFERENCES client(idClient) ON DELETE CASCADE,
    idProduit INT REFERENCES produit(idProduit) ON DELETE CASCADE
);

CREATE TABLE commentaire (
    idCommentaire SERIAL PRIMARY KEY,
    idClient INT REFERENCES client(idClient) ON DELETE CASCADE,
    idProduit INT REFERENCES produit(idProduit) ON DELETE CASCADE,
    texte VARCHAR(255)
);

-- Insérer des produits
INSERT INTO produit (nom, prix) VALUES
('Ordinateur', 1200.50),
('Smartphone', 800.99),
('Casque Bluetooth', 150.75),
('Clavier mecanique', 99.90),
('Souris sans fil', 49.99);

-- Insérer des clients
INSERT INTO client (nom, mdp) VALUES
('Alice', 'mdp123'),
('Bob', 'securepass'),
('Charlie', 'azerty'),
('David', 'qwerty'),
('Emma', 'password');

-- Insérer des achats
INSERT INTO achat (idClient, idProduit) VALUES
(1, 2),
(1, 4),
(2, 1),
(3, 3),
(4, 5),
(5, 2),
(5, 3);

-- Insérer des commentaires
INSERT INTO commentaire (idClient, idProduit, texte) VALUES
(1, 2, 'Tres bon smartphone, performant et fluide !'),
(2, 1, 'Ordinateur puissant, parfait pour le travail.'),
(3, 3, 'Le son du casque est incroyable, je recommande.'),
(4, 5, 'Souris ergonomique et tres reactive.'),
(5, 4, 'Clavier agreable a utiliser, bon rapport qualite-prix.');
