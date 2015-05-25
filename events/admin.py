from django.contrib import admin
from .models import *
# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'naam')

admin.site.register(AccountBijdrage)
admin.site.register(Bericht)
admin.site.register(Bestand)
admin.site.register(Bijdrage)
admin.site.register(BijdrageBericht)
admin.site.register(Categorie)
admin.site.register(Event, EventAdmin)
admin.site.register(Locatie)
admin.site.register(Persoon)
admin.site.register(Plek)
admin.site.register(PlekSpecificatie)
admin.site.register(Polsbandje)
admin.site.register(Product)
admin.site.register(Productcat)
admin.site.register(Productexemplaar)
admin.site.register(Reservering)
admin.site.register(ReserveringPolsbandje)
admin.site.register(Specificatie)
admin.site.register(Verhuur)