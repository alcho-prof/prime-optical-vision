"""
Tests for Billing Application
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.billing.models import Payment
from apps.orders.models import Order, OrderItem
from apps.catalog.models import Product, ProductVariant, Category
from apps.lenses.models import Lens
from decimal import Decimal
import json

User = get_user_model()


class PaymentModelTest(TestCase):
    """Test Payment model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Eyeglasses', slug='eyeglasses')
        self.product = Product.objects.create(
            name='Test Frame',
            slug='test-frame',
            category=self.category,
            description='Test',
            base_price=1000
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            color_name='Black',
            in_stock=True
        )
        self.lens = Lens.objects.create(
            name='Standard Lens',
            lens_type='single',
            price=500
        )
        self.order = Order.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            phone='1234567890',
            address='Test Address',
            city='Test City',
            state='Test State',
            pincode='123456',
            total_amount=Decimal('1500.00')
        )
        
    def test_payment_creation(self):
        """Test creating a payment"""
        payment = Payment.objects.create(
            order=self.order,
            razorpay_order_id='order_test123',
            amount=Decimal('1500.00'),
            currency='INR',
            status='created'
        )
        self.assertIsNotNone(payment.id)
        self.assertEqual(payment.order, self.order)
        self.assertEqual(payment.amount, Decimal('1500.00'))
        self.assertEqual(payment.status, 'created')
        
    def test_payment_str_method(self):
        """Test string representation"""
        payment = Payment.objects.create(
            order=self.order,
            razorpay_order_id='order_test456',
            amount=Decimal('1500.00')
        )
        self.assertIn('order_test456', str(payment))
        
    def test_payment_success(self):
        """Test successful payment"""
        payment = Payment.objects.create(
            order=self.order,
            razorpay_order_id='order_success',
            amount=Decimal('1500.00'),
            status='created'
        )
        payment.status = 'success'
        payment.razorpay_payment_id = 'pay_success123'
        payment.save()
        
        self.assertEqual(payment.status, 'success')
        self.assertIsNotNone(payment.razorpay_payment_id)


class PaymentViewTest(TestCase):
    """Test Payment views"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Sunglasses', slug='sunglasses')
        self.product = Product.objects.create(
            name='Aviator',
            slug='aviator',
            category=self.category,
            description='Classic',
            base_price=2000
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            color_name='Gold',
            in_stock=True
        )
        self.lens = Lens.objects.create(
            name='Premium Lens',
            lens_type='progressive',
            price=1000
        )
        self.order = Order.objects.create(
            user=self.user,
            full_name='Test User',
            email='test@example.com',
            phone='9876543210',
            address='123 Test St',
            city='Mumbai',
            state='Maharashtra',
            pincode='400001',
            total_amount=Decimal('3000.00')
        )
        
    def test_payment_page_requires_login(self):
        """Test that payment page requires authentication"""
        response = self.client.get(
            reverse('billing:payment', kwargs={'order_id': self.order.id})
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
    def test_payment_page_loads_for_authenticated_user(self):
        """Test payment page loads for logged-in user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('billing:payment', kwargs={'order_id': self.order.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'billing/payment.html')
        
    def test_payment_page_contains_order_details(self):
        """Test that payment page shows order information"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('billing:payment', kwargs={'order_id': self.order.id})
        )
        self.assertContains(response, 'Test User')
        self.assertContains(response, '3000')


class RazorpayIntegrationTest(TestCase):
    """Test Razorpay integration"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='razorpay_user',
            email='razorpay@example.com',
            password='testpass123'
        )
        self.category = Category.objects.create(name='Eyeglasses', slug='eyeglasses')
        self.product = Product.objects.create(
            name='Square Frame',
            slug='square-frame',
            category=self.category,
            description='Modern square frame',
            base_price=1800
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            color_name='Black',
            in_stock=True
        )
        self.order = Order.objects.create(
            user=self.user,
            full_name='Razorpay User',
            email='razorpay@example.com',
            phone='1231231234',
            address='Razorpay St',
            city='Bangalore',
            state='Karnataka',
            pincode='560001',
            total_amount=Decimal('1800.00')
        )
        
    def test_razorpay_order_creation(self):
        """Test that Razorpay order is created"""
        payment = Payment.objects.create(
            order=self.order,
            razorpay_order_id='order_razorpay123',
            amount=Decimal('1800.00'),
            currency='INR',
            status='created'
        )
        self.assertEqual(payment.currency, 'INR')
        self.assertEqual(payment.status, 'created')
