"""
Cart signals for handling cart sync on login
"""

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .hybrid_cart import HybridCart


@receiver(user_logged_in)
def sync_cart_on_login(sender, request, user, **kwargs):
    """
    Sync session cart to database cart when user logs in.
    This preserves items added while anonymous.
    """
    if request:
        # Ensure user is attached to request (needed for HybridCart)
        request.user = user
        cart = HybridCart(request)
        cart.sync_session_to_db()
