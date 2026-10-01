import csv
from django.shortcuts import render, redirect
from .forms import TextSentimentForm
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Client, Produit, Commentaire, Achat
from .forms import LoginForm
from django.http import HttpResponse
from .sentiment_analyzer import analyze_sentiment
from .sentiment_analyzer import model, w2v_model, scaler, preprocess_and_train

def home(request):
    if not request.session.get('client_id'):
        return redirect('login')
    produits = Produit.objects.all()
    return render(request, 'clients/products.html', {'produits': produits})

def login(request):
    try:
        # Test la connexion et affiche plus de détails
        test_connection = Client.objects.all()
        clients_count = test_connection.count()
        messages.info(request, f'Connexion DB OK - {clients_count} clients trouvés')
        # Ajoutez ces lignes pour le débogage
        for client in test_connection:
            messages.info(request, f'Client trouvé: {client.nom}')
    except Exception as e:
        messages.error(request, f'Erreur de connexion détaillée: {str(e)}')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            nom = form.cleaned_data['nom']
            mdp = form.cleaned_data['mdp']
            try:
                client = Client.objects.get(nom=nom, mdp=mdp)
                request.session['client_id'] = client.idclient
                return redirect('home')
            except Client.DoesNotExist:
                messages.error(request, 'Nom ou mot de passe incorrect')
    else:
        form = LoginForm()
    return render(request, 'clients/login.html', {'form': form})

def acheter(request, produit_id):
    if not request.session.get('client_id'):
        return redirect('login')
    
    try:
        client = Client.objects.get(idclient=request.session['client_id'])
        produit = Produit.objects.get(idproduit=produit_id)
        
        # Créer l'achat
        achat = Achat.objects.create(
            idclient=client,
            idproduit=produit
        )
        
        # Ajouter un message de succès
        messages.success(request, f'Voavidy soa aman-tsara ny {produit.nom} amnin ny  {produit.prix} Ar!')
        return redirect('home')
        
    except Exception as e:
        messages.error(request, f'Erreur lors de l\'achat: {str(e)}')
        return redirect('home')


def inserer_texte(request):
    if request.method == 'POST':
        form = SentimentForm(request.POST)
        if form.is_valid():
            texte = form.cleaned_data['texte']
            sentiment = form.cleaned_data['sentiment']
            
            # Écrire dans le fichier CSV
            with open('data.csv', 'a', newline='', encoding='utf-8') as fichier_csv:
                writer = csv.writer(fichier_csv)
                writer.writerow([texte, sentiment])
            
            return redirect('inserer_texte')  # Recharge la page
    else:
        form = SentimentForm()
    
    return render(request, 'inserer.html', {'form': form})

def commentaires(request, produit_id):
    if not request.session.get('client_id'):
        return redirect('login')
    
    client_id = request.session['client_id']
    produit = Produit.objects.get(idproduit=produit_id)
    commentaires = Commentaire.objects.filter(idproduit=produit_id)
    
    # Analyser le sentiment de tous les commentaires existants
    commentaires_with_sentiment = []
    for commentaire in commentaires:
        sentiment_result = analyze_sentiment(commentaire.texte)
        commentaires_with_sentiment.append({
            'commentaire': commentaire,
            'sentiment': sentiment_result
        })
    
    # Vérifier si le client a acheté le produit
    a_achete = Achat.objects.filter(idclient=client_id, idproduit=produit_id).exists()
    
    if request.method == 'POST' and a_achete:
        texte = request.POST.get('commentaire')
        if texte:
            # Analyser le sentiment du commentaire
            sentiment_result = analyze_sentiment(texte)
            
            Commentaire.objects.create(
                idclient_id=client_id,
                idproduit_id=produit_id,
                texte=texte
            )
            
            messages.success(
                request, 
                f'Tafiditra ny fanehoan-kevitrao {sentiment_result["emoji"]} '
                f'(Sentiment: {sentiment_result["sentiment"]}, '
                f'Confiance: {sentiment_result["confidence"]:.2f})'
            )
            return redirect('commentaires', produit_id=produit_id)
    
    return render(request, 'clients/commentaires.html', {
        'produit': produit,
        'commentaires': commentaires_with_sentiment,
        'a_achete': a_achete
    })

def add_text_sentiment(request):
    if request.method == 'POST':
        form = TextSentimentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            sentiment = form.cleaned_data['sentiment']
            
            # Ajouter dans donne.csv
            with open('donne.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([text, sentiment])
            
            return redirect('add_text_sentiment')
    else:
        form = TextSentimentForm()
    
    return render(request, 'clients/add_text_sentiment.html', {'form': form})

def retrain_model(request):
    if request.method == 'POST':
        # Réentrainer le modèle
        global model, w2v_model, scaler
        model, w2v_model, scaler = preprocess_and_train()
        messages.success(request, 'Le modèle a été réentrainé avec succès!')
    return redirect('add_text_sentiment')
