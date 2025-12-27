from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Wishlist
from apps.catalog.models import Product


@login_required
def wishlist_view(request):
    """Display user's wishlist"""
    wishlist_items = Wishlist.objects.filter(user=request.user).select_related('product')
    return render(request, 'wishlist/wishlist.html', {'wishlist_items': wishlist_items})


@login_required
@require_POST
def add_to_wishlist(request, product_id):
    """Add product to wishlist"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    wishlist_item, created = Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )
    
    if created:
        messages.success(request, f'{product.name} added to your wishlist!')
        return JsonResponse({'status': 'added', 'message': 'Added to wishlist'})
    else:
        messages.info(request, f'{product.name} is already in your wishlist.')
        return JsonResponse({'status': 'exists', 'message': 'Already in wishlist'})


@login_required
@require_POST
def remove_from_wishlist(request, product_id):
    """Remove product from wishlist"""
    product = get_object_or_404(Product, id=product_id)
    
    try:
        wishlist_item = Wishlist.objects.get(user=request.user, product=product)
        wishlist_item.delete()
        messages.success(request, f'{product.name} removed from your wishlist.')
        return JsonResponse({'status': 'removed', 'message': 'Removed from wishlist'})
    except Wishlist.DoesNotExist:
        return JsonResponse({'status': 'not_found', 'message': 'Item not in wishlist'})


@login_required
@require_POST
def toggle_wishlist(request, product_id):
    """Toggle product in wishlist (add if not exists, remove if exists)"""
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    try:
        wishlist_item = Wishlist.objects.get(user=request.user, product=product)
        wishlist_item.delete()
        return JsonResponse({
            'status': 'removed',
            'message': 'Removed from wishlist',
            'in_wishlist': False
        })
    except Wishlist.DoesNotExist:
        Wishlist.objects.create(user=request.user, product=product)
        return JsonResponse({
            'status': 'added',
            'message': 'Added to wishlist',
            'in_wishlist': True
        })
