from django.db import models
from accounts.models import CustomUser
from products.models import Product
from django.core.validators import MinValueValidator, RegexValidator

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='orders', verbose_name="کاربر")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="زمان ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="زمان به‌روزرسانی")
    is_paid = models.BooleanField(default=False)
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{10}$', 'کد پستی باید ۱۰ رفم باشد')])
    phone_number = models.CharField(max_length=15, validators=[RegexValidator(r'^\d{11}$', 'شماره تلفن باید ۱۱ رقم باشد')])

    def __str__(self):
        return f'Order {self.id} by {self.user.email}'
    
    def get_total_price(self):
        total = sum(item.cost() for item in self.items.all())
        return total

    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=12, decimal_places=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.quantity} of {self.product.name} in Order {self.order.id}'

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.get_final_price()
        return super().save(*args, **kwargs)
    

    def cost(self):
        return self.price * self.quantity
    


from django.db import models
from accounts.models import CustomUser


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='carts', verbose_name='سبد خرید')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد') 
    updated_at = models.DateTimeField(auto_now=True, verbose_name='زمان به‌روزرسانی')    

    def __str__(self):
        return f'Cart {self.id} for {self.user.email}'
    
    def get_total_price(self):
        total = sum(item.cost() for item in self.items.all())
        return total
    
    def add_to_cart(self, product, quantity=1):
        cart_item , created = CartItem.objects.get_or_create(cart=self, product=product)
        if created:
            cart_item.price = product.get_final_price()
            cart_item.quantity = quantity
            
        else:
            cart_item.quantity += quantity
            cart_item.price = product.get_final_price()
        cart_item.save()
    
    def remove_empty_cart(self):
        if not self.items.exists():
            self.delete()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', verbose_name='آیتم سبد خرید')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, verbose_name='محصول')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    price = models.DecimalField(max_digits=12, decimal_places=0, verbose_name='قیمت')  # قیمت محصول در زمان اضافه شدن به سبد خرید
    
    def __str__(self):
        return f'{self.quantity} of {self.product.name} in Cart {self.cart.id}'
    
    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = self.product.get_final_price()
        return super().save(*args, **kwargs)
    
    def cost(self):
        return self.price * self.quantity
    
    def update_cart_quantity(self, quantity):
        if quantity < 1:
            raise ValueError("تعداد نمی‌تواند کمتر از 1 باشد")
        if quantity <= self.product.stock:
            self.quantity = quantity
            self.save()
        else:
            raise ValueError("تعداد درخواستی بیشتر از موجودی است")

    def del_cart_item(self):
        self.delete()