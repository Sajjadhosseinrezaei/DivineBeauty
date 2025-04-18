from django.urls import path, re_path
from . import views


app_name = 'products'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    re_path(r'^(?P<slug>[\w-]+)/$', views.ProductDetailView.as_view(), name='product_detail'),
]
