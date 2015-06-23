from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import View
from ICT4EVENTS.decorators import event_is_active
from events.models import Polsbandje, Specificatie, Locatie, Plek, PlekSpecificatie
from reservations.models import Verhuur, Product, Productcat, Productexemplaar
from staff.forms import BarcodeForm
from accounts.models import ReserveringPolsbandje
import random
from django.contrib.admin.views.decorators import staff_member_required

class IndexView(View):
    @method_decorator(login_required)
    @method_decorator(event_is_active)
    def get(self, request):
        context = {}

        context['form'] = BarcodeForm()

        return render(request, "staff/index.html", context)

    @method_decorator(login_required)
    @method_decorator(event_is_active)
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
    @method_decorator(login_required)
    def get(self, request):
        if not request.user.is_superuser:
            messages.error(request, "You are not allowed to view this page")
            return redirect("events:index")

        self.generatePolsbandje()
        self.generateProducts()
        self.generatePlaces()

        return redirect("staff:index")

    def generatePlaces(self):
        l = Locatie.objects.get_or_create(naam="Camping Reeendael")
        spec1 = Specificatie.objects.get_or_create(naam="Lawaai")[0]
        spec1val = ["Hoog", "Gemiddeld", "Laag"]
        spec2 = Specificatie.objects.get_or_create(naam="Comfort")[0]
        spec3 = Specificatie.objects.get_or_create(naam="Huisvesting")[0]
        spec3val = ["Bungalow", "Tent", "Groepstent", "Tipi", "Caravan", "Camper"]
        loc = Locatie.objects.all().first()

        for i in range(1, 667):
            p = Plek.objects.get_or_create(nummer=str(i), capaciteit=random.choice(range(1,10)), locatie=loc)[0]

            ps = PlekSpecificatie(plek=p, specificatie=spec1, waarde=random.choice(spec1val))
            ps.save()
            ps = PlekSpecificatie(plek=p, specificatie=spec2, waarde=random.choice(spec1val))
            ps.save()
            ps = PlekSpecificatie(plek=p, specificatie=spec3, waarde=random.choice(spec3val))
            ps.save()


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