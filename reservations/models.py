from django.db import models

# Create your models here.
from accounts.models import ReserveringPolsbandje


class Productcat(models.Model):
    productcategorie = models.ForeignKey('self', blank=True, null=True, related_name="+")
    naam = models.CharField(unique=True, max_length=510)

    class Meta:
        managed = True
        db_table = 'productcat'


class Productexemplaar(models.Model):
    barcode = models.CharField(unique=True, max_length=510, blank=True, null=True)

    product = models.ForeignKey('Product')

    class Meta:
        managed = True
        db_table = 'productexemplaar'

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

class Product(models.Model):
    productcategorie = models.ForeignKey('Productcat', related_name="+")
    merk = models.CharField(max_length=510, blank=True, null=True)
    serie = models.CharField(max_length=510, blank=True, null=True)
    typenummer = models.CharField(max_length=510, blank=True, null=True)
    prijs = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'product'