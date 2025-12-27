from django.db import models
from django.utils.text import slugify
from apps.core.models import TimeStampedModel


class Brand(TimeStampedModel):
    """Brand model for eyewear manufacturers"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='brands/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            
            while Brand.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


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
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            
            # Check if slug exists and add number suffix if needed
            while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(TimeStampedModel):
    """Product model for eyewear items"""
    GENDER_CHOICES = [
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Unisex', 'Unisex'),
        ('Kids', 'Kids'),
    ]
    
    FRAME_MATERIAL_CHOICES = [
        ('Acetate', 'Acetate'),
        ('Metal', 'Metal'),
        ('Titanium', 'Titanium'),
        ('TR90', 'TR90'),
        ('Stainless Steel', 'Stainless Steel'),
        ('Plastic', 'Plastic'),
        ('Wood', 'Wood'),
        ('Mixed', 'Mixed Materials'),
    ]
    
    LENS_MATERIAL_CHOICES = [
        ('CR-39', 'CR-39 Plastic'),
        ('Polycarbonate', 'Polycarbonate'),
        ('Trivex', 'Trivex'),
        ('High-Index', 'High-Index Plastic'),
        ('Glass', 'Glass'),
    ]
    
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products'
    )
    brand = models.ForeignKey(
        Brand,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_range = models.CharField(
        max_length=100, 
        blank=True,
        help_text="e.g. '₹2000 - ₹5000' or 'Starting at ₹2000'"
    )
    
    # Eyewear specific fields
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Unisex')
    frame_material = models.CharField(max_length=50, choices=FRAME_MATERIAL_CHOICES, blank=True)
    frame_shape = models.CharField(max_length=50, blank=True, help_text="e.g., Round, Square, Aviator")
    frame_color = models.CharField(max_length=50, blank=True)
    lens_material = models.CharField(max_length=50, choices=LENS_MATERIAL_CHOICES, blank=True)
    lens_color = models.CharField(max_length=50, blank=True)
    weight = models.IntegerField(null=True, blank=True, help_text="Weight in grams")
    
    # Dimensions
    lens_width = models.IntegerField(null=True, blank=True, help_text="Lens width in mm")
    bridge_width = models.IntegerField(null=True, blank=True, help_text="Bridge width in mm")
    temple_length = models.IntegerField(null=True, blank=True, help_text="Temple length in mm")
    
    # Stock and status
    stock = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_new_arrival = models.BooleanField(default=False)
    is_bestseller = models.BooleanField(default=False)
    
    # SEO fields
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['brand', 'is_active']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            
            # Check if slug exists and add number suffix if needed
            while Product.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            self.slug = slug
        
        # Auto-generate price_range if not set
        if not self.price_range and self.price:
            self.price_range = f"₹{int(self.price)}"
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    @property
    def in_stock(self):
        """Check if product is in stock"""
        return self.stock > 0
    
    @property
    def main_image(self):
        """Get the main product image"""
        return self.images.filter(is_primary=True).first() or self.images.first()


class ProductImage(TimeStampedModel):
    """Product images model"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=200, blank=True)
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', '-is_primary']
    
    def save(self, *args, **kwargs):
        # If this is set as primary, unset other primary images
        if self.is_primary:
            ProductImage.objects.filter(
                product=self.product,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.product.name} - Image {self.order}"


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
