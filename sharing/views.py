from django.utils.timezone import datetime
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from django.views.generic import View
import sharing
from sharing.forms import BerichtForm, CommentForm
from sharing.models import Bericht, Bijdrage, Bestand, BijdrageBericht, AccountBijdrage


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
        self.context["form"] = CommentForm()
        p = None

        if bijdrage.soort == "bericht":
            p = Bericht.objects.get(bijdrage=bijdrage)
        else:
            p = Bestand.objects.get(bijdrage=bijdrage)

        self.context['post'] = p

        return render(request, self.template, self.context)

    def post(self, request, post_id):
        context = {}
        form = CommentForm(request.POST)

        if form.is_valid():
            bijdrage = Bijdrage(event=request.user.settings.active_event, user=request.user, datum=datetime.now(), soort="bericht")
            bijdrage.save()
            bericht = Bericht(bijdrage=bijdrage, inhoud=form.cleaned_data["bericht"])
            bericht.save()
            bijdrage_bericht = BijdrageBericht(bijdrage=Bijdrage.objects.get(id=post_id), bericht=bericht)
            bijdrage_bericht.save()
            return redirect("sharing:post_details", post_id)
        else:
            messages.error(request, "form is niet correct ingevuld")
            context["form"] = form
            return render(request, self.template, context)

class LikeReportView(View):
    context = {}
    template = "sharing/post.html"

    def get(self, request, post_id,modus):
        bijdrage = get_object_or_404(Bijdrage, pk=post_id)
        accountbijdrage = AccountBijdrage.objects.get_or_create(bijdrage=bijdrage,user=request.user)[0]
        if modus == "like":
            accountbijdrage.like = True
        elif modus == "report":
            accountbijdrage.ongewenst = True
        accountbijdrage.save()
        return redirect("sharing:post_details", post_id)
