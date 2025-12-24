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

    def _generate_cart_id(self, variant_id, lens_id=None, prescription_id=None):
        parts = [str(variant_id)]
        if lens_id:
            parts.append(str(lens_id))
        else:
            parts.append("0") # Use 0 as placeholder to keep position if we want consistent easier parsing or just append?
            # Actually, standardizing format "v-l-p" is safer.
            # But the previous implementation was "v-l" or "v".
            # Let's use a safe join that we can split flexibly or use strict format.
            # strict "v-l-p" where l or p can be "None" or "0".
            pass 
        
        # Let's stick to appending only if present, but parsing becomes harder.
        # Better: Join with separators, but we need to know which part is which.
        # "variant_id" is always there.
        # If lens_id is there, it's appended.
        # If prescription_id is there, it's appended.
        # If I have variant+prescription (no lens - unlikely for glasses), it might look like variant-rxID.
        # If I have variant+lens (no Rx - sunglasses), it is variant-lens.
        # If I have variant+lens+rx, it is variant-lens-rx.
        
        # To avoid ambiguity, let's use: f"{variant_id}-{lens_id or ''}-{prescription_id or ''}"
        # Example: "1--", "1-2-", "1-2-5", "1--5"
        
        l = str(lens_id) if lens_id else ""
        p = str(prescription_id) if prescription_id else ""
        
        return f"{variant_id}-{l}-{p}"

    def add(self, product_variant, quantity=1, override_quantity=False, lens_id=None, prescription_id=None):
        """
        Add a product to the cart with optional lens and prescription.
        """
        cart_id = self._generate_cart_id(product_variant.id, lens_id, prescription_id)
        
        if cart_id not in self.cart:
            self.cart[cart_id] = {
                'quantity': 0,
                'price': str(product_variant.product.price),
                'variant_id': product_variant.id,
                'lens_id': lens_id,
                'prescription_id': prescription_id
            }
        
        if override_quantity:
            self.cart[cart_id]['quantity'] = quantity
        else:
            self.cart[cart_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, product_variant, lens_id=None, prescription_id=None):
        cart_id = self._generate_cart_id(product_variant.id, lens_id, prescription_id)
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
        prescription_ids = set()
        
        for item in self.cart.values():
            variant_ids.add(item['variant_id'])
            if item.get('lens_id'):
                lens_ids.add(item['lens_id'])
            if item.get('prescription_id'):
                prescription_ids.add(item['prescription_id'])
                
        variants = {v.id: v for v in ProductVariant.objects.filter(id__in=variant_ids)}
        lenses = {l.id: l for l in LensType.objects.filter(id__in=lens_ids)}
        
        # Avoid circular import if possible, but we need Prescription model
        from apps.prescriptions.models import Prescription
        prescriptions = {p.id: p for p in Prescription.objects.filter(id__in=prescription_ids)}
        
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
            
            # Prescription Logic
            prescription = None
            if item.get('prescription_id'):
                prescription = prescriptions.get(int(item['prescription_id']))
            item['prescription'] = prescription
            
            item['price'] = price
            item['total_price'] = price * item['quantity']
            item['cart_id'] = cart_id 
            
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
