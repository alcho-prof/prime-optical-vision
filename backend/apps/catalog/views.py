from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Product
from apps.inquiries.forms import InquiryForm

def product_list(request):
    """
    Display all active products.
    Phase 1: No pagination, no advanced filtering.
    """
    products = Product.objects.filter(is_active=True).select_related('category')
    
    context = {
        'products': products,
    }
    return render(request, 'catalog/product_list.html', context)

def product_detail(request, slug):
    """
    Display full details for a single active product.
    Handles Inquiry Form submission.
    """
    product = get_object_or_404(Product, slug=slug, is_active=True)
    variants = product.variants.all()
    
    if request.method == 'POST':
        form = InquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save(commit=False)
            inquiry.product = product
            inquiry.save()
            
            # Send Email Notification
            subject = f"New Inquiry: {product.name}"
            message = (
                f"Customer: {inquiry.customer_name}\n"
                f"Phone: {inquiry.phone_number}\n"
                f"Product: {product.name}\n"
                f"Message: {inquiry.message}"
            )
            try:
                # In dev, this prints to console if backend is 'console'
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.DEFAULT_FROM_EMAIL], # Send to admin (self) for now
                    fail_silently=False,
                )
            except Exception as e:
                # Log error but don't crash user experience
                print(f"Email failed: {e}")
                
            return render(request, 'catalog/product_detail.html', {
                'product': product,
                'variants': variants,
                'success': True
            })
    else:
        form = InquiryForm()
    
    context = {
        'product': product,
        'variants': variants,
        'form': form,
    }
    return render(request, 'catalog/product_detail.html', context)
