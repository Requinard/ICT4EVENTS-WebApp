from django.contrib import messages
from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from reservations.models import Verhuur
from staff.forms import BarcodeForm
from accounts.models import ReserveringPolsbandje


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

                context['reservering'] = polsbandje.reservering

                items = Verhuur.objects.filter(res_pb=polsbandje)
                context['items'] = items
        context['form'] = form

        return render(request, "staff/index.html", context)
