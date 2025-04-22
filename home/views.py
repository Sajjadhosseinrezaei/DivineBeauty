from django.shortcuts import render
from django.views import View
from products.models import Product

# Create your views here.
class HomeView(View):

    template_name = 'home/home.html'


    def get(self, request):
        products = Product.objects.filter(label__name='ویژه').order_by('-created_at')
        return render(request, self.template_name, {'products':products})


