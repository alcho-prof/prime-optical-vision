from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel

class Category(TimeStampedModel):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='subcategories'
    )
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products'
    )
    description = models.TextField()
    price_range = models.CharField(
        max_length=100, 
        help_text="e.g. '₹2000 - ₹5000' or 'Starting at ₹2000'"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProductVariant(TimeStampedModel):
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE, 
        related_name='variants'
    )
    color_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='products/variants/')
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} - {self.color_name}"
