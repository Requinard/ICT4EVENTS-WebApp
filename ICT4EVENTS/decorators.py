from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect


def event_is_active(function):
    def wrap(request, *args, **kwargs):
        if request.user.settings.active_event is None:
            messages.error(request, "Je hebt nog geen inschrijving voor een event")
            return redirect("events:index")
        else:
            return function(request, *args, **kwargs)


    wrap.__doc__=function.__doc__
    wrap.__name__=function.__name__
    return wrap