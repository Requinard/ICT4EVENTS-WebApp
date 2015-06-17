from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.utils.timezone import datetime
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import ReserveringPolsbandje
from events.models import Polsbandje
import reservations

# Create your views here.
from django.views.generic import View
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
