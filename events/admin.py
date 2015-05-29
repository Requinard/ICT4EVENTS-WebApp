from django.contrib import admin

from accounts.models import ReserveringPolsbandje
from .models import *

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'naam')

admin.site.register(Event, EventAdmin)
admin.site.register(Locatie)
admin.site.register(Plek)
admin.site.register(PlekSpecificatie)
admin.site.register(Polsbandje)
admin.site.register(Reservering)
admin.site.register(Specificatie)
admin.site.register(Persoon)