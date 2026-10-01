from django import forms
from django.shortcuts import render

class LoginForm(forms.Form):
    nom = forms.CharField(max_length=25)
    mdp = forms.CharField(widget=forms.PasswordInput)

class TextSentimentForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
    sentiment = forms.ChoiceField(
        choices=[('positif', 'Positif'), ('négatif', 'Négatif')],
        widget=forms.RadioSelect
    )

def add_text_sentiment(request):
    if request.method == 'POST':
        form = TextSentimentForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['text']
            sentiment = analyze_sentiment(text)  # Votre fonction d'analyse
            # Sauvegarde dans le CSV...
            return render(request, 'clients/add_text_sentiment.html', {
                'form': form,
                'sentiment': sentiment
            })
    else:
        form = TextSentimentForm()
    return render(request, 'clients/add_text_sentiment.html', {'form': form})