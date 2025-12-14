from django.db import models
from apps.core.models import TimeStampedModel
from apps.catalog.models import Product

class Inquiry(TimeStampedModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inquiries')
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    message = models.TextField(blank=True)

    def __str__(self):
        return f"{self.customer_name} - {self.product.name}"
