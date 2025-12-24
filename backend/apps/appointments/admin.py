from django.contrib import admin
from .models import Appointment

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'date', 'time', 'purpose', 'status', 'created_at')
    list_filter = ('status', 'date', 'purpose')
    search_fields = ('full_name', 'phone_number', 'email')
    list_editable = ('status',)
