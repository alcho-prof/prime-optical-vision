from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

class Prescription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='prescriptions')
    name = models.CharField(max_length=100, help_text="e.g., 'My Primary Glasses'")
    doctor_name = models.CharField(max_length=100, blank=True)
    exam_date = models.DateField(null=True, blank=True)
    
    # Right Eye (OD)
    od_sphere = models.DecimalField(max_digits=4, decimal_places=2, help_text="Sphere (SPH)")
    od_cylinder = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="Cylinder (CYL)")
    od_axis = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(180)])
    od_add = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="Addition (ADD)")
    
    # Left Eye (OS)
    os_sphere = models.DecimalField(max_digits=4, decimal_places=2, help_text="Sphere (SPH)")
    os_cylinder = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="Cylinder (CYL)")
    os_axis = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0), MaxValueValidator(180)])
    os_add = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True, help_text="Addition (ADD)")
    
    # PD (Pupillary Distance)
    pd_single = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="Single PD (e.g. 62.0)")
    pd_right = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="Right PD (Mono)")
    pd_left = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, help_text="Left PD (Mono)")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} - {self.user.email}"
