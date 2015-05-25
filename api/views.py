from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from api.serializers import PlekSerializer
from rest_framework.generics import ListAPIView, ListCreateAPIView
from events.models import PlekSpecificatie


class PlekAutocompleteViewset(ListCreateAPIView):
    serializer_class = PlekSerializer

    def get_queryset(self):
        name = self.kwargs['name']
        plekken = PlekSpecificatie.objects.filter(waarde__icontains=name)
        return plekken