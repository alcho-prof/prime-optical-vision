from django.db import models
from apps.core.models import TimeStampedModel

class LensType(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, help_text="Additional cost for this lens type")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} (+₹{self.price})"
