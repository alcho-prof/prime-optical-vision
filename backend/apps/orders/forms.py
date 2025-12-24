from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    PAYMENT_CHOICES = (
        ('COD', 'Cash on Delivery (COD)'),
        ('online', 'Online Payment (Razorpay)'),
    )
    
    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'payment-method-radio'}),
        initial='COD',
        label='Payment Method'
    )
    
    class Meta:
        model = Order
        fields = ['full_name', 'email', 'phone_number', 'address_line_1', 'address_line_2', 'city', 'postal_code', 'payment_method']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'address_line_1': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 1'}),
            'address_line_2': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address Line 2 (Optional)'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Postal Code'}),
        }

