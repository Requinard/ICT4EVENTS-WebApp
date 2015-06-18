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
from django.db import connection


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
        try:
            reservations = Reservering.objects.filter(plekken__contains=spots.all(), betaald=paid,
                                                      datumstart__gte=self.datumstart,
                                                      datumeinde__lte=self.datumeinde) or []
        except:
            reservations = []
        return reservations

    def GetAllUnpaidRegistrations(self):
        return self.GetAllRegistrations(False)

    def evaluate_user_registered(self, user):
        if self in user.settings.get_reservations():
            return True

        return False


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
        return self.naam

    def GetSlugifiedName(self):
        if self.straat is not None:
            s = "%s+%s,%s,%s" % (self.straat, self.nr, self.postcode, self.plaats)
        else:
            s = self.naam
        return s.replace(' ', '+')


class Plek(models.Model):
    nummer = models.CharField(max_length=510, blank=True, null=True)
    capaciteit = models.IntegerField(blank=True, null=True)
    locatie = models.ForeignKey(Locatie)

    class Meta:
        managed = True
        db_table = 'plek'

    def __str__(self):
        return self.nummer

    @staticmethod
    def reserve(plek, persoon, startdate, enddate):
        '''
        plek_id = Plek.objects.get(nummer=plek)
        pers_id = persoon

        cursor = connection.cursor()
        try:
            cursor.execute("BEGIN")
            cursor.callproc(' CreatePlaceReservation', [startdate, enddate, False, pers_id.id, plek_id.id])
            cursor.execute("COMMIT")
            cursor.close()
            return (True, None)
        except:
            cursor.rollback()
            cursor.close()
            return (False,None)
        '''
        return (False,None)

class PlekSpecificatie(models.Model):
    plek = models.ForeignKey(Plek)
    waarde = models.CharField(max_length=510)
    specificatie = models.ForeignKey('Specificatie')

    class Meta:
        managed = True
        db_table = 'plek_specificatie'

    def __str__(self):
        return self.waarde


class Reservering(models.Model):
    datumstart = models.DateField(blank=True, null=True)
    datumeinde = models.DateField(blank=True, null=True)
    betaald = models.BooleanField(default=False)

    plekken = models.ForeignKey(Plek)
    persoon = models.ForeignKey('Persoon')

    class Meta:
        managed = True
        db_table = 'reservering'

    def __str__(self):
        return "%s tot %s" % (self.datumstart, self.datumeinde)


class Polsbandje(models.Model):
    barcode = models.CharField(unique=True, max_length=510)
    actief = models.BooleanField()

    class Meta:
        managed = True
        db_table = 'polsbandje'

    def __str__(self):
        return self.barcode

    @receiver(post_save, sender=Reservering)
    def create_new(sender, instance=None, created=False, **kwargs):
        if created:
            pass
            # ReserveringPolsbandje.objects.get_or_create(polsband=Polsbandje.objects.filter(actief=False)[0],reservering=sender,account=sender.account)


class Specificatie(models.Model):
    naam = models.CharField(unique=True, max_length=510)

    class Meta:
        managed = True
        db_table = 'specificatie'

    def __str__(self):
        return self.naam


class Persoon(models.Model):
    straat = models.CharField(max_length=510, blank=True, null=True)
    huisnr = models.CharField(max_length=510, blank=True, null=True)
    woonplaats = models.CharField(max_length=510, blank=True, null=True)
    banknr = models.CharField(max_length=510, blank=True, null=True)

    user = models.OneToOneField(User, related_name="details", null=True, blank=True)

    @property
    def voornaam(self):
        return self.user.first_name

    @property
    def achternaam(self):
        return self.user.last_name

    class Meta:
        managed = True
        db_table = 'persoon'

    def get_full_name(self):
        return "%s %s" % (self.voornaam, self.achternaam)

    def __str__(self):
        return self.get_full_name()

    @receiver(post_save, sender=User)
    def create_new(sender, instance=None, created=False, **kwargs):
        if created:
            Persoon.objects.get_or_create(user=instance)

    @receiver(pre_delete, sender=User)
    def delete_on_parent(sender, instance=None, **kwargs):
        if instance:
            persoon = Persoon.objects.get(user=instance)

            persoon.delete()
