from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from django.views.generic import View
from .models import *

class IndexView(View):
    def get(self, request):
        context = {}
        messages.success(request, "Messages werken!")
        messages.warning(request, "Er ging iets fout")
        messages.error(request, "dit is een error")
        context['events'] = Event.objects.all()
        return render(request, 'base.html', context)