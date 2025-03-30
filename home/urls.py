from django.urls import path
from django.views.generic import TemplateView


app_name = 'home'

# URL patterns for the home app
urlpatterns = [
    path('', TemplateView.as_view(template_name='home/home.html'), name='home'),

]
