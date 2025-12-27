from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from allauth.account.models import EmailAddress

User = get_user_model()

@receiver(post_save, sender=User)
def create_email_address(sender, instance, created, **kwargs):
    """
    Automatically create an Allauth EmailAddress when a User is created or updated.
    This ensures admin-created users or OTP users get an entry in account_emailaddress.
    """
    if instance.email:
        # Check if this email already exists for this user
        email_address, created_email = EmailAddress.objects.get_or_create(
            user=instance,
            email=instance.email,
            defaults={
                'verified': instance.is_verified if hasattr(instance, 'is_verified') else False,
                'primary': True # Assume primary if explicitly invoking save/create
            }
        )
        
        # If it wasn't created, but we want to ensure it is primary/verified if user is
        if not created_email:
            if hasattr(instance, 'is_verified') and instance.is_verified and not email_address.verified:
                email_address.verified = True
                email_address.save()
