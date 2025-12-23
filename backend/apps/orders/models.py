from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.catalog.models import ProductVariant
from apps.lenses.models import LensType

class Order(TimeStampedModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    # User info (Optional for Guest)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Shipping Details
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    address_line_1 = models.CharField(max_length=250)
    address_line_2 = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    
    # Order Info
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, default='COD')
    
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Order #{self.id} - {self.full_name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product_variant = models.ForeignKey(ProductVariant, related_name='order_items', on_delete=models.CASCADE)
    lens_type = models.ForeignKey(LensType, related_name='order_items', on_delete=models.SET_NULL, null=True, blank=True)
    
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Unit price at time of purchase")
    
    def __str__(self):
        return f"{self.quantity}x {self.product_variant.product.name} ({self.order.id})"

    def get_total_price(self):
        return self.price * self.quantity
