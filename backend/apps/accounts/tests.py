from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .forms import UserRegistrationForm, UserProfileForm

User = get_user_model()

class AccountTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.email = "testuser@example.com"
        self.password = "securepassword123"
        self.register_url = reverse('accounts:register')
        self.login_url = reverse('accounts:login')
        self.profile_url = reverse('accounts:profile')

    def test_registration_success(self):
        """Test valid registration creates a user."""
        data = {
            'full_name': 'Test User',
            'email': self.email,
            'password': self.password,
            'confirm_password': self.password
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 302)  # Redirects to home
        self.assertTrue(User.objects.filter(email=self.email).exists())
        user = User.objects.get(email=self.email)
        self.assertEqual(user.username, self.email)
        self.assertTrue(user.check_password(self.password))

    def test_registration_duplicate_email(self):
        """Test that registering with an existing email fails."""
        User.objects.create_user(username=self.email, email=self.email, password=self.password)
        
        data = {
            'full_name': 'Test User 2',
            'email': self.email,
            'password': self.password,
            'confirm_password': self.password
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        # Manual form error check due to assertFormError issue
        form = response.context['form']
        self.assertTrue(form.is_bound, "Form should be bound")
        self.assertIn('email', form.errors, "Email field should have errors")
        self.assertEqual(form.errors['email'], ['User with this Email address already exists.'])

    def test_registration_password_mismatch(self):
        """Test that password mismatch is caught."""
        data = {
            'full_name': 'Mismatch User',
            'email': 'mismatch@example.com',
            'password': 'passwordA',
            'confirm_password': 'passwordB'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Passwords do not match')

    def test_login_success(self):
        """Test valid login."""
        User.objects.create_user(username=self.email, email=self.email, password=self.password)
        data = {
            'username': self.email,  # Custom form uses username field mapping to email
            'password': self.password
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, 302)  # Redirects
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_profile_update(self):
        """Test profile update requires login and updates fields."""
        user = User.objects.create_user(username=self.email, email=self.email, password=self.password)
        self.client.force_login(user)
        
        new_phone = "1234567890"
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'phone_number': new_phone
        }
        response = self.client.post(self.profile_url, data)
        self.assertEqual(response.status_code, 302)
        
        user.refresh_from_db()
        self.assertEqual(user.phone_number, new_phone)
        self.assertEqual(user.first_name, 'Updated')
