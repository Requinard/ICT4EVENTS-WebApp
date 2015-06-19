from django.contrib import admin

from .models import *

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'naam', 'locatie', 'datumstart', 'datumeinde', 'maxbezoekers')
    list_filter = ('locatie', 'datumstart', 'datumeinde')


class LocatieAdmin(admin.ModelAdmin):
    list_display = ('id', 'naam', 'straat', 'nr', 'postcode', 'plaats')
    list_filter = ('plaats',)

    search_fields = ('naam', 'straat', 'plaats')


class PlekAdmin(admin.ModelAdmin):
    list_display = ('id', 'locatie', 'nummer')
    list_display = ('id', 'locatie')

    search_fields = ('nummer',)


class PlekSpecificatieAdmin(admin.ModelAdmin):
    list_display = ('id', 'plek', 'specificatie', 'waarde')

    list_filter = ('specificatie', 'waarde')


class PolsbandjeAdmin(admin.ModelAdmin):
    list_display = ('id', 'barcode', 'actief')

    list_filter = ('actief',)


class ReserveringAdmin(admin.ModelAdmin):
    list_display = ('id', 'betaald', 'datumstart', 'datumeinde', 'persoon')
    list_filter = ('betaald', 'datumeinde', 'datumstart')


class SpecificatieAdmin(admin.ModelAdmin):
    list_display = ('id', 'naam')


class PersoonAdmin(admin.ModelAdmin):
    list_display = ('id', 'straat', 'huisnr', 'woonplaats', 'banknr', 'user')

    search_fields = ('straat', 'woonplaats')


admin.site.register(Event, EventAdmin)
admin.site.register(Locatie, LocatieAdmin)
admin.site.register(Plek, PlekAdmin)
admin.site.register(PlekSpecificatie, PlekSpecificatieAdmin)
admin.site.register(Polsbandje, PolsbandjeAdmin)
admin.site.register(Reservering, ReserveringAdmin)
admin.site.register(Specificatie, SpecificatieAdmin)
admin.site.register(Persoon, PersoonAdmin)
