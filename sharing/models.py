from django.db import models

# Create your models here.
class AccountBijdrage(models.Model):
    bijdrage = models.ForeignKey('Bijdrage')
    like = models.BooleanField()
    ongewenst = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'account_bijdrage'


class Bericht(models.Model):
    bijdrage = models.OneToOneField('Bijdrage')
    titel = models.CharField(max_length=510, blank=True, null=True)
    inhoud = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'bericht'


class Bestand(models.Model):
    bijdrage = models.OneToOneField('Bijdrage')
    categorie = models.ForeignKey('Categorie')
    bestandslocatie = models.CharField(max_length=510)
    grootte = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'bestand'


class Bijdrage(models.Model):
    datum = models.DateField(blank=True, null=True)
    soort = models.CharField(max_length=510, choices=(
        ('bericht', 'bericht'),
        ('bestand', 'bestand'),
        ('categorie', 'categorie'),
        ('account', 'account')
    ))

    class Meta:
        managed = True
        db_table = 'bijdrage'


class BijdrageBericht(models.Model):
    bijdrage = models.ForeignKey(Bijdrage, blank=True, null=True)
    bericht = models.ForeignKey(Bericht, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'bijdrage_bericht'


class Categorie(models.Model):
    bijdrage = models.OneToOneField(Bijdrage)
    categorie_gerelateerd = models.ForeignKey('Categorie', blank=True, null=True, related_name="+")
    naam = models.CharField(max_length=510)

    class Meta:
        managed = True
        db_table = 'categorie'