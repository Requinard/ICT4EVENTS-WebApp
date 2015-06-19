from datetime import datetime

from django.db import models


# Create your models here.
from accounts.models import ReserveringPolsbandje


class Productcat(models.Model):
    productcategorie = models.ForeignKey('self', blank=True, null=True, related_name="+")
    naam = models.CharField(unique=True, max_length=510)

    class Meta:
        managed = True
        db_table = 'productcat'

    def __str__(self):
        return self.naam


class Productexemplaar(models.Model):
    barcode = models.CharField(unique=True, max_length=510, blank=True, null=True)

    product = models.ForeignKey('Product')

    def is_available(self, event):
        verhuurs = Verhuur.objects.filter(productexemplaar=self, datumuit=event.datumeinde)
        y = {x.productexemplaar for x in verhuurs}
        return self not in y

    @staticmethod
    def get_available_items(event):
        return {x for x in Productexemplaar.objects.all() if x.is_available(event)}

    def __str__(self):
        return "{0} - Barcode: {1}".format(self.product, self.barcode)

    class Meta:
        managed = True
        db_table = 'productexemplaar'


class Verhuur(models.Model):
    productexemplaar = models.ForeignKey(Productexemplaar, blank=True, null=True)
    res_pb = models.ForeignKey(ReserveringPolsbandje, blank=True, null=True)
    datumin = models.DateField(blank=True, null=True, default=datetime.now())
    datumuit = models.DateField(blank=True, null=True)
    prijs = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)
    betaald = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'verhuur'


class Product(models.Model):
    productcategorie = models.ForeignKey('Productcat', related_name="+")
    merk = models.CharField(max_length=510, blank=True, null=True)
    serie = models.CharField(max_length=510, blank=True, null=True)
    typenummer = models.CharField(max_length=510, blank=True, null=True)
    prijs = models.DecimalField(max_digits=19, decimal_places=2, blank=True, null=True)

    #product_image = models.FileField(upload_to="product/%Y/%m/%d", null=True, blank=True)

    class Meta:
        managed = True
        db_table = 'product'

    def __str__(self):
        return "{0} {1} {2}".format(self.productcategorie, self.merk, self.serie)
