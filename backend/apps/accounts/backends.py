from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

User = get_user_model()

class PasswordlessAuthBackend(ModelBackend):
    """
    Custom authentication backend that allows users with 
    'can_login_no_password=True' to login without a password check.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        
        try:
            # Try fetching by email (standard for this project) or username
            user = User.objects.get(Q(email=username) | Q(username=username))
        except User.DoesNotExist:
            return None
        
        # If user allows passwordless login, skip password check
        if user.can_login_no_password:
            return user
            
        # Otherwise, return None to let other backends (ModelBackend) handle password check
        return None
