from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Must be unique.')

    class Meta:
        model = User
        fields = ('email', 'username')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "❌ Error: This email is already registered.\n"
                "👉 Fix: Please use a unique email address, or go back to the User List to find and edit the existing user."
            )
        return email

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username')
