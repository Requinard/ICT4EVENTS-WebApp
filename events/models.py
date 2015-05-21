# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Account(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    gebruikersnaam = models.CharField(unique=True, max_length=510, blank=True, null=True)
    email = models.CharField(unique=True, max_length=510)
    activatiehash = models.CharField(max_length=510)
    geactiveerd = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'account'


class AccountBijdrage(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    account = models.ForeignKey(Account)
    bijdrage = models.ForeignKey('Bijdrage')
    like = models.BooleanField()
    ongewenst = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'account_bijdrage'


class Bericht(models.Model):
    bijdrage = models.ForeignKey('Bijdrage', primary_key=True)
    titel = models.CharField(max_length=510, blank=True, null=True)
    inhoud = models.CharField(max_length=255)

    class Meta:
        managed = True
        db_table = 'bericht'


class Bestand(models.Model):
    bijdrage = models.ForeignKey('Bijdrage', primary_key=True)
    categorie = models.ForeignKey('Categorie')
    bestandslocatie = models.CharField(max_length=510)
    grootte = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'bestand'


class Bijdrage(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    account = models.ForeignKey(Account)
    datum = models.DateField(blank=True, null=True)
    soort = models.CharField(max_length=510)

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
    bijdrage = models.ForeignKey(Bijdrage, primary_key=True)
    categorie_gerelateerd = models.ForeignKey('Categorie', blank=True, null=True, related_name="+")
    naam = models.CharField(max_length=510)

    class Meta:
        managed = True
        db_table = 'categorie'


class Event(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    locatie = models.ForeignKey('Locatie', blank=True, null=True)
    naam = models.CharField(max_length=510)
    datumstart = models.DateField(blank=True, null=True)
    datumeinde = models.DateField(blank=True, null=True)
    maxbezoekers = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'event'

    def __str__(self):
        return self.naam


class Locatie(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    naam = models.CharField(unique=True, max_length=510)
    straat = models.CharField(max_length=510, blank=True, null=True)
    nr = models.CharField(max_length=510, blank=True, null=True)
    postcode = models.CharField(max_length=510, blank=True, null=True)
    plaats = models.CharField(max_length=510, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'locatie'


class Persoon(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    voornaam = models.CharField(max_length=510)
    tussenvoegsel = models.CharField(max_length=510, blank=True, null=True)
    achternaam = models.CharField(max_length=510)
    straat = models.CharField(max_length=510, blank=True, null=True)
    huisnr = models.CharField(max_length=510, blank=True, null=True)
    woonplaats = models.CharField(max_length=510, blank=True, null=True)
    banknr = models.CharField(max_length=510, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'persoon'


class Plek(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    locatie = models.ForeignKey(Locatie)
    nummer = models.CharField(max_length=510, blank=True, null=True)
    capaciteit = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'plek'


class PlekReservering(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    plek = models.ForeignKey(Plek)
    reservering = models.ForeignKey('Reservering')

    class Meta:
        managed = True
        db_table = 'plek_reservering'


class PlekSpecificatie(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    specificatie = models.ForeignKey('Specificatie')
    plek = models.ForeignKey(Plek)
    waarde = models.CharField(max_length=510)

    class Meta:
        managed = True
        db_table = 'plek_specificatie'


class Polsbandje(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    barcode = models.CharField(unique=True, max_length=510)
    actief = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'polsbandje'


class Product(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    productcategorie = models.ForeignKey('Productcat', related_name="+")
    merk = models.CharField(max_length=510, blank=True, null=True)
    serie = models.CharField(max_length=510, blank=True, null=True)
    typenummer = models.CharField(max_length=510, blank=True, null=True)
    prijs = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'product'


class Productcat(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    productcategorie = models.ForeignKey('self', blank=True, null=True, related_name="+")
    naam = models.CharField(unique=True, max_length=510)

    class Meta:
        managed = True
        db_table = 'productcat'


class Productexemplaar(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    product = models.ForeignKey(Product)
    volgnummer = models.IntegerField()
    barcode = models.CharField(unique=True, max_length=510, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'productexemplaar'


class Reservering(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    persoon = models.ForeignKey(Persoon)
    datumstart = models.DateField(blank=True, null=True)
    datumeinde = models.DateField(blank=True, null=True)
    betaald = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'reservering'


class ReserveringPolsbandje(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    reservering = models.ForeignKey(Reservering)
    polsbandje = models.ForeignKey(Polsbandje)
    account = models.ForeignKey(Account)
    aanwezig = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'reservering_polsbandje'


class Specificatie(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    naam = models.CharField(unique=True, max_length=510)

    class Meta:
        managed = True
        db_table = 'specificatie'


class Verhuur(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    productexemplaar = models.ForeignKey(Productexemplaar, blank=True, null=True)
    res_pb = models.ForeignKey(ReserveringPolsbandje, blank=True, null=True)
    datumin = models.DateField(blank=True, null=True)
    datumuit = models.DateField(blank=True, null=True)
    prijs = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    betaald = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'verhuur'
