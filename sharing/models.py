from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from events.models import Event


class AccountBijdrage(models.Model):
    bijdrage = models.ForeignKey('Bijdrage')
    like = models.BooleanField(default=False)
    ongewenst = models.BooleanField(default=False)

    user = models.ForeignKey(User)

    class Meta:
        managed = True
        db_table = 'account_bijdrage'


class Bericht(models.Model):
    bijdrage = models.OneToOneField('Bijdrage')
    titel = models.CharField(max_length=510, blank=True, null=True)
    inhoud = models.CharField(max_length=255)

    def get_child_comments(self):
        bijdrages = BijdrageBericht.objects.filter(bijdrage_id=self.bijdrage.id)
        comments = [x.bericht for x in bijdrages]

        return comments

    class Meta:
        managed = True
        db_table = 'bericht'
        ordering = ("-id",)


class Bestand(models.Model):
    bijdrage = models.OneToOneField('Bijdrage')
    categorie = models.ForeignKey('Categorie')
    bestandslocatie = models.FileField(upload_to='user_uploads/%Y/%m/%d')

    def get_child_comments(self):
        bijdrages = BijdrageBericht.objects.filter(bijdrage_id=self.bijdrage.id)
        comments = [x.bericht for x in bijdrages]

        return comments

    class Meta:
        managed = True
        db_table = 'bestand'
        ordering = ("-id",)


class Bijdrage(models.Model):
    datum = models.DateField(blank=True, null=True)
    soort = models.IntegerField(choices=(
        (1, 'bericht'),
        (2, 'bestand'),
        (3, 'categorie'),
        (4, 'account'),
        (5, 'comment'),
    ))

    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)

    def get_like_count(self):
        return AccountBijdrage.objects.filter(bijdrage=self, like=True).count()

    def get_report_count(self):
        return AccountBijdrage.objects.filter(bijdrage=self, ongewenst=True).count()

    class Meta:
        managed = True
        db_table = 'bijdrage'
        ordering = ("id",)


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

    def __str__(self):
        if self.categorie_gerelateerd is None:
            return self.naam
        else:
            return "{0} < {1}".format(self.naam, self.categorie_gerelateerd)
