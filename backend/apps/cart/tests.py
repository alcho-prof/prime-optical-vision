from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Cart, CartItem
from apps.catalog.models import Category, Product, ProductVariant

User = get_user_model()

from django.core.files.uploadedfile import SimpleUploadedFile

class CartTests(TestCase):
    def setUp(self):
        # Create user
        self.user = User.objects.create_user(username='testuser', password='password123', email='test@test.com')
        self.client.force_login(self.user)
        
        # Create product
        self.category = Category.objects.create(name='Glasses')
        self.product = Product.objects.create(
            name='Test Product',
            category=self.category,
            description='Test Desc',
            price_range='100'
        )
        
        # Create dummy image
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        
        self.variant = ProductVariant.objects.create(
            product=self.product,
            color_name='Black',
            image=image
        )

    def test_add_to_cart_creates_cart(self):
        url = reverse('cart:add', args=[self.variant.id])
        self.client.post(url)
        
        self.assertTrue(Cart.objects.filter(user=self.user).exists())
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.total_items, 1)

    def test_add_same_item_increases_quantity(self):
        url = reverse('cart:add', args=[self.variant.id])
        self.client.post(url)
        self.client.post(url)
        
        cart = Cart.objects.get(user=self.user)
        self.assertEqual(cart.total_items, 2)
        item = CartItem.objects.get(cart=cart, product_variant=self.variant)
        self.assertEqual(item.quantity, 2)

    def test_product_detail_page_has_add_to_cart_button(self):
        url = reverse('catalog:product_detail', args=[self.product.slug])
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Add to Cart')
        # Verify the form action points to the cart add URL
        expected_action = reverse('cart:add', args=[self.variant.id])
        self.assertContains(response, f'action="{expected_action}"')

    def test_remove_from_cart(self):
        # Add item first
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, product_variant=self.variant, quantity=1)
        
        url = reverse('cart:remove', args=[item.id])
        self.client.post(url)
        
        self.assertEqual(CartItem.objects.count(), 0)

    def test_update_quantity(self):
        # Add item first
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, product_variant=self.variant, quantity=1)
        
        url = reverse('cart:update', args=[item.id])
        self.client.post(url, {'quantity': 5})
        
        item.refresh_from_db()
        self.assertEqual(item.quantity, 5)

    def test_update_quantity_zero_removes_item(self):
        cart = Cart.objects.create(user=self.user)
        item = CartItem.objects.create(cart=cart, product_variant=self.variant, quantity=1)
        
        url = reverse('cart:update', args=[item.id])
        self.client.post(url, {'quantity': 0})
        
        self.assertEqual(CartItem.objects.count(), 0)
