from django.shortcuts import render
from rest_framework import viewsets
from products.models import Product
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
# Create your views here.
class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    


class ProductViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing product instances.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'
    pagination_class = CustomPagination
    def create(self, request, *args, **kwargs):
        # بررسی اینکه داده‌ها لیست هستند یا خیر
        data = request.data
        if isinstance(data, list):
            # پردازش داده‌ها به‌صورت گروهی
            serializer = self.get_serializer(data=data, many=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # رفتار پیش‌فرض برای ایجاد یک محصول
            return super().create(request, *args, **kwargs)