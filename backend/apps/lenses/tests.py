from decimal import Decimal
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from apps.catalog.models import Category, Product, ProductVariant
from apps.lenses.models import LensType
from apps.cart.cart import Cart

class LensSelectionTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Glasses')
        self.product = Product.objects.create(
            name='Frame X', category=self.category, price='1000.00'
        )
        self.variant = ProductVariant.objects.create(product=self.product, color_name='Black')
        
        self.lens_zero = LensType.objects.create(name='Zero Power', price='0.00')
        self.lens_single = LensType.objects.create(name='Single Vision', price='500.00')

    def test_add_cart_with_lens(self):
        url = reverse('cart:add', args=[self.variant.id])
        
        # Add Frame + Single Vision Lens
        self.client.post(url, {'quantity': 1, 'lens_id': self.lens_single.id})
        
        cart = self.client.session[settings.CART_SESSION_ID]
        cart_key_1 = f"{self.variant.id}-{self.lens_single.id}"
        
        self.assertIn(cart_key_1, cart)
        self.assertEqual(cart[cart_key_1]['lens_id'], str(self.lens_single.id))

    def test_add_separate_lines_for_different_lenses(self):
        url = reverse('cart:add', args=[self.variant.id])
        
        # Add 1x Frame + Zero Power
        self.client.post(url, {'quantity': 1, 'lens_id': self.lens_zero.id})
        
        # Add 1x Frame + Single Vision
        self.client.post(url, {'quantity': 1, 'lens_id': self.lens_single.id})
        
        cart = self.client.session[settings.CART_SESSION_ID]
        self.assertEqual(len(cart), 2) # Should be 2 distinct items

    def test_total_price_calculation(self):
        url = reverse('cart:add', args=[self.variant.id])
        
        # Frame (1000) + Single Vision (500) = 1500
        self.client.post(url, {'quantity': 2, 'lens_id': self.lens_single.id})
        
        # Explicitly check cart object logic
        cart = Cart(self.client)
        total = cart.get_total_price()
        
        expected_total = (Decimal('1000.00') + Decimal('500.00')) * 2
        self.assertEqual(total, expected_total)
