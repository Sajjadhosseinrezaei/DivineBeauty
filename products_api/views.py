from django.shortcuts import render
from rest_framework import viewsets
from products.models import Product
from .serializers import ProductSerializer
# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'