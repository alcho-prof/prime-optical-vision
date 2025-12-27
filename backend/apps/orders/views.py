from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order, OrderItem
from .forms import OrderCreateForm
from apps.cart.hybrid_cart import HybridCart

def checkout_view(request):
    cart = HybridCart(request)
    if len(cart) == 0:
        messages.warning(request, "Your cart is empty.")
        return redirect('cart:detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            
            order.total_amount = cart.get_total_price()
            order.payment_method = form.cleaned_data['payment_method']
            order.save()
            
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product_variant=item['product_variant'],
                    lens_type=item['lens'],
                    prescription=item['prescription'],
                    price=item['price'], # Unit price (Frame + Lens)
                    quantity=item['quantity']
                )
            
            # Clear the cart
            cart.clear()
            
            # Redirect based on payment method
            if order.payment_method == 'COD':
                # Cash on Delivery - Direct to success
                messages.success(request, f"Order #{order.id} placed successfully! Pay cash on delivery.")
                return redirect('orders:success', order_id=order.id)
            else:
                # Online Payment - Redirect to payment gateway
                messages.info(request, "Redirecting to payment gateway...")
                return redirect('billing:payment', order_id=order.id)
            
            
    else:
        # Pre-fill form if user is authenticated
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'full_name': f"{request.user.first_name} {request.user.last_name}".strip(),
                'email': request.user.email,
                'phone_number': request.user.phone_number
            }
        form = OrderCreateForm(initial=initial_data)

    return render(request, 'orders/checkout.html', {'cart': cart, 'form': form}) 


def order_success_view(request, order_id):
    return render(request, 'orders/success.html', {'order_id': order_id})
