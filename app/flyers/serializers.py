
from rest_framework import serializers
from core import models


class FlyerSerializer(serializers.ModelSerializer):
    """Serializer for the flyers object"""
    class Meta:
        model = models.Flyer
        fields = "__all__"
