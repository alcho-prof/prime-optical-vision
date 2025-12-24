from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [
    path('payment/process/<int:order_id>/', views.process_payment, name='process_payment'),
    path('payment/verify/', views.verify_payment, name='verify_payment'),
]
