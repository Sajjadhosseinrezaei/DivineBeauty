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
        cart, created = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, id=kwargs['id'])

        quantity = request.POST.get('quantity', 1)
        try:
            quantity = int(quantity)
            if quantity <= 0:
                raise ValueError("تعداد باید بزرگتر از صفر باشد.")
        except (ValueError, TypeError):
            messages.error(request, "تعداد نامعتبر است.")
            return redirect_with_next(request, 'products:product_detail', product_id=product.id)

        if created:
            if quantity > product.stock:
                messages.error(request, "موجودی کافی برای این محصول وجود ندارد.")
                return redirect_with_next(request, 'order:cart_detail')

            cart.add_to_cart(product=product, quantity=quantity)
            messages.success(request, f"{product.name} با موفقیت به سبد خرید اضافه شد.")
            return redirect_with_next(request, 'order:cart_detail')

        else:
            cart_item = Cart.objects.get(user=request.user).items.filter(product=product).first()
            if cart_item:
                quantity_with_cart_quantity = cart_item.quantity + quantity
                if quantity_with_cart_quantity > product.stock:
                    messages.error(request, "تعداد وارد شده از تعداد موجود در سبد خرید بیشتر است.")
                    return redirect_with_next(request, 'order:cart_detail')
            else:
                quantity_with_cart_quantity = quantity
                
            cart.add_to_cart(product=product, quantity=quantity)
            messages.success(request, f"{product.name} با موفقیت به سبد خرید اضافه شد.")
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
        else:
            messages.error(request, "محصول مرود نظر در سبد خرید شما پیدا نشد")
            return redirect('order:cart_detail')
        
        

class UpdateCartQuantityView(LoginRequiredMixin, View):
    def dispatch(self, request, *args, **kwargs):
        self.cart_item = get_object_or_404(CartItem, id=kwargs['cart_item_id'], cart__user=request.user)
        
        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            messages.error(request, "مقدار تعداد معتبر نیست.")
            return redirect('order:cart_detail')
        
        if self.cart_item.quantity == quantity:
            messages.error(request, "تعداد کالا در سبد خرید شما با مقدار وارد شده برابر است.")
            return redirect('order:cart_detail')

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, cart_item_id):
        quantity = request.POST.get('quantity')
        try:
            quantity = int(quantity)
            self.cart_item.update_cart_quantity(quantity)
            messages.success(request, "مقدار کالا با موفقیت به‌روزرسانی شد.")
        except (ValueError, ValidationError) as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, "خطایی رخ داد. لطفاً دوباره تلاش کنید.")

        return redirect('order:cart_detail')  # آدرس صفحه سبد



