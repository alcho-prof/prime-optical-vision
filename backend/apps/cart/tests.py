from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings
from apps.catalog.models import Category, Product, ProductVariant
from django.core.files.uploadedfile import SimpleUploadedFile

User = get_user_model()

class CartSessionTests(TestCase):
    def setUp(self):
        # Create user (optional for session cart, but good to have)
        self.user = User.objects.create_user(username='testuser', password='password123', email='test@test.com')
        
        # Create product with Price
        self.category = Category.objects.create(name='Glasses')
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            description='Test Desc',
            price_range='100',
            price=Decimal('500.00')  # Real price
        )
        
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        
        self.variant = ProductVariant.objects.create(
            product=self.product,
            color_name='Black',
            image=image
        )
        self.variant_id = str(self.variant.id)

    def test_add_to_cart_guest(self):
        """Test adding item as anonymous user updates session"""
        url = reverse('cart:add', args=[self.variant.id])
        response = self.client.post(url, {'quantity': 2})
        
        self.assertEqual(response.status_code, 302)
        session = self.client.session
        self.assertIn(settings.CART_SESSION_ID, session)
        cart = session[settings.CART_SESSION_ID]
        self.assertIn(self.variant_id, cart)
        self.assertEqual(cart[self.variant_id]['quantity'], 2)
        self.assertEqual(cart[self.variant_id]['price'], '500.00')

    def test_add_same_item_increases_quantity(self):
        url = reverse('cart:add', args=[self.variant.id])
        self.client.post(url, {'quantity': 1})
        self.client.post(url, {'quantity': 2})
        
        session = self.client.session
        cart = session[settings.CART_SESSION_ID]
        self.assertEqual(cart[self.variant_id]['quantity'], 3)

    def test_remove_from_cart(self):
        # Manually set session
        session = self.client.session
        session[settings.CART_SESSION_ID] = {
            self.variant_id: {'quantity': 1, 'price': '500.00'}
        }
        session.save()
        
        url = reverse('cart:remove', args=[self.variant.id])
        self.client.post(url)
        
        session = self.client.session
        self.assertNotIn(self.variant_id, session[settings.CART_SESSION_ID])

    def test_update_quantity(self):
        session = self.client.session
        session[settings.CART_SESSION_ID] = {
            self.variant_id: {'quantity': 1, 'price': '500.00'}
        }
        session.save()
        
        url = reverse('cart:update', args=[self.variant.id])
        self.client.post(url, {'quantity': 5})
        
        session = self.client.session
        self.assertEqual(session[settings.CART_SESSION_ID][self.variant_id]['quantity'], 5)

    def test_context_processor_exposes_cart(self):
        """Test that templates receive the cart object"""
        url = reverse('cart:add', args=[self.variant.id])
        self.client.post(url, {'quantity': 1})
        
        response = self.client.get(reverse('cart:detail'))
        self.assertIn('cart', response.context)
        cart_obj = response.context['cart']
        self.assertEqual(len(cart_obj), 1)
        self.assertEqual(cart_obj.get_total_price(), Decimal('500.00'))
