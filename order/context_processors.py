# your_app/context_processors.py
from .models import Cart, CartItem

def cart_context(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all().order_by('created')
            total_items = sum(item.quantity for item in cart_items)
            total_price = cart.get_total_price()  # فرض بر این است که متد get_total_price در مدل Cart تعریف شده است
        except Cart.DoesNotExist:
            cart = None
            cart_items = []
            total_items = 0
            total_price = 0
    else:
        cart = None
        cart_items = []
        total_items = 0
        total_price = 0

    return {
        'cart': cart,
        'cart_items': cart_items,
        'total_cart_items': total_items,
        'total_cart_price': total_price,
    }