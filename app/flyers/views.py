from rest_framework import generics, authentication, permissions
from flyers.serializers import FlyerSerializer
from core import models


class FlyerCategoryView(generics.ListAPIView):
    """API view for all flyers"""
    lookup_url_kwarg = 'category'
    serializer_class = FlyerSerializer

    def get_queryset(self):
        return models.Flyer.objects.filter(category=self.kwargs['category'])
