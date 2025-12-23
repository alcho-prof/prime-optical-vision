from django import forms
from .models import Prescription

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = [
            'name', 'doctor_name', 'exam_date',
            'od_sphere', 'od_cylinder', 'od_axis', 'od_add',
            'os_sphere', 'os_cylinder', 'os_axis', 'os_add',
            'pd_single', 'pd_right', 'pd_left'
        ]
        widgets = {
            'exam_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. My Reading Glasses'}),
            'doctor_name': forms.TextInput(attrs={'class': 'form-control'}),
            # Add classes for grid layout in template
        }
