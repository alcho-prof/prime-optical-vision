from django import forms
from .models import Appointment
from django.utils import timezone

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['full_name', 'phone_number', 'email', 'date', 'time', 'purpose', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'min': timezone.now().date().isoformat()}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }
    
    def clean_date(self):
        date_obj = self.cleaned_data.get('date')
        if date_obj and date_obj < timezone.now().date():
            raise forms.ValidationError("Date needs to be in the future.")
        return date_obj
