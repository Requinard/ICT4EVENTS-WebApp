from django.contrib import messages
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import View
from events.models import Polsbandje
from reservations.models import Verhuur, Product, Productcat, Productexemplaar
from staff.forms import BarcodeForm
from accounts.models import ReserveringPolsbandje
import random

class IndexView(View):
    def get(self, request):
        context = {}

        context['form'] = BarcodeForm()

        return render(request, "staff/index.html", context)

    def post(self, request):
        context = {}

        form = BarcodeForm(request.POST)

        if form.is_valid():
            barcode = form.cleaned_data["barcode"]

            polsbandje = ReserveringPolsbandje.objects.filter(polsband__barcode=barcode)

            if len(polsbandje) == 0:
                messages.error(request, "geen polsbandje gevonden")
                form = BarcodeForm()
            else:
                messages.success(request, "polsbandje gevonden!")
                polsbandje = polsbandje.first()
                polsbandje.aanwezig = True
                polsbandje.save()

                context['reservering'] = polsbandje.reservering

                items = Verhuur.objects.filter(res_pb=polsbandje)
                context['items'] = items
        context['form'] = form

        return render(request, "staff/index.html", context)

class GenerateView(View):
    def get(self, request):
        self.generatePolsbandje()
        #self.generateProducts()
        return redirect("staff:index")

    def generatePolsbandje(self):
        try:
            for i in range(1000, 10000):
                p = Polsbandje(barcode=i, actief=False)
                p.save()
        except:
            pass

    def generateProducts(self):
        procat = Productcat.objects.get_or_create(naam="test")[0]
        product = Product(productcategorie=procat, merk="Lenovo", serie="Y510p", typenummer="5", prijs=500)
        product.save()

        for i in range(0, 10):
            b = random.randint(1000, 10000000)
            pe = Productexemplaar(barcode=b, product=product)

            pe.save()

        product = Product(productcategorie=procat, merk="Kruidvat", serie="Tandenborstel", typenummer="Ultimate", prijs=10)
        product.save()

        for i in range(0, 10):
            b = random.randint(1000, 10000000)
            pe = Productexemplaar(barcode=b, product=product)

            pe.save()

        product = Product(productcategorie=procat, merk="Slaapzak", serie="Super Deluxe", typenummer="Ultimate", prijs=100)
        product.save()

        for i in range(0, 10):
            b = random.randint(1000, 10000000)
            pe = Productexemplaar(barcode=b, product=product)

            pe.save()