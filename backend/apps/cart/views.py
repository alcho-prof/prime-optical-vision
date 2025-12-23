from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from .cart import Cart
from apps.catalog.models import ProductVariant

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@require_POST
def add_to_cart(request, variant_id):
    cart = Cart(request)
    variant = get_object_or_404(ProductVariant, id=variant_id)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
    except ValueError:
        quantity = 1
        
    override = request.POST.get('override_quantity') == 'True'
    
    # Capture lens_id from form
    lens_id = request.POST.get('lens_id')
    if lens_id == "": # Handle empty string if select field is default
        lens_id = None
    
    cart.add(product_variant=variant, quantity=quantity, override_quantity=override, lens_id=lens_id)
    messages.success(request, f"Added {variant.product.name} to cart.")
    
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'cart:detail'
    return redirect(next_url)

@require_POST
def remove_from_cart(request, item_id): # This is now the composite CART ID (variant-lens), OR we split URL.
    # Approach: Let's pass the composite ID string to this view.
    # But wait, urls.py typically expects int. We should check urls.py.
    # If urls.py uses <int:item_id>, this will break for "1-2".
    # Need to update urls.py to use <str:item_id> or similar.
    
    cart = Cart(request)
    
    # Parse the ID
    cart_id = str(item_id)
    parts = cart_id.split('-')
    variant_id = parts[0]
    lens_id = parts[1] if len(parts) > 1 else None
    
    # We need product variant object
    variant = get_object_or_404(ProductVariant, id=variant_id)
    
    cart.remove(variant, lens_id=lens_id)
    messages.success(request, "Item removed from cart")
    return redirect('cart:detail')

@require_POST
def update_quantity(request, item_id):
    cart = Cart(request)
    
    # Parse composite ID
    cart_id = str(item_id)
    parts = cart_id.split('-')
    variant_id = parts[0]
    lens_id = parts[1] if len(parts) > 1 else None
    
    variant = get_object_or_404(ProductVariant, id=variant_id)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            cart.remove(variant, lens_id=lens_id)
        else:
            cart.add(product_variant=variant, quantity=quantity, override_quantity=True, lens_id=lens_id)
            messages.success(request, "Cart updated")
    except ValueError:
        pass
        
    return redirect('cart:detail')
