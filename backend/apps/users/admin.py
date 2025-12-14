from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'phone_number', 'is_staff', 'is_verified')
    list_filter = ('is_staff', 'is_superuser', 'is_verified', 'groups')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('email',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('phone_number', 'is_verified')}),
    )
