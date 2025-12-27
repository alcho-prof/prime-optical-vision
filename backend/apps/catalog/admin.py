from django.contrib import admin
from .models import Category, Product, ProductVariant, Brand, ProductImage


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ('is_active',)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text', 'is_primary', 'order')


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'category', 'price', 'stock', 'gender', 'is_active', 'is_featured', 'updated_at')
    list_filter = ('is_active', 'is_featured', 'is_new_arrival', 'is_bestseller', 'category', 'brand', 'gender', 'frame_material')
    search_fields = ('name', 'description', 'brand__name')
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariantInline]
    list_editable = ('is_active', 'is_featured', 'stock')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'brand', 'category', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'price_range')
        }),
        ('Eyewear Specifications', {
            'fields': ('gender', 'frame_material', 'frame_shape', 'frame_color', 
                      'lens_material', 'lens_color', 'weight')
        }),
        ('Dimensions', {
            'fields': ('lens_width', 'bridge_width', 'temple_length'),
            'classes': ('collapse',)
        }),
        ('Stock & Status', {
            'fields': ('stock', 'is_active', 'is_featured', 'is_new_arrival', 'is_bestseller')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'is_primary', 'order', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('product__name', 'alt_text')
    list_editable = ('is_primary', 'order')
