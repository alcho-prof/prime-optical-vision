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
        
        # Key format: variant_id-lens_id-prescription_id
        # Both lens and prescription are None -> 'id--'
        cart_key = f"{self.variant_id}--"
        
        self.assertIn(cart_key, cart)
        self.assertEqual(cart[cart_key]['quantity'], 2)
        self.assertEqual(cart[cart_key]['price'], '500.00')

    def test_add_same_item_increases_quantity(self):
        url = reverse('cart:add', args=[self.variant.id])
        self.client.post(url, {'quantity': 1})
        self.client.post(url, {'quantity': 2})
        
        session = self.client.session
        cart_key = f"{self.variant_id}--"
        cart = session[settings.CART_SESSION_ID]
        self.assertEqual(cart[cart_key]['quantity'], 3)

    def test_remove_from_cart(self):
        cart_key = f"{self.variant_id}--"
        
        # Manually set session
        session = self.client.session
        session[settings.CART_SESSION_ID] = {
            cart_key: {'quantity': 1, 'price': '500.00', 'variant_id': self.variant.id}
        }
        session.save()
        
        url = reverse('cart:remove', args=[cart_key])
        self.client.post(url)
        
        session = self.client.session
        self.assertNotIn(cart_key, session[settings.CART_SESSION_ID])

    def test_update_quantity(self):
        cart_key = f"{self.variant_id}--"
        
        session = self.client.session
        session[settings.CART_SESSION_ID] = {
            cart_key: {'quantity': 1, 'price': '500.00', 'variant_id': self.variant.id}
        }
        session.save()
        
        url = reverse('cart:update', args=[cart_key])
        self.client.post(url, {'quantity': 5})
        
        session = self.client.session
        self.assertEqual(session[settings.CART_SESSION_ID][cart_key]['quantity'], 5)

    def test_context_processor_exposes_cart(self):
        """Test that templates receive the cart object"""
        url = reverse('cart:add', args=[self.variant.id])
        self.client.post(url, {'quantity': 1})
        
        response = self.client.get(reverse('cart:detail'))
        self.assertIn('cart', response.context)
        cart_obj = response.context['cart']
        self.assertEqual(len(cart_obj), 1)
        self.assertEqual(cart_obj.get_total_price(), Decimal('500.00'))


class CartSyncTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testsync', email='sync@test.com', password='password')
        self.category = Category.objects.create(name='Glasses')
        self.product = Product.objects.create(name='Frame Sync', category=self.category, price='1000.00')
        self.variant = ProductVariant.objects.create(product=self.product, color_name='Black')

    def test_sync_on_login(self):
        """Test that guest cart items are merged into database cart on login"""
        # 1. Add item as guest via view
        self.client.post(reverse('cart:add', args=[self.variant.id]), {'quantity': 1})
        
        # Verify item in session
        session = self.client.session
        self.assertIn(settings.CART_SESSION_ID, session)
        
        # 2. Login (triggers signal)
        login_success = self.client.login(email='sync@test.com', password='password')
        self.assertTrue(login_success)
        
        # 3. Verify Database Cart has the item
        from apps.cart.models import CartItem
        self.assertEqual(CartItem.objects.count(), 1)
        item = CartItem.objects.first()
        self.assertEqual(item.product_variant, self.variant)
        self.assertEqual(item.quantity, 1)
        self.assertEqual(item.cart.user, self.user)
        
        # 4. Verify Session Cart is cleared
        session = self.client.session
        self.assertNotIn(settings.CART_SESSION_ID, session)
