from django.db import models
from django.contrib.auth import get_user_model
from apps.catalog.models import ProductVariant

User = get_user_model()


class TryOnSession(models.Model):
    """Store virtual try-on sessions for analytics and user history"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Try-On Session'
        verbose_name_plural = 'Try-On Sessions'
    
    def __str__(self):
        return f"Session {self.session_id} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"


class TryOnPhoto(models.Model):
    """Store user photos from try-on sessions"""
    session = models.ForeignKey(TryOnSession, on_delete=models.CASCADE, related_name='photos')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='tryon_photos/%Y/%m/%d/')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Try-On Photo'
        verbose_name_plural = 'Try-On Photos'
    
    def __str__(self):
        return f"Photo for {self.variant.product.name} - {self.created_at.strftime('%Y-%m-%d')}"


class FaceDetectionCache(models.Model):
    """Cache face detection data for performance"""
    session = models.ForeignKey(TryOnSession, on_delete=models.CASCADE)
    face_data = models.JSONField()  # Store face landmarks, positions, etc.
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Face Detection Cache'
        verbose_name_plural = 'Face Detection Caches'
    
    def __str__(self):
        return f"Face data for session {self.session.session_id}"


class SpectacleFrame(models.Model):
    """3D Model and metadata for a spectacle frame"""
    variant = models.OneToOneField(ProductVariant, on_delete=models.CASCADE, related_name='tryon_model')
    model_file = models.FileField(upload_to='frames_3d/', help_text="Upload .glb or .gltf file")
    
    # Geometric parameters for alignment
    scaling_factor = models.FloatField(default=1.0, help_text="Scale adjustment for the model")
    
    # Position offsets (in meters, approx) to align with face landmarks
    offset_x = models.FloatField(default=0.0)
    offset_y = models.FloatField(default=0.0)
    offset_z = models.FloatField(default=0.0)
    
    # Rotation adjustment if needed
    rotation_x = models.FloatField(default=0.0)
    rotation_y = models.FloatField(default=0.0)
    rotation_z = models.FloatField(default=0.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"3D Model for {self.variant}"
