import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import re
from .commentaires import commentaires_positifs, commentaires_negatifs

def clean_text(text):
    """Nettoie et normalise le texte"""
    text = re.sub(r'[^\w\s]', ' ', text)
    text = ' '.join(text.split())
    return text.lower().strip()

def load_and_prepare_data():
    """Charge et prépare les données"""
    # Créer le DataFrame
    data = {
        'comment': commentaires_positifs + commentaires_negatifs,
        'sentiment': [1] * len(commentaires_positifs) + [0] * len(commentaires_negatifs)
    }
    df = pd.DataFrame(data)
    
    # Nettoyer les textes
    df['clean_comment'] = df['comment'].apply(clean_text)
    return df

def train_model():
    """Entraîne le modèle TF-IDF + Random Forest"""
    # Préparer les données
    df = load_and_prepare_data()
    
    # Créer et configurer le vectoriseur TF-IDF
    tfidf = TfidfVectorizer(
        max_features=1000,      # Limite le nombre de features
        min_df=2,              # Ignore les termes apparaissant dans moins de 2 documents
        max_df=0.95,           # Ignore les termes apparaissant dans plus de 95% des documents
        ngram_range=(1, 2)     # Utilise des unigrammes et bigrammes
    )
    
    # Vectoriser les textes
    X = tfidf.fit_transform(df['clean_comment'])
    y = df['sentiment']
    
    # Diviser les données
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    # Configurer la grille de paramètres pour RandomForest
    param_grid = {
        'n_estimators': [50, 100],
        'max_depth': [5, 10],
        'min_samples_split': [2, 3],
        'min_samples_leaf': [1, 2],
        'class_weight': ['balanced'],
        'max_features': ['sqrt', 'log2']
    }
    
    # Créer et entraîner le modèle avec GridSearch
    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(
        rf, param_grid, cv=5, scoring='f1', n_jobs=-1
    )
    grid_search.fit(X_train, y_train)
    
    # Évaluer le modèle
    y_pred = grid_search.predict(X_test)
    print("\nMeilleurs paramètres:", grid_search.best_params_)
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")
    print("\nRapport de classification:")
    print(classification_report(y_test, y_pred))
    
    return grid_search, tfidf

def predict_sentiment(model, vectorizer, text):
    """Prédit le sentiment d'un nouveau texte"""
    # Nettoyer le texte
    clean = clean_text(text)
    
    # Vectoriser
    X = vectorizer.transform([clean])
    
    # Prédire
    proba = model.predict_proba(X)[0]
    prediction = 1 if proba[1] >= 0.60 else 0
    confidence = proba[1] if prediction == 1 else proba[0]
    
    sentiment = "positif" if prediction == 1 else "négatif"
    return sentiment, confidence

# Pour tester directement ce fichier
if __name__ == "__main__":
    model, vectorizer = train_model()
    
    # Exemple de prédiction
    test_text = "Ce produit est vraiment excellent!"
    sentiment, confidence = predict_sentiment(model, vectorizer, test_text)
    print(f"\nTest avec: '{test_text}'")
    print(f"Sentiment: {sentiment}")
    print(f"Confiance: {confidence:.2f}")