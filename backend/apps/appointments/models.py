from django.db import models
from django.conf import settings
from datetime import date, time

class Appointment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    PURPOSE_CHOICES = (
        ('eye_exam', 'Eye Examination'),
        ('fitting', 'Glasses Fitting / Adjustment'),
        ('consultation', 'General Consultation'),
        ('pickup', 'Order Pickup'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='appointments', on_delete=models.CASCADE)
    
    # Guest info if needed, but let's stick to authenticated for now or optional
    full_name = models.CharField(max_length=150, help_text="Patient Name")
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    
    date = models.DateField()
    time = models.TimeField(help_text="Preferred Time")
    
    purpose = models.CharField(max_length=50, choices=PURPOSE_CHOICES, default='eye_exam')
    notes = models.TextField(blank=True, help_text="Any specific issues or requests?")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'time']
        
    def __str__(self):
        return f"{self.full_name} - {self.date} @ {self.time}"
