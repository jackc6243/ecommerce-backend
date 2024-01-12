"""
Views for products api
"""

from rest_framework import generics, authentication, permissions
from products.serializers import ProductSerializer
from core import models

from datetime import datetime, timedelta


class AllProductView(generics.ListAPIView):
    """API view for all products"""
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer


class NewProductView(generics.ListAPIView):
    queryset = models.Product.objects.filter(
        creation_date__gte=datetime.now()-timedelta(days=60))
    serializer_class = ProductSerializer


class DiscountProductView(generics.ListAPIView):
    queryset = models.Product.objects.filter(discount__lt=0.99)
    serializer_class = ProductSerializer


class CategoryProductView(generics.ListAPIView):
    lookup_url_kwarg = 'category'
    serializer_class = ProductSerializer

    def get_queryset(self):
        return models.Product.objects.filter(category=self.kwargs['category'])


class RetrieveSingleProduct(generics.RetrieveAPIView):
    queryset = models.Product.objects.all()
    serializer_class = ProductSerializer
