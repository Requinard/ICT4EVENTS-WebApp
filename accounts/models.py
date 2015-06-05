from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from events.models import Event, Reservering, Persoon, Polsbandje
from sharing.models import Bericht


class Account(models.Model):
    gebruiker = models.OneToOneField(User, related_name="settings")
    activatiehash = models.CharField(max_length=510)
    active_event = models.ForeignKey(Event, null=True, blank=True)
    geactiveerd = models.BooleanField()
    active_theme = models.IntegerField(choices=(
        (1, 'Material Design'),
        (2, 'Metro'),
        (3, 'I328 Terminal'),
        (4, 'Bootsflat'),
        (5, 'Basic'),
    ), default=1)

    profile_picture = models.FileField(blank=True, null=True, upload_to='profilepictures/%Y/%m/%d')

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
        return str(self.gebruiker.username)

    def get_reservations(self):
        events = []

        reservations = Reservering.objects.filter(persoon=self.gebruiker.details)

        for r in reservations:
            plekken = r.plekken

            for p in plekken.all():
                print(p.locatie)
                event = Event.objects.filter(locatie=p.locatie, datumstart__lte=r.datumstart, datumeinde__gte=r.datumeinde)
                for e in event:
                    events.append(e)

        return events

    def get_posts(self):
        return Bericht.objects.filter(bijdrage__user=self.gebruiker)

class ReserveringPolsbandje(models.Model):
    polsband = models.ForeignKey(Polsbandje)
    reservering = models.ForeignKey(Reservering)
    account = models.ForeignKey(Account)

    aanwezig = models.BooleanField(default=False)

    class Meta:
        managed = True
        db_table = 'reservering_polsbandje'

    def __str__(self):
        return self.polsband