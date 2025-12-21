from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    full_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}))

    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        # Handle Name splitting (simple logic)
        names = self.cleaned_data["full_name"].split(" ", 1)
        user.first_name = names[0]
        if len(names) > 1:
            user.last_name = names[1]
        
        # Set username to email (since we treat email as primary identity)
        user.username = user.email
        
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request, *args, **kwargs)
        # Make password optional in field validation
        self.fields['password'].required = False


from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate

class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={"autofocus": True}))

    def clean(self):
        email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if email and password:
            self.user_cache = authenticate(self.request, username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(self.error_messages.get("invalid_login"), code="invalid_login")
        return self.cleaned_data


