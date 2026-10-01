from django.db import models

class Client(models.Model):
    idclient = models.AutoField(primary_key=True)  # Pour correspondre à votre colonne PostgreSQL
    nom = models.CharField(max_length=25)
    mdp = models.CharField(max_length=25)

    class Meta:
        db_table = 'client'
        managed = False  # Changez à False pour que Django ne gère pas la table

    def __str__(self):
        return self.nom
    
class Produit(models.Model):
    idproduit = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=25)
    prix = models.FloatField()

    class Meta:
        db_table = 'produit'
        managed = False

    def __str__(self):
        return self.nom

class Commentaire(models.Model):
    idcommentaire = models.AutoField(primary_key=True)
    idclient = models.ForeignKey(Client, models.CASCADE, db_column='idclient')
    idproduit = models.ForeignKey(Produit, models.CASCADE, db_column='idproduit')
    texte = models.CharField(max_length=255)

    class Meta:
        db_table = 'commentaire'
        managed = False

    def __str__(self):
        return f"Commentaire de {self.idclient.nom} sur {self.idproduit.nom}"

# Ajouter le modèle Achat
class Achat(models.Model):
    idachat = models.AutoField(primary_key=True)
    idclient = models.ForeignKey(Client, models.CASCADE, db_column='idclient')
    idproduit = models.ForeignKey(Produit, models.CASCADE, db_column='idproduit')

    class Meta:
        db_table = 'achat'
        managed = False

    def __str__(self):
        return f"Achat de {self.idproduit.nom} par {self.idclient.nom}"