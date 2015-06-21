from django.contrib import admin

from .models import Bijdrage, Bericht, BijdrageBericht, Bestand, Categorie
# Register your models here.
class BijdrageAdmin(admin.ModelAdmin):
    list_display = ("id", "soort", "datum", "user", "event")
    list_filter = ("event", "datum", "soort")

class BerichtAdmin(admin.ModelAdmin):
    list_display = ("id", "titel", "inhoud")
    search_fields = ("titel__icontains", "berict__icontains")

class BestandAdmin(admin.ModelAdmin):
    list_display = ("id", "bestandslocatie", "categorie")

class BijdrageBerichtAdmin(admin.ModelAdmin):
    list_display = ("id", "bijdrage", "bericht")

class CategorieAdmin(admin.ModelAdmin):
    list_display = ("id", "naam")

admin.site.register(Bijdrage, BijdrageAdmin)
admin.site.register(Bericht, BerichtAdmin)
admin.site.register(Bestand, BestandAdmin)
admin.site.register(Categorie, CategorieAdmin)
admin.site.register(BijdrageBericht, BijdrageBerichtAdmin)
