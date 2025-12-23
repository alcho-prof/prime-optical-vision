from django.contrib import admin
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product_variant', 'lens_type', 'quantity', 'price', 'get_total_price']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'full_name', 'email', 'city', 'total_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['id', 'full_name', 'email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at', 'total_amount']
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('status', 'total_amount', 'user', 'created_at')
        }),
        ('Customer Details', {
            'fields': ('full_name', 'email', 'phone_number')
        }),
        ('Shipping Address', {
            'fields': ('address_line_1', 'address_line_2', 'city', 'postal_code')
        }),
    )
    
    actions = ['mark_as_shipped', 'mark_as_delivered']
    
    def mark_as_shipped(self, request, queryset):
        queryset.update(status='shipped')
    mark_as_shipped.short_description = "Mark selected orders as Shipped"

    def mark_as_delivered(self, request, queryset):
        queryset.update(status='delivered')
    mark_as_delivered.short_description = "Mark selected orders as Delivered"
