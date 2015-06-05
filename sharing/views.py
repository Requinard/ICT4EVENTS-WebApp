from django.utils.timezone import datetime
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import View
import sharing
from sharing.form import BerichtForm
from sharing.models import Bericht, Bijdrage, Bestand


class IndexView(View):
    context = {}
    template = "sharing/index.html"
    def get(self, request):
        active_event = request.user.settings.active_event
        p = Bericht.objects.filter(bijdrage__soort =  "bericht",bijdrage__event = active_event)
        self.context["posts"] = p
        self.context["form"] = BerichtForm()
        return render(request, self.template, self.context)


    def post(self,request):
        context = {}

        form = BerichtForm(request.POST)

        if form.is_valid():
            bijdrage = Bijdrage(event=request.user.settings.active_event, user=request.user, datum=datetime.now(), soort="bericht")
            bijdrage.save()
            bericht = Bericht(bijdrage=bijdrage, titel=form.cleaned_data["title"], inhoud=form.cleaned_data["bericht"])
            bericht.save()

            return redirect("sharing:index")

        messages.error(request, "form is niet correct ingevuld")
        context["form"] = form
        return render(request, self.template, context)
class PostView(View):
    context = {}
    template = "sharing/post.html"

    def get(self,request, post_id):
        bijdrage = get_object_or_404(Bijdrage, pk=post_id)
        p = None

        if bijdrage.soort == "bericht":
            p = Bericht.objects.get(bijdrage=bijdrage)
        else:
            p = Bestand.objects.get(bijdrage=bijdrage)

        self.context['post'] = p

        return render(request, self.template, self.context)

