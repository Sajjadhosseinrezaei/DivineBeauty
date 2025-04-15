from django.contrib import admin
from .models import CustomUser, UserProfile

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'date_of_birth', 'last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    readonly_fields = ('last_login', 'date_joined')


     # ✅ حذف is_superuser برای کاربران غیر سوپریوزر
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if 'is_superuser' in form.base_fields:
                form.base_fields.pop('is_superuser')
        return form

    

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'profile_picture', 'bio', 'location', 'website')
    search_fields = ('user__email', 'bio', 'location')
    ordering = ('user',)
    fieldsets = (
        (None, {'fields': ('user', 'profile_picture')}),
        ('Additional info', {'fields': ('bio', 'location', 'website')}),
    )