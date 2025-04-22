from django.shortcuts import render
from django.views import View
from products.models import Product, Category

# Create your views here.
class HomeView(View):

    template_name = 'home/home.html'


    def get(self, request):
        catehories = Category.objects.filter(parent=None)
        products = Product.objects.filter(label__name='ویژه').order_by('-created_at')
        return render(request, self.template_name, {'products':products, 'categories':catehories})


