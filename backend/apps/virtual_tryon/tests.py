"""
Tests for Virtual Try-On Application
"""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.catalog.models import Product, ProductVariant, Category
from apps.virtual_tryon.models import TryOnSession, TryOnPhoto, FaceDetectionCache
import uuid
import json

User = get_user_model()


class TryOnSessionModelTest(TestCase):
    """Test TryOnSession model"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_session_creation(self):
        """Test creating a try-on session"""
        session = TryOnSession.objects.create(
            user=self.user,
            session_id=str(uuid.uuid4())
        )
        self.assertIsNotNone(session.id)
        self.assertEqual(session.user, self.user)
        self.assertIsNotNone(session.created_at)
        
    def test_session_str_method(self):
        """Test string representation"""
        session = TryOnSession.objects.create(
            session_id='test-session-123'
        )
        self.assertIn('test-session-123', str(session))
        
    def test_anonymous_session(self):
        """Test creating session without user"""
        session = TryOnSession.objects.create(
            session_id=str(uuid.uuid4())
        )
        self.assertIsNone(session.user)


class TryOnPhotoModelTest(TestCase):
    """Test TryOnPhoto model"""
    
    def setUp(self):
        self.category = Category.objects.create(
            name='Sunglasses',
            slug='sunglasses'
        )
        self.product = Product.objects.create(
            name='Test Frame',
            slug='test-frame',
            category=self.category,
            description='Test description',
            base_price=1000
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            color_name='Black',
            in_stock=True
        )
        self.session = TryOnSession.objects.create(
            session_id=str(uuid.uuid4())
        )
        
    def test_photo_creation(self):
        """Test creating a try-on photo"""
        photo = TryOnPhoto.objects.create(
            session=self.session,
            variant=self.variant
        )
        self.assertIsNotNone(photo.id)
        self.assertEqual(photo.session, self.session)
        self.assertEqual(photo.variant, self.variant)


class VirtualTryOnViewTest(TestCase):
    """Test Virtual Try-On views"""
    
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(
            name='Eyeglasses',
            slug='eyeglasses'
        )
        self.product = Product.objects.create(
            name='Round Frame',
            slug='round-frame',
            category=self.category,
            description='Classic round frame',
            base_price=1500
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            color_name='Gold',
            in_stock=True
        )
        
    def test_tryon_page_loads(self):
        """Test that try-on page loads successfully"""
        response = self.client.get(reverse('virtual_tryon:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'virtual_tryon/tryon.html')
        
    def test_session_creation_on_page_load(self):
        """Test that session is created when page loads"""
        response = self.client.get(reverse('virtual_tryon:index'))
        self.assertIn('tryon_session_id', self.client.session)
        
    def test_product_specific_tryon(self):
        """Test try-on page for specific product"""
        response = self.client.get(
            reverse('virtual_tryon:product', kwargs={'slug': 'round-frame'})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Round Frame')


class TryOnAPITest(TestCase):
    """Test Virtual Try-On API endpoints"""
    
    def setUp(self):
        self.client = Client()
        self.session = TryOnSession.objects.create(
            session_id='test-api-session'
        )
        self.category = Category.objects.create(
            name='Sunglasses',
            slug='sunglasses'
        )
        self.product = Product.objects.create(
            name='Aviator',
            slug='aviator',
            category=self.category,
            description='Classic aviator',
            base_price=2000
        )
        self.variant = ProductVariant.objects.create(
            product=self.product,
            color_name='Silver',
            in_stock=True
        )
        
    def test_get_variant_overlay(self):
        """Test getting variant overlay data"""
        response = self.client.get(
            reverse('virtual_tryon:variant_overlay', kwargs={'variant_id': self.variant.id})
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        self.assertEqual(data['variant_id'], self.variant.id)
        self.assertEqual(data['product_name'], 'Aviator')
        self.assertEqual(data['color'], 'Silver')
        
    def test_cache_face_data(self):
        """Test caching face detection data"""
        face_data = {
            'landmarks': [[100, 200], [150, 250]],
            'confidence': 0.95
        }
        response = self.client.post(
            reverse('virtual_tryon:cache_face'),
            data=json.dumps({
                'session_id': 'test-api-session',
                'face_data': face_data
            }),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        
        # Verify cache was created
        cache = FaceDetectionCache.objects.filter(session=self.session).first()
        self.assertIsNotNone(cache)
        self.assertEqual(cache.face_data, face_data)
