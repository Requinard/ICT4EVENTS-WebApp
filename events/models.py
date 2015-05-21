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
from django.contrib.auth.models import User

from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver


class Account(models.Model):
    gebruiker = models.OneToOneField(User)
    activatiehash = models.CharField(max_length=510)
    geactiveerd = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'account'

    @receiver(post_save, sender=User)
    def create_new(sender, instance=None, created=False, **kwargs):
        if created:
            Account.objects.get_or_create(gebruiker=instance, activatiehash=hash(sender.pk), geactiveerd=False)

    @receiver(pre_delete, sender=User)
    def delete_on_parent(sender, instance=None, **kwargs):
        if instance:
            acc = Account.objects.get(gebruiker=instance)

            acc.delete()

    def __str__(self):
        return self.gebruiker.username

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
        ('categorie', 'categorie'),
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


class Event(models.Model):
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
    naam = models.CharField(unique=True, max_length=510)
    straat = models.CharField(max_length=510, blank=True, null=True)
    nr = models.CharField(max_length=510, blank=True, null=True)
    postcode = models.CharField(max_length=510, blank=True, null=True)
    plaats = models.CharField(max_length=510, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'locatie'


class Persoon(models.Model):
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
    nummer = models.CharField(max_length=510, blank=True, null=True)
    capaciteit = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'plek'


class PlekReservering(models.Model):
    reservering = models.ForeignKey('Reservering')

    class Meta:
        managed = True
        db_table = 'plek_reservering'


class PlekSpecificatie(models.Model):
    specificatie = models.ForeignKey('Specificatie')
    plek = models.ForeignKey(Plek)
    waarde = models.CharField(max_length=510)

    class Meta:
        managed = True
        db_table = 'plek_specificatie'


class Polsbandje(models.Model):
    barcode = models.CharField(unique=True, max_length=510)
    actief = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'polsbandje'


class Product(models.Model):
    productcategorie = models.ForeignKey('Productcat', related_name="+")
    merk = models.CharField(max_length=510, blank=True, null=True)
    serie = models.CharField(max_length=510, blank=True, null=True)
    typenummer = models.CharField(max_length=510, blank=True, null=True)
    prijs = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'product'


class Productcat(models.Model):
    productcategorie = models.ForeignKey('self', blank=True, null=True, related_name="+")
    naam = models.CharField(unique=True, max_length=510)

    class Meta:
        managed = True
        db_table = 'productcat'


class Productexemplaar(models.Model):
    barcode = models.CharField(unique=True, max_length=510, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'productexemplaar'


class Reservering(models.Model):
    datumstart = models.DateField(blank=True, null=True)
    datumeinde = models.DateField(blank=True, null=True)
    betaald = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'reservering'


class ReserveringPolsbandje(models.Model):
    class Meta:
        managed = True
        db_table = 'reservering_polsbandje'


class Specificatie(models.Model):
    naam = models.CharField(unique=True, max_length=510)

    class Meta:
        managed = True
        db_table = 'specificatie'


class Verhuur(models.Model):
    productexemplaar = models.ForeignKey(Productexemplaar, blank=True, null=True)
    res_pb = models.ForeignKey(ReserveringPolsbandje, blank=True, null=True)
    datumin = models.DateField(blank=True, null=True)
    datumuit = models.DateField(blank=True, null=True)
    prijs = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    betaald = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'verhuur'
