from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'home'

# URL patterns for the home app
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('search/', views.SearchProductView.as_view(), name='search_product'),
    path('faq/', views.FAQView.as_view(), name='faq'),
    path('about/', TemplateView.as_view(template_name='home/about.html'), name='about'),
]
