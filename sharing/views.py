from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from sharing.models import Bericht


class IndexView(View):
    def get(self,request):
        context = {}
        active_event = request.user.settings.active_event
        p = Bericht.objects.filter(bijdrage__soort =  "bericht",bijdrage__event = active_event)
        context["posts"] = p
        return render(request,"sharing/index.html",context)