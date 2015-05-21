from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# Create your views here.
from django.views.generic import View
from .models import *

class IndexView(View):
    def get(self, request):
        context = {}
        context['events'] = Event.objects.all()
        return render(request, 'events/index.html', context)

class SetActiveEventView(View):
    def get(self, request, event_id):
        #TODO: Schrijf unit tests hiervoor
        new_event = get_object_or_404(Event, pk=event_id)

        request.user.settings.active_event = new_event

        messages.info(request, "Overgestapt naar event %s" % (new_event.naam))

        return redirect("events:index")

class SearchView(View):
    def get(self, request, query):
        context = {}
        context['query'] = query.replace('+', ' ')
        return render(request, 'events/search.html', context)