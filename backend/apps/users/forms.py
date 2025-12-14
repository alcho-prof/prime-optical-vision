from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(forms.ModelForm):
    # Explicitly define fields to control order and widget
    email = forms.EmailField(required=True, help_text='Required. Must be unique.')
    username = forms.CharField(required=True, help_text='Required. unique username.')
    password = forms.CharField(widget=forms.PasswordInput, required=False)
    password_2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('email', 'username', 'can_login_no_password', 'phone_number', 'is_verified')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Check uniqueness case-insensitive
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError(
                "❌ Error: This email is already registered.\n"
                "👉 Fix: Please use a unique email address, or go back to the User List to find and edit the existing user."
            )
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_2 = cleaned_data.get("password_2")
        can_login_no_password = cleaned_data.get("can_login_no_password")

        if not can_login_no_password:
            # If standard login, enforce password presence
            if not password:
                 self.add_error('password', "Password is required unless 'Login without password' is checked.")
            if not password_2:
                 self.add_error('password_2', "Confirm Password is required.")
            
            # If both present, check match
            if password and password_2 and password != password_2:
                self.add_error('password_2', "Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
            
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'can_login_no_password')
