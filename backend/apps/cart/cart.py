from decimal import Decimal
from django.conf import settings
from apps.catalog.models import ProductVariant
from apps.lenses.models import LensType

class Cart:
    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def _generate_cart_id(self, variant_id, lens_id=None):
        if lens_id:
            return f"{variant_id}-{lens_id}"
        return str(variant_id)

    def add(self, product_variant, quantity=1, override_quantity=False, lens_id=None):
        """
        Add a product to the cart with optional lens.
        """
        cart_id = self._generate_cart_id(product_variant.id, lens_id)
        
        if cart_id not in self.cart:
            self.cart[cart_id] = {
                'quantity': 0,
                'price': str(product_variant.product.price),
                'variant_id': product_variant.id,
                'lens_id': lens_id
            }
        
        if override_quantity:
            self.cart[cart_id]['quantity'] = quantity
        else:
            self.cart[cart_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product_variant, lens_id=None):
        cart_id = self._generate_cart_id(product_variant.id, lens_id)
        if cart_id in self.cart:
            del self.cart[cart_id]
            self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        # Collect IDs
        variant_ids = set()
        lens_ids = set()
        for item in self.cart.values():
            variant_ids.add(item['variant_id'])
            if item.get('lens_id'):
                lens_ids.add(item['lens_id'])
                
        variants = {v.id: v for v in ProductVariant.objects.filter(id__in=variant_ids)}
        lenses = {l.id: l for l in LensType.objects.filter(id__in=lens_ids)}
        
        cart_copy = self.cart.copy()
        
        for cart_id, item in cart_copy.items():
            variant = variants.get(int(item['variant_id']))
            item['product_variant'] = variant
            
            # Base price
            price = Decimal(item['price'])
            
            # Lens Logic
            lens = None
            if item.get('lens_id'):
                lens = lenses.get(int(item['lens_id']))
                if lens:
                    price += lens.price
            item['lens'] = lens
            
            item['price'] = price
            item['total_price'] = price * item['quantity']
            item['cart_id'] = cart_id # Useful for removal
            
            yield item
            
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        total = Decimal('0.00')
        for item in self.cart.values():
            price = Decimal(item['price'])
            # We must re-fetch lens price here ideally or store it. 
            # Storing is better for performance but requires sync if admin changes price.
            # For MVP, let's re-fetch in __iter__... 
            # BUT get_total_price is usually called often. 
            # Let's trust the stored 'price' in Add? No, Add only stores base price.
            # We need to calculate it properly.
            
            # To avoid N+1 queries here, we might want to change get_total_price to use the helper 
            # or iterate over the generator which already fetches everything.
            pass
        
        # Generator approach (cleaner)
        return sum(item['total_price'] for item in self.__iter__())

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()
