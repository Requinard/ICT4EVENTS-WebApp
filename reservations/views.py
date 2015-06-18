from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.utils.timezone import datetime
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import ReserveringPolsbandje
from events.models import Polsbandje, Reservering
import reservations

# Create your views here.
from django.views.generic import View
from reservations.forms import EmailReservationForm, RegisterForm
from reservations.models import Product, Productexemplaar, Verhuur


class IndexView(View):
    context = {}
    template = "reservation/index.html"

    @method_decorator(login_required)
    def get(self, request):
        active_event = request.user.settings.active_event
        p = Productexemplaar.get_available_items(active_event)

        self.context["products"] = p
        self.context['cart'] = request.session['cart']
        return render(request, self.template, self.context)

class CartView(View):
    context = {}
    template = "reservation/index.html"

    @method_decorator(login_required)
    def get(self,request,product_id):
        active_event = request.user.settings.active_event
        cart = {}
        if 'cart' not in request.session or request.session['cart'] == None:
            cart = {}
        else:
            cart = request.session['cart']

        cart[product_id] = 1
        request.session['cart'] = cart
        self.context['cart'] = cart

        return redirect("reservations:index")

class CartDeleteView(View):
    context = {}
    template = "reservation/index.html"

    @method_decorator(login_required)
    def get(self,request):
        request.session['cart'] = None
        self.context['cart'] = None

        return redirect("reservations:index")


class CartConfirmView(View):
    context = {}
    template = "reservation/index.html"

    @method_decorator(login_required)
    def get(self,request):
        active_event = request.user.settings.active_event
        if 'cart' in request.session:
            cart = request.session.get('cart', {})
            for product_exemplaar in cart:
                    datumuit = request.user.settings.active_event.datumeinde
                    prijs  = Productexemplaar.objects.get(id=product_exemplaar).product.prijs
                    res_pk = ReserveringPolsbandje.objects.filter(account=request.user.settings)[0]
                    verhuur = Verhuur(
                        productexemplaar=Productexemplaar.objects.get(id=product_exemplaar),
                        datumuit=request.user.settings.active_event.datumeinde,
                        prijs= prijs,
                        res_pb=res_pk)
                    verhuur.save()
            request.session['cart'] = None
            self.context['cart'] = None
            messages.success(request,message="Item(s) succesvol gereserveerd")
            return redirect("reservations:index")
        else:
            messages.error(request,message="je winkel wagen is leeg")
            return render(request,self.template,self.context)

class PlaceReservationView(View):
    @method_decorator(login_required)
    def get(self, request):
        context = {}
        event = request.user.settings.active_event

        # Get our reservation
        reservering = Reservering.objects.filter(datumstart=event.datumstart, datumeinde=event.datumeinde, persoon=request.user.details).first()

        # Get the rest of the people on this address
        other_reservations = Reservering.objects.filter(datumstart=event.datumstart, datumeinde=event.datumeinde, plekken=reservering.plekken)

        context['reservering'] = reservering
        context['other_reservations'] = other_reservations
        context['form'] = EmailReservationForm()

        return render(request, "reservation/placereservation.html", context)

    @method_decorator(login_required)
    def post(self, request):
        context = {}
        event = request.user.settings.active_event

        # Get our reservation
        reservering = Reservering.objects.filter(datumstart=event.datumstart, datumeinde=event.datumeinde, persoon=request.user.details).first()

        form = EmailReservationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            user = User.objects.filter(email=email)

            print(user)

            if len(user) != 1:
                messages.warning(request, "Gebruiker bestaat nog niet!")
                return redirect("reservations:place_add", reservering.plekken)

            user = user[0]

            r = Reservering.objects.get_or_create(datumstart=event.datumstart, datumeinde=event.datumeinde, persoon=user.details, plekken=reservering.plekken)

            if r[1] == False:
                messages.error(request, "gebruiker staat al op reservering!")
            else:
                messages.success(request, "Gebruiker toegevoegd aan reservering!")


        return redirect("reservations:place")

class PlaceAddnewPerson(View):
    def get(self, request, place_id):
        context = {}

        context['form'] = RegisterForm()

        return render(request, "reservation/addPerson.html", context)


