from typing import Any
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from products.models import Product
from .models import Cart, CartItem, Order, OrderItem, Payment
from django.contrib import messages
from utility import redirect_with_next
from django.core.exceptions import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from constance import config
# Create your views here.


class AddCartItem(LoginRequiredMixin, View):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            if request.method == 'POST':
                request.session['pending_add_to_cart'] = {
                    'product_id': kwargs['id'],
                    'quantity': request.POST.get('quantity', 1)
                }
                return redirect(request.get_full_path())

        
        return super().dispatch(request, *args, **kwargs)
    

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
            if 'pending_add_to_cart' in request.session:
                del request.session['pending_add_to_cart']
            return redirect_with_next(request, 'order:cart_detail')


            
class ResumeAddToCartView(LoginRequiredMixin, View):

    template_name = 'order/resume_add_to_cart.html'

    def get(self, requset, *args, **kwargs):
        data = requset.session.pop('pending_add_to_cart', None)
        if not data:
            return redirect_with_next(requset, 'home:home')
        
        return render(requset, self.template_name, {
            'product_id': data['product_id'],
            'quantity': data['quantity'],
        })




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



class AddCartItemToOrderView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)

        # اعتبارسنجی فرم
        address = request.POST.get('address', '').strip()
        postal_code = request.POST.get('postal_code', '').strip()
        receiver_name = request.POST.get('receiver_name', '').strip()
        receiver_phone_number = request.POST.get('receiver_phone_number', '').strip()
        type_of_payment = request.POST.get('type_of_payment', '').strip()
        if type_of_payment == 'online':
            if not config.ONLINE_PAYMENT_ENABLED:
                messages.warning(request, "پرداخت آنلاین فعلا قابل استفاده نیست.")
                return redirect('order:cart_detail')

        if not all([address, postal_code, receiver_name, receiver_phone_number, type_of_payment]):
            messages.warning(request, "لطفاً تمام فیلدهای اطلاعات ارسال را تکمیل کنید.")
            return redirect('order:cart_detail')

        # بررسی خالی نبودن سبد خرید
        if not cart.items.exists():
            messages.warning(request, "سبد خرید شما خالی است.")
            return redirect('order:cart_detail')

        # ایجاد سفارش
        order = Order.objects.create(
            user=request.user,
            address=address,
            postal_code=postal_code,
            receiver_name=receiver_name,
            receiver_phone_number=receiver_phone_number,
        )

        # افزودن آیتم‌ها
        for item in cart.items.all():
            try:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.price
                )
            except Exception as e:
                order.delete()  # اگر مشکلی پیش آمد، سفارش ناقص پاک شود
                messages.error(request, "خطایی هنگام ثبت آیتم‌ها رخ داد.")
                return redirect('order:cart_detail')

        cart.delete()  # سبد خرید پس از سفارش حذف شود
        messages.success(request, "سفارش با موفقیت ثبت شد.")
        return redirect('order:order_detail', order.id)
    


class OrderDetailView(LoginRequiredMixin, View):

    template_name = 'order/order_detail.html'

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:

        self.order = get_object_or_404(Order, id=kwargs['order_id'], user=request.user)

        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {'order': self.order})
    

class OrderPaymentView(LoginRequiredMixin, View):

    template_name = 'order/order_payment.html'

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'])
        context = {
            'order': order,
            'payment_settings': {
                'card_number': config.PAYMENT_CARD_NUMBER,
                'card_owner': config.PAYMENT_CARD_OWNER,
                'bank_name': config.PAYMENT_BANK_NAME,
            }
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs['order_id'])
        amount = order.get_total_price()
        payment_method = 'card'
        ref_id = request.POST.get('payment_ref')
        payment = Payment.objects.create(
            order=order,
            amount=amount,
            payment_method=payment_method,
            ref_id=ref_id,
        )
        messages.success(request, 'منتظر بمانید تا پرداخت توسط ادمین بررسی شود ، میتوانید از پروفایل وضعیت سفارش را مشاهده کنید')
        return redirect('order:order_detail', order.id)