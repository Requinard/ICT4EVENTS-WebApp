from django.contrib import admin

from .models import Bijdrage, Bericht, BijdrageBericht, Bestand, Categorie
# Register your models here.

admin.site.register(Bijdrage)
admin.site.register(Bericht)
admin.site.register(Bestand)
admin.site.register(Categorie)
admin.site.register(BijdrageBericht)
