from django.shortcuts import render
from django.contrib import messages
# Create your views here.
from django.views.generic import View
from .models import *

class IndexView(View):
    def get(self, request):
        context = {}
        context['events'] = Event.objects.all()
        return render(request, 'base.html', context)