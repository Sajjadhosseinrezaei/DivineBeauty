from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem, Payment

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'price')
    readonly_fields = ('price',)

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 0
    fields = ('order', 'amount', 'payment_method', 'ref_id', 'status', 'paid_at', 'receipt', 'description')
    readonly_fields = ('order', 'amount', 'payment_method', 'ref_id', 'receipt')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline, PaymentInline]
    list_display = [
            'user',
            'is_paid',
            'address',
            'postal_code',
            'receiver_name',
            'receiver_phone_number',
        ]
    search_fields = ['tracking_code']
    
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 1 
    fields = ('product', 'quantity', 'price')
    readonly_fields = ('price',)


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = [
            'user',
        ]
    list_filter = ['user']
    search_fields = ['user__email']
    ordering = ['user']