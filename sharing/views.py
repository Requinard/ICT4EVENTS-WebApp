from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.timezone import datetime
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q

# Create your views here.
from django.views.generic import View
from itertools import chain
from sharing.forms import BerichtForm, CommentForm
from sharing.models import Bericht, Bijdrage, Bestand, BijdrageBericht, AccountBijdrage, Categorie


class IndexView(View):
    context = {}
    template = "sharing/index.html"

    @method_decorator(login_required)
    def get(self, request):
        active_event = request.user.settings.active_event
        berichten = Bericht.objects.filter(bijdrage__soort=1, bijdrage__event=active_event)[:10]
        bestanden = Bestand.objects.filter(bijdrage__soort=2, bijdrage__event=active_event)[:10]

        posts = []

        for i in range(0, 10):
            try:
                posts.append(berichten[i])
            except:
                pass

            try:
                posts.append(bestanden[i])
            except:
                pass

        self.context["posts"] = posts
        self.context["form"] = BerichtForm()
        return render(request, self.template, self.context)

    @method_decorator(login_required)
    def post(self, request):
        context = {}

        form = BerichtForm(request.POST)

        if form.is_valid():
            try:
                bijdrage = Bijdrage(event=request.user.settings.active_event, user=request.user, datum=datetime.now(),
                                    soort=2)
                bijdrage.save()
                print()
                bestand = Bestand(bijdrage=bijdrage, bestandslocatie=request.FILES['bestand'],
                                  categorie=Categorie.objects.first())
                bestand.save()
            except:
                bijdrage = Bijdrage(event=request.user.settings.active_event, user=request.user, datum=datetime.now(),
                                    soort=1)
                bijdrage.save()
                bericht = Bericht(bijdrage=bijdrage, titel=form.cleaned_data["title"],
                                  inhoud=form.cleaned_data["bericht"])
                bericht.save()
            return redirect("sharing:index")

        messages.error(request, "form is niet correct ingevuld")
        context["form"] = form
        return render(request, self.template, context)


class PostView(View):
    context = {}
    template = ""

    @method_decorator(login_required)
    def get(self, request, post_id):
        bijdrage = get_object_or_404(Bijdrage, pk=post_id)
        self.context["form"] = CommentForm()
        p = None

        if bijdrage.soort == 1:
            p = Bericht.objects.get(bijdrage=bijdrage)
        else:
            p = Bestand.objects.get(bijdrage=bijdrage)

        self.context['post'] = p

        return render(request, "sharing/post.html", self.context)

    @method_decorator(login_required)
    def post(self, request, post_id):
        context = {}
        form = CommentForm(request.POST)

        if form.is_valid():
            bijdrage = Bijdrage(event=request.user.settings.active_event, user=request.user, datum=datetime.now(),
                                soort=5)
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

    @method_decorator(login_required)
    def get(self, request, post_id, modus):
        bijdrage = get_object_or_404(Bijdrage, pk=post_id)
        accountbijdrage = AccountBijdrage.objects.get_or_create(bijdrage=bijdrage, user=request.user)[0]
        if modus == "like":
            accountbijdrage.like = True
        elif modus == "report":
            accountbijdrage.ongewenst = True
        accountbijdrage.save()
        return redirect("sharing:post_details", post_id)
