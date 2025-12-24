from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import AppointmentForm
from .models import Appointment

@login_required
def appointment_create(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            # Auto-fill missing contact info if not provided, though form has them required in fields logic mostly
            # but model doesn't enforce email blank=True
            if not appointment.email:
                appointment.email = request.user.email
            appointment.save()
            messages.success(request, "Appointment request submitted successfully. We will confirm shortly.")
            return redirect('appointments:list')
    else:
        # Pre-fill
        initial = {
            'full_name': f"{request.user.first_name} {request.user.last_name}".strip(),
            'phone_number': request.user.phone_number,
            'email': request.user.email
        }
        form = AppointmentForm(initial=initial)
        
    return render(request, 'appointments/form.html', {'form': form})

@login_required
def appointment_list(request):
    appointments = request.user.appointments.all()
    return render(request, 'appointments/list.html', {'appointments': appointments})
