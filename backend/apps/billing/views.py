from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
# import razorpay  # Skipped for now
from apps.orders.models import Order
from .models import Payment
import uuid

def process_payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # MOCK PAYMENT FLOW (Skipping Razorpay)
    # Generate a dummy transaction ID
    dummy_payment_id = f"mock_pay_{uuid.uuid4().hex[:10]}"
    dummy_order_id = f"mock_order_{uuid.uuid4().hex[:10]}"
    
    # Create Local Payment Record (Completed directly)
    Payment.objects.create(
        order=order,
        amount=order.total_amount,
        razorpay_order_id=dummy_order_id,
        razorpay_payment_id=dummy_payment_id,
        status='completed'
    )
    
    # Update Order Status
    order.status = 'confirmed'
    order.save()
    
    messages.success(request, "Payment Successful (Mock)!")
    return redirect('orders:success', order_id=order.id)

@csrf_exempt
def verify_payment(request):
    # This view is not used in the mock flow but kept for structure
    return redirect('cart:detail')
