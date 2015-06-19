from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import render, redirect
from django.core.mail import send_mail

from accounts.models import ReserveringPolsbandje
from events.models import Reservering, Persoon, Plek


# Create your views here.
from django.views.generic import View
from reservations.forms import EmailReservationForm, RegisterForm
from reservations.models import Productexemplaar, Verhuur, Product


class IndexView(View):
    context = {}
    template = "reservation/index.html"

    @method_decorator(login_required)
    def get(self, request):
        if request.session.get('cart', False) == False:
            request.session['cart'] = {}

        active_event = request.user.settings.active_event
        p = Productexemplaar.get_available_items(active_event)

        self.context["products"] = p
        if 'cart' in request.session:
            self.context['cart'] = request.session['cart']
        return render(request, self.template, self.context)


class CartView(View):
    context = {}
    template = "reservation/index.html"

    @method_decorator(login_required)
    def get(self, request, product_id):
        if request.session.get('cart', False) == False:
            request.session['cart'] = {}
        active_event = request.user.settings.active_event
        cart = {}
        if 'cart' not in request.session or request.session['cart'] == None:
            cart = {}
        else:
            cart = request.session['cart']

        cart[Productexemplaar.objects.get(id = product_id).product.serie] = product_id
        request.session['cart'] = cart
        self.context['cart'] = cart

        return redirect("reservations:index")


class CartDeleteView(View):
    context = {}
    template = "reservation/index.html"

    @method_decorator(login_required)
    def get(self, request):
        if request.session.get('cart', False) == False:
            request.session['cart'] = []
        request.session['cart'] = None
        self.context['cart'] = None

        return redirect("reservations:index")


class CartConfirmView(View):
    context = {}
    template = "reservation/index.html"

    @method_decorator(login_required)
    def get(self, request):
        if request.session.get('cart', False) == False:
            request.session['cart'] = {}
        active_event = request.user.settings.active_event
        if 'cart' in request.session:
            cart = request.session.get('cart', {})
            for product_naam in cart:
                product_exemplaar = cart[product_naam]
                datumuit = request.user.settings.active_event.datumeinde
                prijs = Productexemplaar.objects.get(id=product_exemplaar).product.prijs
                res_pk = ReserveringPolsbandje.objects.filter(account=request.user.settings)[0]
                verhuur = Verhuur(
                    productexemplaar=Productexemplaar.objects.get(id=product_exemplaar),
                    datumuit=request.user.settings.active_event.datumeinde,
                    prijs=prijs,
                    res_pb=res_pk)
                verhuur.save()
            request.session['cart'] = None
            self.context['cart'] = None
            messages.success(request, message="Item(s) succesvol gereserveerd")
            return redirect("reservations:index")
        else:
            messages.error(request, message="je winkel wagen is leeg")
            return render(request, self.template, self.context)


class PlaceReservationView(View):
    @method_decorator(login_required)
    def get(self, request):
        context = {}
        event = request.user.settings.active_event

        # Get our reservation
        reservering = Reservering.objects.filter(datumstart=event.datumstart, datumeinde=event.datumeinde,
                                                 persoon=request.user.details).first()

        if reservering:
            # Get the rest of the people on this address
            other_reservations = Reservering.objects.filter(datumstart=event.datumstart, datumeinde=event.datumeinde,
                                                            plekken=reservering.plekken)

            context['reservering'] = reservering
            context['other_reservations'] = other_reservations
        else:
            messages.error(request,'Je hebt geen plaats gereserveerd.')
        context['form'] = EmailReservationForm()

        return render(request, "reservation/placereservation.html", context)

    @method_decorator(login_required)
    def post(self, request):
        context = {}
        event = request.user.settings.active_event

        # Get our reservation
        reservering = Reservering.objects.filter(datumstart=event.datumstart, datumeinde=event.datumeinde,
                                                 persoon=request.user.details).first()

        form = EmailReservationForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]

            user = User.objects.filter(email=email)

            print(user)

            if len(user) != 1:
                messages.warning(request, "Gebruiker bestaat nog niet!")
                return redirect("reservations:place_add", reservering.plekken)

            user = user[0]

            r = Reservering.objects.get_or_create(datumstart=event.datumstart, datumeinde=event.datumeinde,
                                                  persoon=user.details, plekken=reservering.plekken)

            if r[1] == False:
                messages.error(request, "gebruiker staat al op reservering!")
            else:
                messages.success(request, "Gebruiker toegevoegd aan reservering!")

        return redirect("reservations:place")


class PlaceAddnewPerson(View):
    @method_decorator(login_required)
    def get(self, request, place_id):
        context = {}

        context['form'] = RegisterForm()

        return render(request, "reservation/addPerson.html", context)

    @method_decorator(login_required)
    def post(self, request, place_id):
        context = {}

        event = request.user.settings.active_event
        form = RegisterForm(request.POST)

        if form.is_valid():
            # get the part before the domain as username
            username = form.cleaned_data["email"].split("@")[0]

            user = User.objects.get_or_create(username=username, password="disabled", email=form.cleaned_data["email"],
                                              first_name=form.cleaned_data["first_name"],
                                              last_name=form.cleaned_data["last_name"])[0]

            user.is_active = False

            user.save()

            # now we fill in personal data

            persoon = Persoon.objects.get(user=user)

            persoon.straat = form.cleaned_data["street"]
            persoon.huisnr = form.cleaned_data["house_number"]
            persoon.woonplaats = form.cleaned_data["town"]
            persoon.banknr = form.cleaned_data["bank_number"]

            persoon.save()

            # Now that we have all the details, we make a reservation
            plek = Plek.objects.get(pk=place_id)

            r = Reservering.objects.get_or_create(plekken=plek, persoon=persoon, datumstart=event.datumstart,
                                                  datumeinde=event.datumeinde)

            # Now we send the activation email
            mail_body = "{0} heeft je uitgenodigd om mee te komen naar het{0},activeer nu je account hier http://localhost:8000/account/activate/{0}/ om mee te gaan".format(request.user.settings.naam, request.user.settings.active_event, user.settings.activatiehash)
            send_mail("Account geregistreerd voor ICT4EVENTS", mail_body, "admin@ict4events.com", [user.email, ],
                      fail_silently=False)

            return redirect("reservations:place")

        context['form'] = form

        return render(request, "reservation/addPerson.html", context)


class CurrentReservationsView(View):
    def get(self, request):
        context = {}
        reservering = request.user.settings.get_current_reservation()
        polsbandje = ReserveringPolsbandje.objects.get(reservering=reservering)

        context['verhuurs'] = Verhuur.objects.filter(res_pb=polsbandje)

        return render(request, "reservation/currentReservations.html", context)
