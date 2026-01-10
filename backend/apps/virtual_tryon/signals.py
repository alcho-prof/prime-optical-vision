from django.db.models.signals import post_save
from django.dispatch import receiver
from apps.catalog.models import ProductVariant
from apps.virtual_tryon.models import SpectacleFrame
from .services import generate_3d_glass_model
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=ProductVariant)
def auto_generate_3d_model(sender, instance, created, **kwargs):
    """
    Automatically generates a 3D model for Virtual Try-On when a ProductVariant 
    is created or updated with an image.
    """
    # Check if image exists
    if not instance.image:
        return

    # Check if SpectacleFrame already exists for this variant
    # We might want to update it if the image changed, but for now let's just create if missing
    # or if it has no model file.
    spectacle_frame, frame_created = SpectacleFrame.objects.get_or_create(variant=instance)
    
    # If the frame already has a 'real' 3D model uploaded by admin, don't overwrite it automatically?
    # Or if the user asked "convert every uploaded", maybe we overwrite.
    # Let's overwrite only if it's empty or checks a flag. 
    # For now, let's logic: if created or model_file is empty, generate it.
    
    if not spectacle_frame.model_file or frame_created:
        try:
            logger.info(f"Generating 3D model for {instance.product.name}...")
            # Generate GLB
            glb_file = generate_3d_glass_model(instance.image.path)
            
            if glb_file:
                # Save to model_file
                filename = f"generated_{instance.id}.glb"
                spectacle_frame.model_file.save(filename, glb_file, save=True)
                
                # Set default metadata
                spectacle_frame.scaling_factor = 1.0
                spectacle_frame.offset_y = 0.0 # Adjust based on testing
                spectacle_frame.save()
                logger.info(f"Successfully generated 3D model: {filename}")
            else:
                logger.warning(f"Failed to generate 3D model for {instance.product.name}")
                
        except Exception as e:
            logger.error(f"Error in auto_generate_3d_model: {e}")
