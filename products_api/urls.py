from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views



router = DefaultRouter()
router.register(r'products', views.ProductViewSet, basename='products')

app_name = 'products_api'

urlpatterns = [
    path('', include(router.urls)),
    path('comments/', views.Comments.as_view(), name='comments'),
    path('comments/<int:id>/', views.CommentDetail.as_view(), name='comment_detail'),
    path('categories/', views.CategoryListView.as_view(), name='categories'),
]
