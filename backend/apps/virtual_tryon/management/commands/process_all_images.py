from django.core.management.base import BaseCommand
from apps.catalog.models import ProductVariant
from apps.virtual_tryon.models import SpectacleFrame
from apps.virtual_tryon.services import generate_3d_glass_model
from django.core.files.base import ContentFile
from django.db.models import Q
import os

class Command(BaseCommand):
    help = 'Process all product images in the database and convert them to 3D models for Virtual Try-On'

    def handle(self, *args, **options):
        self.stdout.write(self.style.HTTP_INFO("Starting batch processing of product images..."))

        # Find variants that have images
        variants = ProductVariant.objects.filter(image__isnull=False).exclude(image='')
        
        count = variants.count()
        self.stdout.write(f"Found {count} variants with images.")
        
        updated_count = 0
        failed_count = 0
        skipped_count = 0

        for variant in variants:
            try:
                # Check if frame exists
                frame, created = SpectacleFrame.objects.get_or_create(variant=variant)
                
                # If model already exists and is not empty, skip (unless --force is added, but let's keep it simple)
                # FORCE UPDATE: We want to apply the new curvature fix to all models.
                # if frame.model_file and os.path.exists(frame.model_file.path):
                #    skipped_count += 1
                #    continue
                
                self.stdout.write(f"Processing: {variant.product.name} ({variant.color_name})...")
                
                # Generate Model
                if not os.path.exists(variant.image.path):
                    self.stdout.write(self.style.WARNING(f"  Image file missing for {variant}"))
                    failed_count += 1
                    continue

                glb_file = generate_3d_glass_model(variant.image.path)
                
                if glb_file:
                    # Save
                    filename = f"generated_{variant.id}.glb"
                    # If file exists, delete it first to ensure clean save? Django handles unique names.
                    frame.model_file.save(filename, glb_file, save=True)
                    
                    # Set defaults if they are 0
                    if frame.scaling_factor == 1.0 and frame.offset_y == 0.0:
                        frame.scaling_factor = 1.0
                        frame.offset_y = 0.0 # Center
                        frame.save()
                        
                    self.stdout.write(self.style.SUCCESS(f"  Success! Model saved to {frame.model_file.name}"))
                    updated_count += 1
                else:
                    self.stdout.write(self.style.ERROR(f"  Failed to generate 3D model (algoritm returned None)"))
                    failed_count += 1

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"  Error processing {variant}: {e}"))
                failed_count += 1
        
        self.stdout.write(self.style.SUCCESS(f"\nBatch processing complete."))
        self.stdout.write(f"Updated: {updated_count}")
        self.stdout.write(f"Skipped (already exists): {skipped_count}")
        self.stdout.write(f"Failed: {failed_count}")
