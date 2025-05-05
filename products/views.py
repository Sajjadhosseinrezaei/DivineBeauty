from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Product, Category, Comment
from django.views import View
from django.contrib import messages
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        comments = Comment.objects.filter(product=product)
        context['comments'] = comments
        if product.attributes:
            context['product_attributes'] = product.attributes.items()
        return context


class CommentCreateView(View):
    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('id')
        product = get_object_or_404(Product, id=product_id)
        parent_id = request.POST.get('parent')
        parent = None
        if parent_id:
            try:
                parent = Comment.objects.get(id=parent_id)
            except Comment.DoesNotExist:
                parent = None
        comment = Comment(
            product=product,
            user=request.user,
            comment=request.POST.get('comment'),
            parent=parent
        )
        comment.save()
        messages.success(request, 'نظر شما با موفقیت ثبت شد.')
        return redirect('products:product_detail', product.slug)
    

class CommentDeleteView(View):
    def post(self, request, *args, **kwargs):
        comment_id = self.kwargs.get('id')
        comment = get_object_or_404(Comment, id=comment_id)
        comment.delete()
        messages.success(request, 'نظر شما با موفقیت حذف شد.')
        return redirect('products:product_detail', comment.product.slug)