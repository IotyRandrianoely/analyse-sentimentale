import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler
from gensim.models import Word2Vec
import nltk
from nltk.tokenize import word_tokenize
import re
from .commentaires import commentaires_positifs, commentaires_negatifs

nltk.download('punkt')
nltk.download('punkt_tab')

# Utiliser les commentaires importés
def load_data():
    # Charger les données prédéfinies
    data = {
        'comment': commentaires_positifs + commentaires_negatifs,
        'sentiment': [1] * len(commentaires_positifs) + [0] * len(commentaires_negatifs)
    }
    df_predefined = pd.DataFrame(data)
    
    # Charger les données du CSV
    try:
        df_csv = pd.read_csv('donne.csv', names=['comment', 'sentiment'])
        # Convertir les sentiments textuels en numérique
        df_csv['sentiment'] = df_csv['sentiment'].map({'positif': 1, 'négatif': 0})
        
        # Combiner les deux DataFrames
        df_combined = pd.concat([df_predefined, df_csv], ignore_index=True)
        return df_combined
    except FileNotFoundError:
        # Si le fichier CSV n'existe pas, retourner seulement les données prédéfinies
        return df_predefined

def clean_text(text):
    # Enlever les caractères spéciaux et normaliser le texte
    text = re.sub(r'[^\w\s]', ' ', text)
    text = ' '.join(text.split())  # Normaliser les espaces
    return text.lower().strip()

def preprocess_and_train():
    # Charger les données
    df = load_data()
    
    # Nettoyer les textes
    df['clean_comment'] = df['comment'].apply(clean_text)
    df['tokens'] = df['clean_comment'].apply(word_tokenize)
    
    # Supprimer les lignes avec des valeurs NaN
    df = df.dropna(subset=['comment', 'sentiment'])
    
    # Paramètres optimisés pour Word2Vec
    w2v_model = Word2Vec(
        sentences=df['tokens'],
        vector_size=30,
        window=2,
        min_count=1,
        workers=4,
        sg=1,
        epochs=100
    )
    
    def get_mean_vector(tokens):
        vectors = [w2v_model.wv[word] for word in tokens if word in w2v_model.wv]
        if len(vectors) == 0:
            return np.zeros(30)
        return np.mean(vectors, axis=0)
    
    # Vectorisation et normalisation
    X = np.array([get_mean_vector(tokens) for tokens in df['tokens']])
    y = df['sentiment'].values  # Ensure y is a numpy array
    
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    
    # Create and train the model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model, w2v_model, scaler

def predict_sentiment(model, w2v_model, scaler, new_comment):
    # Nettoyer et tokenizer
    clean_comment = clean_text(new_comment)
    tokens = word_tokenize(clean_comment)
    
    # Obtenir le vecteur
    vectors = [w2v_model.wv[word] for word in tokens if word in w2v_model.wv]
    if len(vectors) == 0:
        comment_vector = np.zeros(50)  # Changed from 100 to 50 to match vector_size
    else:
        weights = np.array([1.0 / len(vectors)] * len(vectors))
        weighted_vectors = np.multiply(vectors, weights[:, np.newaxis])
        comment_vector = np.sum(weighted_vectors, axis=0)
    
    # Normaliser le vecteur
    comment_vector = scaler.transform(comment_vector.reshape(1, -1))
    
    # Prédire avec seuil de confiance ajusté
    proba = model.predict_proba(comment_vector)[0]
    prediction = 1 if proba[1] >= 0.60 else 0  # Seuil augmenté pour plus de précision
    confidence = proba[1] if prediction == 1 else proba[0]
    
    sentiment = "positif" if prediction == 1 else "négatif"
    return sentiment, confidence
