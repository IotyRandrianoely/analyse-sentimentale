# Commerce - Analyse de sentiment des commentaires

## Description

Ce projet est une application web de commerce développée avec Django. Elle permet aux clients de consulter des produits, d'effectuer des achats et de publier des commentaires. Un modèle de machine learning analyse automatiquement chaque commentaire et prédit s'il est positif ou négatif, avec un score de confiance.

## Fonctionnalités

- Connexion des clients ;
- Affichage du catalogue des produits et de leurs prix ;
- Enregistrement des achats ;
- Ajout de commentaires uniquement après l'achat d'un produit ;
- Analyse automatique du sentiment des commentaires ;
- Ajout de nouvelles données d'entraînement dans `donne.csv` ;
- Réentraînement du modèle depuis l'application ;
- Gestion des données avec Django ORM et PostgreSQL.

## Approche data et machine learning

Les données sont des commentaires textuels associés à une étiquette (`positif` ou `négatif`). Le texte est nettoyé puis tokenisé avec NLTK. Les mots sont transformés en vecteurs grâce à Word2Vec, normalisés avec `StandardScaler`, puis classés avec un `RandomForestClassifier` de Scikit-Learn. La prédiction retourne le sentiment et une confiance associée.

Une seconde implémentation expérimentale, dans `clients/mode_tfidf.py`, utilise TF-IDF et Random Forest avec une recherche d'hyperparamètres par `GridSearchCV`.

## Technologies utilisées

- Python 3 ;
- Django 5.1 ;
- PostgreSQL ;
- Pandas et NumPy ;
- Scikit-Learn ;
- Gensim (Word2Vec) ;
- NLTK ;
- HTML/CSS et templates Django.

## Installation et lancement

1. Installer les dépendances Python :

   ```bash
   pip install django pandas numpy scikit-learn gensim nltk psycopg2-binary
   ```

2. Créer la base PostgreSQL `ad_ecommerce` et vérifier les identifiants dans `commerce/settings.py`.

3. Appliquer les migrations :

   ```bash
   python manage.py migrate
   ```

4. Lancer le serveur :

   ```bash
   python manage.py runserver
   ```

5. Ouvrir `http://127.0.0.1:8000/` dans un navigateur.

## Structure principale

- `commerce/` : configuration du projet Django ;
- `clients/` : modèles, vues, formulaires et logique de machine learning ;
- `clients/templates/clients/` : interfaces HTML ;
- `donne.csv` : données textuelles utilisées pour l'entraînement ;
- `db.sqlite3` : fichier SQLite présent dans le projet, tandis que la configuration actuelle utilise PostgreSQL.
