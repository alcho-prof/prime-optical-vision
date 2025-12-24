from django import template
from django.utils import timezone
from django.db.models import Sum, Count, Q
from apps.orders.models import Order
from apps.appointments.models import Appointment
from apps.catalog.models import Product
from django.contrib.auth import get_user_model

register = template.Library()

@register.inclusion_tag('admin/dashboard_stats.html')
def render_dashboard_stats():
    today = timezone.now().date()
    User = get_user_model()
    
    # 1. Total confirmed sales (completed/confirmed orders)
    # Assuming 'confirmed', 'shipped', 'delivered' count as sales. 'pending' might not unless paid?
    # Let's count 'confirmed' and above.
    sales_qs = Order.objects.filter(status__in=['confirmed', 'shipped', 'delivered'])
    total_sales = sales_qs.aggregate(Sum('total_amount'))['total_amount__sum'] or 0
    
    # 2. Orders Count (All time)
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    
    # 3. Today's Appointments
    today_appointments = Appointment.objects.filter(date=today).count()
    pending_appointments = Appointment.objects.filter(status='pending').count()
    
    # 4. Product Stats
    active_products = Product.objects.filter(is_active=True).count()
    low_stock_count = 0 # Placeholder if we had inventory tracking
    
    # 5. Customers
    total_customers = User.objects.count()

    return {
        'total_sales': total_sales,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'today_appointments': today_appointments,
        'pending_appointments': pending_appointments,
        'active_products': active_products,
        'total_customers': total_customers,
    }
