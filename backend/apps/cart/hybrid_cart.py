"""
Hybrid Cart Implementation
Combines session-based cart (anonymous) with database cart (authenticated)
"""

from decimal import Decimal
from django.conf import settings
from apps.catalog.models import ProductVariant
from apps.lenses.models import LensType
from apps.prescriptions.models import Prescription
from .models import Cart as DBCart, CartItem


class HybridCart:
    """
    Hybrid cart that uses:
    - Session storage for anonymous users (fast, no DB queries)
    - Database storage for authenticated users (persistent, synced)
    """
    
    def __init__(self, request):
        self.request = request
        self.user = request.user
        self.session = request.session
        
        if self.user.is_authenticated:
            # Use database cart for logged-in users
            self.db_cart, created = DBCart.objects.get_or_create(user=self.user)
            self.storage_type = 'database'
        else:
            # Use session cart for anonymous users
            cart = self.session.get(settings.CART_SESSION_ID)
            if not cart:
                cart = self.session[settings.CART_SESSION_ID] = {}
            self.session_cart = cart
            self.storage_type = 'session'
    
    def _generate_cart_id(self, variant_id, lens_id=None, prescription_id=None):
        """Generate unique cart ID for session storage"""
        l = str(lens_id) if lens_id else ""
        p = str(prescription_id) if prescription_id else ""
        return f"{variant_id}-{l}-{p}"
    
    def add(self, product_variant, quantity=1, override_quantity=False, lens_id=None, prescription_id=None):
        """Add product to cart"""
        if self.storage_type == 'database':
            return self._add_to_db(product_variant, quantity, override_quantity, lens_id, prescription_id)
        else:
            return self._add_to_session(product_variant, quantity, override_quantity, lens_id, prescription_id)
    
    def _add_to_db(self, product_variant, quantity, override_quantity, lens_id, prescription_id):
        """Add to database cart"""
        lens = LensType.objects.get(id=lens_id) if lens_id else None
        prescription = Prescription.objects.get(id=prescription_id) if prescription_id else None
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=self.db_cart,
            product_variant=product_variant,
            lens=lens,
            prescription=prescription,
            defaults={'quantity': 0}
        )
        
        if override_quantity:
            cart_item.quantity = quantity
        else:
            cart_item.quantity += quantity
        
        cart_item.save()
    
    def _add_to_session(self, product_variant, quantity, override_quantity, lens_id, prescription_id):
        """Add to session cart"""
        cart_id = self._generate_cart_id(product_variant.id, lens_id, prescription_id)
        
        if cart_id not in self.session_cart:
            self.session_cart[cart_id] = {
                'quantity': 0,
                'price': str(product_variant.product.price),
                'variant_id': product_variant.id,
                'lens_id': lens_id,
                'prescription_id': prescription_id
            }
        
        if override_quantity:
            self.session_cart[cart_id]['quantity'] = quantity
        else:
            self.session_cart[cart_id]['quantity'] += quantity
        
        self.save()
    
    def remove(self, product_variant, lens_id=None, prescription_id=None):
        """Remove product from cart"""
        if self.storage_type == 'database':
            return self._remove_from_db(product_variant, lens_id, prescription_id)
        else:
            return self._remove_from_session(product_variant, lens_id, prescription_id)
    
    def _remove_from_db(self, product_variant, lens_id, prescription_id):
        """Remove from database cart"""
        lens = LensType.objects.get(id=lens_id) if lens_id else None
        prescription = Prescription.objects.get(id=prescription_id) if prescription_id else None
        
        try:
            cart_item = CartItem.objects.get(
                cart=self.db_cart,
                product_variant=product_variant,
                lens=lens,
                prescription=prescription
            )
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass
    
    def _remove_from_session(self, product_variant, lens_id, prescription_id):
        """Remove from session cart"""
        cart_id = self._generate_cart_id(product_variant.id, lens_id, prescription_id)
        if cart_id in self.session_cart:
            del self.session_cart[cart_id]
            self.save()
    
    def save(self):
        """Save session cart"""
        if self.storage_type == 'session':
            self.session.modified = True
    
    def __iter__(self):
        """Iterate over cart items"""
        if self.storage_type == 'database':
            return self._iter_db()
        else:
            return self._iter_session()
    
    def _iter_db(self):
        """Iterate over database cart items"""
        cart_items = CartItem.objects.filter(cart=self.db_cart).select_related(
            'product_variant',
            'product_variant__product',
            'lens',
            'prescription'
        )
        
        for cart_item in cart_items:
            # Calculate price
            price = cart_item.product_variant.product.price
            if cart_item.lens:
                price += cart_item.lens.price
            
            yield {
                'product_variant': cart_item.product_variant,
                'quantity': cart_item.quantity,
                'price': price,
                'total_price': price * cart_item.quantity,
                'lens': cart_item.lens,
                'prescription': cart_item.prescription,
                'cart_id': f"{cart_item.product_variant.id}-{cart_item.lens.id if cart_item.lens else ''}-{cart_item.prescription.id if cart_item.prescription else ''}"
            }
    
    def _iter_session(self):
        """Iterate over session cart items"""
        # Collect IDs
        variant_ids = set()
        lens_ids = set()
        prescription_ids = set()
        
        for item in self.session_cart.values():
            variant_ids.add(item['variant_id'])
            if item.get('lens_id'):
                lens_ids.add(item['lens_id'])
            if item.get('prescription_id'):
                prescription_ids.add(item['prescription_id'])
        
        # Fetch objects
        variants = {v.id: v for v in ProductVariant.objects.filter(id__in=variant_ids).select_related('product')}
        lenses = {l.id: l for l in LensType.objects.filter(id__in=lens_ids)}
        prescriptions = {p.id: p for p in Prescription.objects.filter(id__in=prescription_ids)}
        
        for cart_id, item in self.session_cart.copy().items():
            variant = variants.get(int(item['variant_id']))
            if not variant:
                continue
            
            # Calculate price
            price = Decimal(item['price'])
            lens = None
            if item.get('lens_id'):
                lens = lenses.get(int(item['lens_id']))
                if lens:
                    price += lens.price
            
            prescription = None
            if item.get('prescription_id'):
                prescription = prescriptions.get(int(item['prescription_id']))
            
            yield {
                'product_variant': variant,
                'quantity': item['quantity'],
                'price': price,
                'total_price': price * item['quantity'],
                'lens': lens,
                'prescription': prescription,
                'cart_id': cart_id
            }
    
    def __len__(self):
        """Get total number of items in cart"""
        if self.storage_type == 'database':
            return sum(item.quantity for item in CartItem.objects.filter(cart=self.db_cart))
        else:
            return sum(item['quantity'] for item in self.session_cart.values())
    
    def get_total_price(self):
        """Get total price of all items in cart"""
        return sum(item['total_price'] for item in self)
    
    def clear(self):
        """Clear cart"""
        if self.storage_type == 'database':
            CartItem.objects.filter(cart=self.db_cart).delete()
        else:
            del self.session[settings.CART_SESSION_ID]
            self.save()
    
    def sync_session_to_db(self):
        """
        Sync session cart to database cart on login.
        Called when user logs in.
        """
        if self.storage_type == 'database' and hasattr(self, 'session'):
            # Get session cart data
            session_cart_data = self.session.get(settings.CART_SESSION_ID, {})
            
            if session_cart_data:
                # Add each session cart item to database cart
                for cart_id, item in session_cart_data.items():
                    try:
                        variant = ProductVariant.objects.get(id=item['variant_id'])
                        lens = LensType.objects.get(id=item['lens_id']) if item.get('lens_id') else None
                        prescription = Prescription.objects.get(id=item['prescription_id']) if item.get('prescription_id') else None
                        
                        # Get or create cart item
                        cart_item, created = CartItem.objects.get_or_create(
                            cart=self.db_cart,
                            product_variant=variant,
                            lens=lens,
                            prescription=prescription,
                            defaults={'quantity': item['quantity']}
                        )
                        
                        if not created:
                            # If item exists, add quantities
                            cart_item.quantity += item['quantity']
                            cart_item.save()
                    
                    except (ProductVariant.DoesNotExist, LensType.DoesNotExist, Prescription.DoesNotExist):
                        # Skip invalid items
                        continue
                
                # Clear session cart after sync
                del self.session[settings.CART_SESSION_ID]
                self.session.modified = True
