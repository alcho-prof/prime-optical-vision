from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, UserProfileForm
import random
import json
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from apps.users.models import PhoneVerification
from django.conf import settings

User = get_user_model()

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f"Welcome, {user.first_name}!")
            return redirect('home')
        else:
            messages.error(request, "Registration failed. Please correct the errors below.")
    else:
        form = UserRegistrationForm()
        
    return render(request, 'accounts/register.html', {'form': form})

@login_required
def profile_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=user)
        
    return render(request, 'accounts/profile.html', {'form': form})


from .utils import send_otp_sms

@require_POST
def request_otp(request):
    """Generate and send OTP for phone number"""
    try:
        data = json.loads(request.body)
        phone = data.get('phone')
        
        if not phone:
            return JsonResponse({'status': 'error', 'message': 'Phone number required'}, status=400)

        # Generate 6 digit OTP
        otp = str(random.randint(100000, 999999))
        
        # Save to DB
        PhoneVerification.objects.create(phone_number=phone, code=otp)
        
        # Send SMS (Real or Mock based on env)
        sent = send_otp_sms(phone, otp)
        
        if sent:
            msg = 'OTP sent successfully'
            # For dev convenience, still hint
            if settings.DEBUG:
                 print(f"DEBUG OTP: {otp}")
        else:
             print("Failed to send OTP via Provider")
        
        return JsonResponse({'status': 'success', 'message': 'OTP sent successfully'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@require_POST
def verify_otp(request):
    """Verify OTP and login/create user"""
    try:
        data = json.loads(request.body)
        phone = data.get('phone')
        otp = data.get('otp')
        
        if not phone or not otp:
            return JsonResponse({'status': 'error', 'message': 'Phone and OTP required'}, status=400)
            
        # Verify OTP
        verification = PhoneVerification.objects.filter(
            phone_number=phone, 
            code=otp,
            is_verified=False
        ).order_by('-created_at').first()
        
        if not verification or not verification.is_valid():
            return JsonResponse({'status': 'error', 'message': 'Invalid or expired OTP'}, status=400)
            
        # Mark used
        verification.is_verified = True
        verification.save()
        
        # Check if user exists
        user_qs = User.objects.filter(phone_number=phone)
        
        if user_qs.exists():
            # Login existing user
            user = user_qs.first()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return JsonResponse({'status': 'success', 'redirect_url': '/'})
        else:
            # Create new user
            # Use phone as username/email placeholder
            username = phone
            email = f"{phone}@example.com" # Temporary email
            
            # Ensure uniqueness
            if User.objects.filter(username=username).exists():
                 username = f"{phone}_{random.randint(1000,9999)}"
            
            user = User.objects.create_user(username=username, email=email, phone_number=phone)
            user.set_unusable_password()
            user.is_verified = True
            user.save()
            
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return JsonResponse({'status': 'success', 'redirect_url': '/'})
            
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
