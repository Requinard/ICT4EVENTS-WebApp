from rest_framework import serializers
from events.models import PlekSpecificatie


class PlekSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlekSpecificatie