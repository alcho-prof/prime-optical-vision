from django.db import models
from django.conf import settings
from apps.core.models import TimeStampedModel
from apps.catalog.models import ProductVariant
from apps.lenses.models import LensType
from apps.prescriptions.models import Prescription


class Cart(TimeStampedModel):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )

    def __str__(self):
        return f"Cart for {self.user.username}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(TimeStampedModel):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product_variant = models.ForeignKey(
        ProductVariant,
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(default=1)
    
    # Optional lens and prescription
    lens = models.ForeignKey(
        LensType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cart_items'
    )
    prescription = models.ForeignKey(
        Prescription,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='cart_items'
    )

    class Meta:
        unique_together = ('cart', 'product_variant', 'lens', 'prescription')

    def __str__(self):
        return f"{self.quantity} x {self.product_variant} in {self.cart}"
    
    @property
    def total_price(self):
        """Calculate total price including lens"""
        from decimal import Decimal
        price = self.product_variant.product.price
        if self.lens:
            price += self.lens.price
        return price * self.quantity
