from django.contrib import admin
from .models import FAQ, FAQCategory

# Register your models here.

from django.contrib import admin
from .models import FAQ, FAQCategory

class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1

@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    inlines = [FAQInline]

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'created_at', 'updated_at')
    list_filter = ('category',)
    search_fields = ('question', 'answer')

