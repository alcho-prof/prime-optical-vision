from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Prescription
from .forms import PrescriptionForm

@login_required
def prescription_list(request):
    prescriptions = request.user.prescriptions.all()
    return render(request, 'prescriptions/list.html', {'prescriptions': prescriptions})

@login_required
def prescription_create(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.user = request.user
            prescription.save()
            messages.success(request, "Prescription added successfully.")
            return redirect('prescriptions:list')
    else:
        form = PrescriptionForm()
    return render(request, 'prescriptions/form.html', {'form': form, 'title': 'Add Prescription'})

@login_required
def prescription_edit(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk, user=request.user)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            form.save()
            messages.success(request, "Prescription updated successfully.")
            return redirect('prescriptions:list')
    else:
        form = PrescriptionForm(instance=prescription)
    return render(request, 'prescriptions/form.html', {'form': form, 'title': 'Edit Prescription'})

@login_required
def prescription_delete(request, pk):
    prescription = get_object_or_404(Prescription, pk=pk, user=request.user)
    if request.method == 'POST':
        prescription.delete()
        messages.success(request, "Prescription deleted.")
        return redirect('prescriptions:list')
    return render(request, 'prescriptions/confirm_delete.html', {'prescription': prescription})
