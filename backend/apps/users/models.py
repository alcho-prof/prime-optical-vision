from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    """
    Custom User model for Prime Optical.
    Extends AbstractUser to keep standard Django auth features (username, password, permissions).
    Adds phone number and verification status.
    """
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text="Contact phone number")
    is_verified = models.BooleanField(default=False, help_text="Email/Phone verification status")
    
    # Optional: If you want to login with email instead of username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
