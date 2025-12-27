from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import datetime

class User(AbstractUser):
    """
    Custom User model for Prime Optical.
    Extends AbstractUser to keep standard Django auth features (username, password, permissions).
    Adds phone number and verification status.
    """
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text="Contact phone number")
    is_verified = models.BooleanField(default=False, help_text="Email/Phone verification status")
    can_login_no_password = models.BooleanField(default=False, help_text="Allow login without password (username/email only)")
    
    # Optional: If you want to login with email instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class PhoneVerification(models.Model):
    """Store OTP codes for phone verification"""
    phone_number = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False) # Marked True once verified (optional usage)

    def is_valid(self):
        """Check if OTP is within 5 minutes expiry"""
        return self.created_at >= timezone.now() - datetime.timedelta(minutes=5)

    def __str__(self):
        return f"{self.phone_number} - {self.code}"
