from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product, Category

# Create your views here.

class ProductListView(ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10  # تعداد محصولات در هر صفحه
    model = Product
    ordering = ['-created_at']  # مرتب‌سازی بر اساس تاریخ ایجاد (جدیدترین اول)
    allow_empty = True  # اجازه نمایش صفحه خالی در صورت عدم وجود محصول
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(parent=None)
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slug = self.kwargs.get('slug')
        if category_slug:
            try:
                category = Category.objects.get(slug=category_slug)
                descendants = category.get_descendants(include_self=True)
                queryset = queryset.filter(category__in=descendants)
            except Category.DoesNotExist:
                queryset = queryset.none()
        return queryset
    



    
        


class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    model = Product
    slug_field = 'slug'  # نام فیلد اسلاگ در مدل
    slug_url_kwarg = 'slug'  # نام پارامتر URL که اسلاگ را دریافت می‌کند
    