from clients.mode import preprocess_and_train, predict_sentiment

# Entraîner les modèles
print("Entraînement des modèles...")
model, w2v_model, scaler = preprocess_and_train()

# Tester une phrase
phrase = "aleoko maty toy izay mampiasa an'io"
sentiment, confidence = predict_sentiment(model, w2v_model, scaler, phrase)

print(f"\nPhrase testée: {phrase}")
print(f"Sentiment: {sentiment}")
print(f"Confiance: {confidence:.2f}")