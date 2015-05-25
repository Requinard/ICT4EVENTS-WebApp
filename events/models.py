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


class Event(models.Model):
    locatie = models.ForeignKey('Locatie', blank=True, null=True)
    naam = models.CharField(max_length=510)
    datumstart = models.DateField(blank=True, null=True)
    datumeinde = models.DateField(blank=True, null=True)
    maxbezoekers = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'event'
        ordering = ('datumstart', 'datumeinde')

    def __str__(self):
        return self.naam

    def GetAllRegistrations(self, paid=True):
        location = self.locatie

        spots = Plek.objects.filter(locatie=location)

        reservations = Reservering.objects.filter(plekken__contains=spots.all(), betaald=paid,
                                                  datumstart__gte=self.datumstart, datumeinde__lte=self.datumeinde)

        return reservations

    def GetAllUnpaidRegistrations(self):
        return self.GetAllRegistrations(False)


class Locatie(models.Model):
    naam = models.CharField(unique=True, max_length=510)
    straat = models.CharField(max_length=510, blank=True, null=True)
    nr = models.CharField(max_length=510, blank=True, null=True)
    postcode = models.CharField(max_length=510, blank=True, null=True)
    plaats = models.CharField(max_length=510, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'locatie'

    def __str__(self):
        return "%s\n%s %s\n%s %s" % (self.naam, self.straat, self.nr, self.postcode, self.plaats)

    def GetSlugifiedName(self):
        s = "%s+%s,%s,%s" % (self.straat, self.nr, self.postcode, self.plaats)
        return s.replace(' ', '+')


class Plek(models.Model):
    nummer = models.CharField(max_length=510, blank=True, null=True)
    capaciteit = models.IntegerField(blank=True, null=True)
    locatie = models.ForeignKey(Locatie)

    class Meta:
        managed = True
        db_table = 'plek'


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


class Reservering(models.Model):
    datumstart = models.DateField(blank=True, null=True)
    datumeinde = models.DateField(blank=True, null=True)
    betaald = models.BooleanField()

    plekken = models.ManyToManyField(Plek)
    persoon = models.ForeignKey('Persoon')

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
