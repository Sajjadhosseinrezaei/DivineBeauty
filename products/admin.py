from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from .models import Product, Brand, ProductLabel, Category, ProductImage
from django_json_widget.widgets import JSONEditorWidget
from django import forms

class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'attributes': JSONEditorWidget(
                options={
                    'mode': 'tree',    # حالت گرافیکی درختی
                    'modes': ['tree', 'code'],  # اجازه تغییر بین درخت و کد
                }
            )
        }

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm

    list_display = ('name','main_image', 'price', 'discount_price', 'brand', 'stock', 'is_available', 'created_at')
    list_filter = ('is_available', 'brand', 'category', 'skintype')
    search_fields = ('name', 'description')
    list_editable = ('is_available', 'stock')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('label',)

    fieldsets = (
        (None, {'fields': ('name','description', 'main_image')}),
        ('قیمت‌گذاری', {'fields': ('price', 'discount_price')}),
        ('اطلاعات بیشتر', {'fields': ('skintype', 'expiration_date', 'usage_instructions')}),
        ('دسته‌بندی و برند', {'fields': ('category', 'brand', 'label')}),
        ('موجودی و وضعیت', {'fields': ('stock', 'is_available')}),
        ('تاریخ‌ها', {'fields': ('created_at', 'updated_at')}),
        ('ویژگی های اضافه', {'fields':('attributes',)})
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

