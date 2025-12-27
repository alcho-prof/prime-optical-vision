from .hybrid_cart import HybridCart

def cart_processor(request):
    return {'cart': HybridCart(request)}
