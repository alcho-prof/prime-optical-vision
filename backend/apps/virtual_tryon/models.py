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
