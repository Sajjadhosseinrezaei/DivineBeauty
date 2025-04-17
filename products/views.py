from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product

# Create your views here.

class ProductListView(ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 10  # تعداد محصولات در هر صفحه
    model = Product
    ordering = ['-created_at']  # مرتب‌سازی بر اساس تاریخ ایجاد (جدیدترین اول)
    allow_empty = True  # اجازه نمایش صفحه خالی در صورت عدم وجود محصول
    empty_label = 'محصولی وجود ندارد'  # متن نمایش داده شده در صورت عدم وجود محصول


class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'
    context_object_name = 'product'
    model = Product
    slug_field = 'slug'  # نام فیلد اسلاگ در مدل
    slug_url_kwarg = 'slug'  # نام پارامتر URL که اسلاگ را دریافت می‌کند
    