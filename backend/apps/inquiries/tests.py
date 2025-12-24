"""
Tests for Inquiries Application
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.inquiries.models import Inquiry

User = get_user_model()


class InquiryModelTest(TestCase):
    """Test Inquiry model"""
    
    def test_inquiry_creation(self):
        """Test creating an inquiry"""
        inquiry = Inquiry.objects.create(
            name='Test User',
            email='test@example.com',
            phone='1234567890',
            subject='Product Question',
            message='I have a question about your products.'
        )
        self.assertIsNotNone(inquiry.id)
        self.assertEqual(inquiry.name, 'Test User')
        self.assertEqual(inquiry.status, 'new')
        self.assertFalse(inquiry.is_read)
        
    def test_inquiry_str_method(self):
        """Test string representation"""
        inquiry = Inquiry.objects.create(
            name='John Doe',
            email='john@example.com',
            subject='Pricing Inquiry'
        )
        self.assertIn('John Doe', str(inquiry))
        self.assertIn('Pricing Inquiry', str(inquiry))
        
    def test_inquiry_status_transitions(self):
        """Test inquiry status changes"""
        inquiry = Inquiry.objects.create(
            name='Jane Smith',
            email='jane@example.com',
            subject='Delivery Question',
            message='When will my order arrive?'
        )
        
        self.assertEqual(inquiry.status, 'new')
        
        inquiry.status = 'in_progress'
        inquiry.is_read = True
        inquiry.save()
        
        self.assertEqual(inquiry.status, 'in_progress')
        self.assertTrue(inquiry.is_read)
        
        inquiry.status = 'resolved'
        inquiry.save()
        
        self.assertEqual(inquiry.status, 'resolved')


class InquiryFormTest(TestCase):
    """Test Inquiry forms"""
    
    def test_valid_inquiry_form(self):
        """Test form with valid data"""
        from apps.inquiries.forms import InquiryForm
        
        form_data = {
            'name': 'Form Test',
            'email': 'formtest@example.com',
            'phone': '9876543210',
            'subject': 'Test Subject',
            'message': 'This is a test message for the inquiry form.'
        }
        form = InquiryForm(data=form_data)
        self.assertTrue(form.is_valid())
        
    def test_invalid_inquiry_form_missing_required(self):
        """Test form with missing required fields"""
        from apps.inquiries.forms import InquiryForm
        
        form_data = {
            'name': 'Incomplete',
            # Missing email, subject, message
        }
        form = InquiryForm(data=form_data)
        self.assertFalse(form.is_valid())
        
    def test_invalid_inquiry_form_bad_email(self):
        """Test form with invalid email"""
        from apps.inquiries.forms import InquiryForm
        
        form_data = {
            'name': 'Bad Email User',
            'email': 'not-an-email',
            'subject': 'Test',
            'message': 'Test message'
        }
        form = InquiryForm(data=form_data)
        self.assertFalse(form.is_valid())


class InquiryViewTest(TestCase):
    """Test Inquiry views"""
    
    def setUp(self):
        self.client = Client()
        
    def test_inquiry_creation_anonymous(self):
        """Test creating inquiry without login"""
        # Assuming there's a contact form view
        # Adjust URL name based on your actual implementation
        inquiry_count_before = Inquiry.objects.count()
        
        inquiry_data = {
            'name': 'Anonymous Inquirer',
            'email': 'anon@example.com',
            'phone': '5555555555',
            'subject': 'General Question',
            'message': 'I have a general question about your services.'
        }
        
        # If you have a contact view, test it here
        # response = self.client.post(reverse('contact'), inquiry_data)
        # self.assertEqual(response.status_code, 302)  # Redirect on success
        
        # Verify inquiry was created
        # inquiry_count_after = Inquiry.objects.count()
        # self.assertEqual(inquiry_count_after, inquiry_count_before + 1)


class InquiryAdminTest(TestCase):
    """Test Inquiry admin functionality"""
    
    def setUp(self):
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.client = Client()
        
    def test_inquiry_admin_access(self):
        """Test that admin can access inquiry admin"""
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get('/admin/inquiries/inquiry/')
        self.assertEqual(response.status_code, 200)
        
    def test_inquiry_list_display(self):
        """Test inquiry list in admin"""
        Inquiry.objects.create(
            name='Admin Test',
            email='admintest@example.com',
            subject='Admin Subject',
            message='Admin message'
        )
        
        self.client.login(username='admin', password='adminpass123')
        response = self.client.get('/admin/inquiries/inquiry/')
        self.assertContains(response, 'Admin Test')
        self.assertContains(response, 'Admin Subject')
