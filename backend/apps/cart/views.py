from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import Cart, CartItem
from apps.catalog.models import ProductVariant

@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

@login_required
@require_POST
def add_to_cart(request, variant_id):
    variant = get_object_or_404(ProductVariant, id=variant_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, item_created = CartItem.objects.get_or_create(
        cart=cart, 
        product_variant=variant
    )
    
    if not item_created:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, f"Updated quantity for {variant.product.name} ({variant.color_name})")
    else:
        messages.success(request, f"Added {variant.product.name} ({variant.color_name}) to cart")

    # Redirect to where the user came from or cart
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'cart:detail'
    return redirect(next_url)

@login_required
@require_POST
def remove_from_cart(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    item.delete()
    messages.success(request, "Item removed from cart")
    return redirect('cart:detail')

@login_required
@require_POST
def update_quantity(request, item_id):
    cart = get_object_or_404(Cart, user=request.user)
    item = get_object_or_404(CartItem, id=item_id, cart=cart)
    
    try:
        quantity = int(request.POST.get('quantity', 1))
        if quantity <= 0:
            item.delete()
            messages.success(request, "Item removed from cart")
        else:
            item.quantity = quantity
            item.save()
            messages.success(request, "Cart updated")
    except ValueError:
        pass
        
    return redirect('cart:detail')
