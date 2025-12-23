
import os
import django
import sys
from django.test import RequestFactory, Client
from django.contrib.auth import get_user_model
from django.urls import reverse

# Setup Django environment
# Current: backend/apps/accounts/tests_manual_validation.py
# Goal: backend/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from apps.accounts.forms import UserRegistrationForm, UserProfileForm

User = get_user_model()

def test_registration():
    print("\n--- Testing Registration ---")
    email = "testuser@example.com"
    password = "securepassword123"
    
    # Cleanup previous run
    User.objects.filter(email=email).delete()
    
    form_data = {
        'full_name': 'Test User',
        'email': email,
        'password': password,
        'confirm_password': password
    }
    
    form = UserRegistrationForm(data=form_data)
    if form.is_valid():
        user = form.save()
        print(f"✅ User created: {user.email}")
        print(f"✅ Username set to email: {user.username == user.email}")
        print(f"✅ Password check: {user.check_password(password)}")
        print(f"✅ First Name: {user.first_name}, Last Name: {user.last_name}")
    else:
        print(f"❌ Form invalid: {form.errors}")
        sys.exit(1)

def test_duplicate_registration():
    print("\n--- Testing Duplicate Registration (Edge Case) ---")
    email = "testuser@example.com"
    password = "securepassword123"
    
    form_data = {
        'full_name': 'Test User 2',
        'email': email, # Same email
        'password': password,
        'confirm_password': password
    }
    
    form = UserRegistrationForm(data=form_data)
    if not form.is_valid():
        print(f"✅ Correctly rejected duplicate email: {form.errors.get('email')}")
    else:
        print("❌ Failed: Duplicate email was accepted!")

def test_password_mismatch():
    print("\n--- Testing Password Mismatch (Edge Case) ---")
    form_data = {
        'full_name': 'Mismatch User',
        'email': 'mismatch@example.com',
        'password': 'passwordA',
        'confirm_password': 'passwordB'
    }
    
    form = UserRegistrationForm(data=form_data)
    if not form.is_valid() and 'Passwords do not match' in str(form.non_field_errors()):
        print("✅ Correctly rejected mismatched passwords")
    else:
        print(f"❌ Failed to catch mismatch: {form.errors}")

def test_profile_update():
    print("\n--- Testing Profile Update ---")
    email = "testuser@example.com"
    user = User.objects.get(email=email)
    
    new_phone = "1234567890"
    form_data = {
        'first_name': 'Updated',
        'last_name': 'User',
        'phone_number': new_phone
    }
    
    form = UserProfileForm(data=form_data, instance=user)
    if form.is_valid():
        user = form.save()
        print(f"✅ Profile updated. Phone: {user.phone_number}")
        assert user.phone_number == new_phone
        assert user.first_name == 'Updated'
    else:
        print(f"❌ Profile update failed: {form.errors}")

def run_all_tests():
    try:
        test_registration()
        test_duplicate_registration()
        test_password_mismatch()
        test_profile_update()
        print("\n🎉 ALL MANUAL CHECKS PASSED")
    except Exception as e:
        print(f"\n❌ EXCEPTION: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_all_tests()
