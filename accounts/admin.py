from django.contrib import admin

from .models import *

class ReserveringsPolsbandjeAdmin(admin.ModelAdmin):
    list_filter = ("aanwezig", "reservering__plekken__locatie")

# Register your models here.
admin.site.register(Account)
admin.site.register(ReserveringPolsbandje, ReserveringsPolsbandjeAdmin)
