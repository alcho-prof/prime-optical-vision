from django.contrib import admin
from .models import Inquiry

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('created_at', 'customer_name', 'phone_number', 'product')
    list_filter = ('created_at',)
    search_fields = ('customer_name', 'phone_number', 'product__name')
    readonly_fields = ('created_at', 'updated_at', 'product', 'customer_name', 'phone_number', 'message')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
