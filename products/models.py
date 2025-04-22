from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from utility import AutoSlugField

class Brand(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام برند")

    def __str__(self):
        return self.name
    
class SkinType(models.TextChoices):
    NORMAL = 'normal', 'نرمال'
    OILY = 'oily', 'چرب'
    DRY = 'dry', 'خشک'
    COMBINATION = 'combination', 'مختلط'
    SENSITIVE = 'sensitive', 'حساس'

class ProductLabel(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام برچسب")
    slug = AutoSlugField(max_length=200,unique=True, verbose_name="نامک", blank=True, null=True)

    def __str__(self):
        return self.name
    


class Category(MPTTModel):
    
    name = models.CharField(max_length=200, verbose_name="نام دسته‌بندی")
    slug = AutoSlugField(max_length=200,unique=True, verbose_name="نامک", blank=True, null=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name="دسته‌بندی والد")

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    slug = AutoSlugField(max_length=200, unique=True, verbose_name="نامک", blank=True, null=True)
    description = models.TextField(blank=True, null=True, verbose_name="توضیحات محصول")
    main_image = models.ImageField(upload_to='products/main/', blank=True, null=True, verbose_name="تصویر اصلی")
    price = models.IntegerField(verbose_name="قیمت")
    skintype = models.CharField(max_length=20, choices=SkinType.choices, verbose_name="نوع پوست", blank=True, null=True)
    discount_price = models.IntegerField(blank=True, null=True, verbose_name="قیمت تخفیف‌خورده")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="دسته‌بندی")
    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی انبار")
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, verbose_name="برند", blank=True)
    label = models.ManyToManyField(ProductLabel, blank=True, verbose_name="برچسب")
    is_available = models.BooleanField(default=True, verbose_name="موجود")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاریخ بروزرسانی")
    expiration_date = models.DateField(blank=True, null=True, verbose_name="تاریخ انقضا")  # برای محصولات با تاریخ انقضا
    usage_instructions = models.TextField(blank=True, null=True, verbose_name="دستورالعمل مصرف")
    attributes = models.JSONField(blank=True, null=True, verbose_name="ویژگی‌ها")  # برای ویژگی‌های اضافی
    
    def __str__(self):
        return self.name

    def get_final_price(self):
        return self.discount_price if self.discount_price else self.price
    
    def get_discount_percentage(self):
        if self.discount_price:
            return round((self.price - self.discount_price) / self.price * 100)
        return 0



class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images', verbose_name="محصول")
    image = models.ImageField(upload_to='products/', verbose_name="تصویر")

    def __str__(self):
        return self.product.name
    

