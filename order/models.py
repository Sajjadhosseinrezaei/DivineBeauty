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
    

    def get_total_price(self):
        