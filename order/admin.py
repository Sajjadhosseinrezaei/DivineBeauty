from django.contrib import admin
from .models import Order, OrderItem, Cart, CartItem

# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1 
    fields = ('product', 'quantity', 'price')
    readonly_fields = ('price',)



@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    list_display = [
            'user',
            'is_paid',
            'address',
            'postal_code',
            'phone_number',
        ]
    
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