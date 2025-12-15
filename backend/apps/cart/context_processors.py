from .models import Cart

def cart_processor(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            # We access the related name 'cart' from the User model (OneToOne)
            # If cart doesn't exist, accessing request.user.cart would raise DoesNotExist
            # BUT we defined it as OneToOne. 
            # Safest is to try/except or use filter
            cart = getattr(request.user, 'cart', None)
            if cart:
                cart_count = cart.total_items
        except Exception:
            pass
            
    return {'cart_count': cart_count}
