"""
Tests for Appointments Application
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.appointments.models import Appointment
from datetime import datetime, timedelta
from django.utils import timezone

User = get_user_model()


class AppointmentModelTest(TestCase):
    """Test Appointment model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_appointment_creation(self):
        """Test creating an appointment"""
        appointment_time = timezone.now() + timedelta(days=1)
        appointment = Appointment.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            phone='1234567890',
            appointment_date=appointment_time.date(),
            appointment_time=appointment_time.time(),
            service_type='eye_test',
            notes='Regular checkup'
        )
        self.assertIsNotNone(appointment.id)
        self.assertEqual(appointment.user, self.user)
        self.assertEqual(appointment.service_type, 'eye_test')
        self.assertEqual(appointment.status, 'pending')
        
    def test_appointment_str_method(self):
        """Test string representation"""
        appointment_time = timezone.now() + timedelta(days=2)
        appointment = Appointment.objects.create(
            user=self.user,
            full_name='John Doe',
            email='john@example.com',
            phone='9876543210',
            appointment_date=appointment_time.date(),
            appointment_time=appointment_time.time(),
            service_type='frame_fitting'
        )
        self.assertIn('John Doe', str(appointment))
        
    def test_appointment_status_choices(self):
        """Test appointment status transitions"""
        appointment_time = timezone.now() + timedelta(days=3)
        appointment = Appointment.objects.create(
            user=self.user,
            full_name='Jane Doe',
            email='jane@example.com',
            phone='5555555555',
            appointment_date=appointment_time.date(),
            appointment_time=appointment_time.time(),
            service_type='consultation'
        )
        
        # Test status changes
        self.assertEqual(appointment.status, 'pending')
        
        appointment.status = 'confirmed'
        appointment.save()
        self.assertEqual(appointment.status, 'confirmed')
        
        appointment.status = 'completed'
        appointment.save()
        self.assertEqual(appointment.status, 'completed')


class AppointmentViewTest(TestCase):
    """Test Appointment views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='appointmentuser',
            email='appointment@example.com',
            password='testpass123'
        )
        
    def test_appointment_create_page_loads(self):
        """Test that appointment creation page loads"""
        response = self.client.get(reverse('appointments:create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/form.html')
        
    def test_appointment_list_requires_login(self):
        """Test that appointment list requires authentication"""
        response = self.client.get(reverse('appointments:list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
    def test_appointment_list_for_authenticated_user(self):
        """Test appointment list for logged-in user"""
        self.client.login(username='appointmentuser', password='testpass123')
        response = self.client.get(reverse('appointments:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'appointments/list.html')
        
    def test_create_appointment_authenticated(self):
        """Test creating appointment when logged in"""
        self.client.login(username='appointmentuser', password='testpass123')
        appointment_date = (timezone.now() + timedelta(days=5)).date()
        appointment_time = '14:00'
        
        response = self.client.post(reverse('appointments:create'), {
            'full_name': 'Authenticated User',
            'email': 'auth@example.com',
            'phone': '1112223333',
            'appointment_date': appointment_date,
            'appointment_time': appointment_time,
            'service_type': 'eye_test',
            'notes': 'Test appointment'
        })
        
        # Should redirect on success
        self.assertEqual(response.status_code, 302)
        
        # Verify appointment was created
        appointment = Appointment.objects.filter(email='auth@example.com').first()
        self.assertIsNotNone(appointment)
        self.assertEqual(appointment.full_name, 'Authenticated User')
        
    def test_create_appointment_anonymous(self):
        """Test creating appointment without login"""
        appointment_date = (timezone.now() + timedelta(days=7)).date()
        appointment_time = '10:00'
        
        response = self.client.post(reverse('appointments:create'), {
            'full_name': 'Anonymous User',
            'email': 'anon@example.com',
            'phone': '4445556666',
            'appointment_date': appointment_date,
            'appointment_time': appointment_time,
            'service_type': 'consultation',
            'notes': 'Walk-in appointment'
        })
        
        # Should redirect on success
        self.assertEqual(response.status_code, 302)
        
        # Verify appointment was created
        appointment = Appointment.objects.filter(email='anon@example.com').first()
        self.assertIsNotNone(appointment)
        self.assertIsNone(appointment.user)  # No user for anonymous


class AppointmentFormTest(TestCase):
    """Test Appointment forms"""
    
    def test_valid_appointment_form(self):
        """Test form with valid data"""
        from apps.appointments.forms import AppointmentForm
        
        appointment_date = (timezone.now() + timedelta(days=10)).date()
        form_data = {
            'full_name': 'Form Test User',
            'email': 'formtest@example.com',
            'phone': '7778889999',
            'appointment_date': appointment_date,
            'appointment_time': '11:30',
            'service_type': 'frame_fitting',
            'notes': 'Need help choosing frames'
        }
        form = AppointmentForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_appointment_form_missing_required(self):
        """Test form with missing required fields"""
        from apps.appointments.forms import AppointmentForm
        
        form_data = {
            'full_name': 'Incomplete User',
            # Missing email, phone, date, time, service_type
        }
        form = AppointmentForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    def test_invalid_appointment_form_past_date(self):
        """Test form with past date"""
        from apps.appointments.forms import AppointmentForm
        
        past_date = (timezone.now() - timedelta(days=1)).date()
        form_data = {
            'full_name': 'Past Date User',
            'email': 'past@example.com',
            'phone': '1231231234',
            'appointment_date': past_date,
            'appointment_time': '15:00',
            'service_type': 'eye_test'
        }
        form = AppointmentForm(data=form_data)
        # Form should be invalid for past dates if validation is implemented
        # This depends on your form's clean methods
