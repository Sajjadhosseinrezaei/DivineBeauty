from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Product, Brand, ProductLabel, Category, ProductImage

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'discount_price', 'brand', 'stock', 'is_available', 'created_at')
    list_filter = ('is_available', 'brand', 'category', 'skintype')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_available', 'stock')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('lable',)

    fieldsets = (
        (None, {'fields': ('name', 'slug', 'description', 'main_image')}),
        ('قیمت‌گذاری', {'fields': ('price', 'discount_price')}),
        ('اطلاعات بیشتر', {'fields': ('skintype', 'expiration_date', 'usage_instructions')}),
        ('دسته‌بندی و برند', {'fields': ('category', 'brand', 'lable')}),
        ('موجودی و وضعیت', {'fields': ('stock', 'is_available')}),
        ('تاریخ‌ها', {'fields': ('created_at', 'updated_at')}),
    )
    
@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(ProductLabel)
class ProductLabelAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Category)
class CategoryAdmin(DraggableMPTTAdmin):
    mptt_indent_field = "name"
    list_display = ('tree_actions', 'indented_title', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'image')

