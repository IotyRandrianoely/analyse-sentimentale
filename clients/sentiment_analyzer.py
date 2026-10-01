from .mode import preprocess_and_train, predict_sentiment

# Initialiser le modèle une seule fois
model, w2v_model, scaler = preprocess_and_train()

def analyze_sentiment(text):
    sentiment, confidence = predict_sentiment(model, w2v_model, scaler, text)
    
    # Ajouter l'emoji en fonction du sentiment
    emoji = "😊" if sentiment == "positif" else "😞"
    
    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "emoji": emoji
    }