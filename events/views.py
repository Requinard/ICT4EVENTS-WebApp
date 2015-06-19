from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import View
from events.forms import PlekReserveringForm
from .models import *
from sharing.models import Bericht
import random

slogans = [
    "Van Virtueel naar Hiertueel",
    "You can't spell exciting without ICT",
    "Putting the ICT in Social Media",
    "'; DROP TABLE *;",
    "This site uses cookiedough",
    "No animals were harmed in the making of this website",
    "Why don't you take a seat right there",
    "I'm not mad, just impressed",
    "100% uptime, except when we're down",
    "85% of the time we are up 100% of the time",
    "Powered by unicorns, rainbow dust and fairy tails",
    "What's that song? Darude sandstorm",
    "<a href='https://www.youtube.com/watch?v=dQw4w9WgXcQ'>Click me</a>",
    "Turn down for patat",
    "Is het al Doner Donderdag?",
    "shrek is love. shrek is life",
    "Brought to you by Heisenberg Meth Emporium",
    "This site is running on your favourite bath salts",
    "ITS OVER 9000",
    "Your mother was a newt and your father smelt of elderberries",
    "She turned me into a newt! ... I got better.",
    "Yer a wizard harry",
    "Aloha Snackbar"
]


class IndexView(View):
    def get(self, request):
        context = {}
        context['events'] = Event.objects.all()
        if request.user.is_active:
            context['slogan'] = random.choice(slogans)
        else:
            context['slogan'] = slogans[0]
        return render(request, 'events/index.html', context)


class SetActiveEventView(View):
    @method_decorator(login_required)
    def get(self, request, event_id):
        # TODO: Schrijf unit tests hiervoor
        new_event = get_object_or_404(Event, pk=event_id)

        request.user.settings.active_event = new_event
        request.user.settings.save()

        messages.info(request, "Overgestapt naar event %s" % (new_event.naam))

        return redirect("events:index")


class EventDetailsView(View):
    @method_decorator(login_required)
    def get(self, request, event_id):
        context = {}
        Event.objects.filter(pk=event_id)
        context['event'] = get_object_or_404(Event, pk=event_id)

        if request.user.is_authenticated:
            context['registered'] = context['event'].evaluate_user_registered(request.user)

        return render(request, "events/eventdetails.html", context)

    @method_decorator(login_required)
    def post(self, request, event_id):
        return self.get(request, event_id)


class SearchView(View):
    def get(self, request, query):
        context = {}
        context['query'] = query.replace('+', ' ')

        context['result_events'] = Event.objects.filter(naam__icontains=context['query'])
        context['result_posts'] = Bericht.objects.filter(titel__icontains=context['query'])
        context['result_users'] = User.objects.filter(username__icontains=context['query'])

        return render(request, 'events/search.html', context)


class ReserveView(View):
    @method_decorator(login_required)
    def get(self, request, event_id):
        context = {}
        context['form'] = PlekReserveringForm()
        # context['places'] = Plek.objects.exclude(id__in=Reservering.plekken)
        return render(request, "events/reservation.html", context)

    @method_decorator(login_required)
    def post(self, request, event_id):
        context = {}

        event = get_object_or_404(Event, pk=event_id)

        form = PlekReserveringForm(request.POST)

        if form.is_valid():
            plek = form.cleaned_data['plek']
            datum_begin = event.datumstart
            datum_eind = event.datumeinde
            persoon = request.user.details

            ret, p = Plek.reserve(plek, persoon, datum_begin, datum_eind)

            if not p:
                plek_id = Plek.objects.get(nummer=plek)
                pers_id = persoon
                """We now know that the database does not use stored procedures, so we will save it in python"""
                reserveringen = Reservering.objects.filter(plekken=plek_id)
                if len(reserveringen) > 0:
                    ret = False
                    p = None
                else:
                    reservering = Reservering(datumstart=datum_begin, datumeinde=datum_eind, plekken=plek_id,
                                              persoon=pers_id)
                    reservering.save()
                    ret = True
                    p = reservering

            if not ret:
                messages.error(request, "Deze plek is al gereserveerd")
            else:
                messages.success(request, "Je reservering is gelukt!")
                return redirect("events:details", event_id)

            context['form'] = form

        return render(request, "events/reservation.html", context)
