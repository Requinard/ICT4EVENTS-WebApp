# Create your views here.
from django.db.models import Q
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView

from api.serializers import PlekSerializer, PlekSpecificatieSerializer
from events.models import PlekSpecificatie, Plek


class PlekAutocompleteViewset(ListCreateAPIView):
    serializer_class = PlekSpecificatieSerializer

    def get_queryset(self):
        name = self.kwargs['name']
        plekken = PlekSpecificatie.objects.filter(Q(plek__nummer__icontains=str(name)) | Q(plek__nummer=str(name)))
        return plekken


class PlekViewset(viewsets.ModelViewSet):
    serializer_class = PlekSerializer
    queryset = Plek.objects.all()
