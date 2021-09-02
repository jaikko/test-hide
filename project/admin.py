from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Staff

# Register your models here.


class CustomUserAdmin(UserAdmin):
    model = Staff
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('first_name', 'last_name', 'email', 'phone', 'mobile', 'team', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('first_name', 'last_name', 'email', 'phone', 'mobile', 'team', 'password1', 'password2', 'is_staff', 'is_active', 'is_superuser')})
    ),
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(Staff, CustomUserAdmin)
