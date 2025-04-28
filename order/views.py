from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from products.models import Product
from .models import Cart, CartItem
from django.contrib import messages
from utility import redirect_with_next
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class AddCartItem(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart, created= Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=kwargs['id'])
        cart.add_to_cart(product=product)
        return redirect_with_next(request, 'order:cart_detail')






class RemoveCartItemView(LoginRequiredMixin, View):
    
    def post(self,request, product_id):
        product = get_object_or_404(Product, id=product_id)
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        if cart_item:
            try:
                cart_item.del_cart_item()
                messages.success(request, f'{product.name} از سبد خرید شما حذف شد.')
            
            except:
                messages.error(request, "نتوانستیم حذف کنیم دوباره امتحان کنید")
            
            return redirect('order:cart_detail')
        

class UpdateCartQuantityView(LoginRequiredMixin, View):

    def post(self, request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id)
        quantity = request.POST.get('quantity')

        if quantity:
            try:
                quantity = int(quantity)
                cart_item.update_cart_quantity(quantity)
                messages.success(request, "مقدار کالا با موفقیت به‌روزرسانی شد.")
            except (ValueError, ValidationError) as e:
                messages.error(request, str(e))
            except Exception as e:
                messages.error(request, "خطایی رخ داد. لطفاً دوباره تلاش کنید.")
        else:
            messages.error(request, "تعداد معتبر وارد نشده است.")

        return redirect('order:cart_detail')  # آدرس صفحه سبد



