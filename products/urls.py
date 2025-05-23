from django.urls import path, re_path
from . import views


app_name = 'products'
urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    re_path(r'^(?P<slug>[\w-]+)/$', views.ProductDetailView.as_view(), name='product_detail'),
    re_path(r'^category/(?P<slug>[\w-]+)/$', views.ProductListView.as_view(), name='product_list_by_category'),
    path('comment/create/<int:id>/', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/delete/<int:id>/', views.CommentDeleteView.as_view(), name='comment_delete'),
]
