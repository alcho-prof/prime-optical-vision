import os
import random
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files import File
from apps.catalog.models import Product, ProductVariant, Category, Brand

class Command(BaseCommand):
    help = 'Imports optical products from "optical project image" folder'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting Optical Products Import...'))

        # Define Source Directory
        # "optical project image" is in the root of the repo (parent of backend)
        # settings.BASE_DIR is backend.
        source_dir = settings.BASE_DIR.parent / 'optical project image'
        
        if not source_dir.exists():
            self.stdout.write(self.style.ERROR(f'Source directory not found: {source_dir}'))
            return

        # 1. Setup Categories
        self.setup_categories()
        
        # 2. Setup Brands
        self.setup_brands()

        # 3. Process Folders
        self.process_folders(source_dir)

        self.stdout.write(self.style.SUCCESS('Import Complete!'))

    def setup_categories(self):
        """Create standard optical categories"""
        self.categories = {}
        
        # Main Categories
        eyeglasses, _ = Category.objects.get_or_create(name="Eyeglasses", defaults={'slug': 'eyeglasses'})
        sunglasses, _ = Category.objects.get_or_create(name="Sunglasses", defaults={'slug': 'sunglasses'})
        computer, _ = Category.objects.get_or_create(name="Computer Glasses", defaults={'slug': 'computer-glasses'})
        
        # Subcategories
        self.categories['men_gl'] = Category.objects.get_or_create(name="Men", parent=eyeglasses, defaults={'slug': 'men-eyeglasses'})[0]
        self.categories['women_gl'] = Category.objects.get_or_create(name="Women", parent=eyeglasses, defaults={'slug': 'women-eyeglasses'})[0]
        self.categories['kids_gl'] = Category.objects.get_or_create(name="Kids", parent=eyeglasses, defaults={'slug': 'kids-eyeglasses'})[0]
        self.categories['unisex_gl'] = Category.objects.get_or_create(name="Unisex", parent=eyeglasses, defaults={'slug': 'unisex-eyeglasses'})[0]
        
        self.categories['men_sun'] = Category.objects.get_or_create(name="Men", parent=sunglasses, defaults={'slug': 'men-sunglasses'})[0]
        self.categories['women_sun'] = Category.objects.get_or_create(name="Women", parent=sunglasses, defaults={'slug': 'women-sunglasses'})[0]
        
        self.stdout.write(f"Categories setup: {[c.name for c in self.categories.values()]}")

    def setup_brands(self):
        brand_names = ['Prime', 'Ray-Ban', 'Oakley', 'Vogue', 'Titan', 'Fastrack']
        self.brands = []
        for name in brand_names:
            brand, _ = Brand.objects.get_or_create(name=name)
            self.brands.append(brand)

    def process_folders(self, source_dir):
        # Iterate over numeric folders
        folders = [f for f in source_dir.iterdir() if f.is_dir() and f.name.isdigit()]
        folders.sort(key=lambda x: int(x.name))

        self.stdout.write(f"Found {len(folders)} product folders.")

        colors = ['Black', 'Gunmetal', 'Gold', 'Silver', 'Tortoise', 'Blue', 'Brown', 'Transparent']
        shapes = ['Rectangular', 'Round', 'Aviator', 'Wayfarer', 'Cat Eye', 'Square']
        materials = ['Acetate', 'Metal', 'Titanium', 'TR90', 'Mixed']

        for folder in folders:
            folder_id = folder.name
            
            # Smart Name Generation
            shape = random.choice(shapes)
            material = random.choice(materials)
            brand = random.choice(self.brands)
            product_name = f"{brand.name} {shape} {folder_id}"
            
            # Determine Category Randomly
            category_key = random.choice(list(self.categories.keys()))
            category = self.categories[category_key]
            
            # Determine Gender from category key
            gender = 'Unisex'
            if 'men' in category_key: gender = 'Men'
            if 'women' in category_key: gender = 'Women'
            if 'kids' in category_key: gender = 'Kids'

            price = random.choice([999, 1499, 1999, 2499, 2999, 3499, 4999])
            
            self.stdout.write(f"Processing Folder {folder_id} -> {product_name} ({category.name})")

            # Create/Update Product
            product, created = Product.objects.get_or_create(
                name=product_name,
                defaults={
                    'category': category,
                    'brand': brand,
                    'description': f"Premium {material} {shape.lower()} frame. Lightweight and durable design suitable for daily wear. Features high-quality hinges and comfortable nose pads.",
                    'price': price,
                    'gender': gender,
                    'frame_shape': shape,
                    'frame_material': material,
                    'stock': 50,
                    'weight': random.randint(15, 30),
                    'lens_width': random.choice([50, 52, 54]),
                    'bridge_width': random.choice([16, 18, 20]),
                    'temple_length': random.choice([135, 140, 145]),
                    'is_active': True
                }
            )

            # Process Images (Variants)
            # Filter distinct images
            images = [f for f in folder.iterdir() if f.is_file() and f.suffix.lower() in ['.jpg', '.jpeg', '.png', '.webp']]
            images.sort()

            # Create Variants for each image
            # We assume each image is a different color variant for variety
            used_colors = []
            
            for idx, img_path in enumerate(images):
                # Pick a unique color for this variant
                available_colors = [c for c in colors if c not in used_colors]
                if not available_colors:
                    color = f"Color {idx+1}"
                else:
                    color = random.choice(available_colors)
                    used_colors.append(color)

                variant_identifier = f"{product.name} - {color}"
                
                # Check if variant exists to avoid dupes
                if ProductVariant.objects.filter(product=product, color_name=color).exists():
                    continue

                self.stdout.write(f"  - Adding Variant: {color} ({img_path.name})")
                
                variant = ProductVariant(
                    product=product,
                    color_name=color,
                    in_stock=True
                )
                
                # Save image
                with open(img_path, 'rb') as f:
                    variant.image.save(f"{folder_id}_{color}_{img_path.name}", File(f), save=True)
                
                variant.save()
