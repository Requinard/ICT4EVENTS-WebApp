from rest_framework import serializers

from events.models import PlekSpecificatie, Plek


class PlekSpecificatieSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlekSpecificatie
        depth = 1


class PlekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Plek
