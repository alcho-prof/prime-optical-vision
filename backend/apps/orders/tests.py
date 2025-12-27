from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from apps.orders.models import Order, OrderItem
from apps.catalog.models import Category, Product, ProductVariant
from apps.cart.hybrid_cart import HybridCart

User = get_user_model()

class MockRequest:
    def __init__(self, session, user=None):
        self.session = session
        self.user = user

class CheckoutTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@test.com', password='password')
        self.category = Category.objects.create(name='Glasses')
        self.product = Product.objects.create(name='Frame X', category=self.category, price='1000.00')
        self.variant = ProductVariant.objects.create(product=self.product, color_name='Black')
        
    def test_checkout_creates_order(self):
        # 1. Add item to cart
        self.client.post(reverse('cart:add', args=[self.variant.id]), {'quantity': 1})
        
        # 2. Post to checkout
        url = reverse('orders:checkout')
        data = {
            'full_name': 'John Doe',
            'email': 'john@example.com',
            'phone_number': '1234567890',
            'address_line_1': '123 Street',
            'city': 'Test City',
            'postal_code': '12345',
            'payment_method': 'COD'
        }
        response = self.client.post(url, data)
        
        # 3. Verify success redirect
        self.assertEqual(response.status_code, 302)
        
        # 4. Verify Order created
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.first()
        self.assertEqual(order.full_name, 'John Doe')
        self.assertEqual(order.total_amount, Decimal('1000.00'))
        
        # 5. Verify Order Items
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().product_variant, self.variant)
        
        # 6. Verify Cart Cleared
        from django.contrib.auth.models import AnonymousUser
        request = MockRequest(self.client.session, AnonymousUser())
        cart = HybridCart(request)
        self.assertEqual(len(cart), 0)

    def test_authenticated_user_checkout_links_user(self):
        self.client.force_login(self.user)
        self.client.post(reverse('cart:add', args=[self.variant.id]), {'quantity': 1})
        
        self.client.post(reverse('orders:checkout'), {
            'full_name': 'User Name',
            'email': 'user@example.com',
            'phone_number': '1112223333',
            'address_line_1': 'User Addr',
            'city': 'City',
            'postal_code': '00000',
            'payment_method': 'COD'
        })
        
        order = Order.objects.first()
        self.assertEqual(order.user, self.user)
