from django.shortcuts import render
from django.views import View
from products.models import Product, Category
from django.views.generic import ListView
from .models import FAQ, FAQCategory

# Create your views here.
class HomeView(View):

    template_name = 'home/home.html'


    def get(self, request):
        categories = Category.objects.filter(parent=None)
        products = Product.objects.filter(label__name='ویژه').order_by('-created_at')
        return render(request, self.template_name, {'products':products, 'categories':categories})


class SearchProductView(ListView):
    template_name = 'home/search.html'
    context_object_name = 'products'
    paginate_by = 10  # تعداد محصولات در هر صفحه
    model = Product

    def get_queryset(self):
        search_query = self.request.GET.get('search')
        if search_query:
            return Product.objects.filter(name__icontains=search_query)
        return Product.objects.none()

class FAQView(ListView):
    template_name = 'home/FAQ.html'
    context_object_name = 'categories_fqa'
    paginate_by = 10
    model = FAQCategory

    def get_queryset(self):
        slug = self.request.GET.get('category')
        if slug:
            return FAQCategory.objects.filter(slug=slug).prefetch_related('faqs')
        return FAQCategory.objects.prefetch_related('faqs').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected'] = self.request.GET.get('category')
        return context


    
