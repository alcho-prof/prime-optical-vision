from django.urls import path
from . import views

app_name = 'prescriptions'

urlpatterns = [
    path('', views.prescription_list, name='list'),
    path('add/', views.prescription_create, name='add'),
    path('<int:pk>/edit/', views.prescription_edit, name='edit'),
    path('<int:pk>/delete/', views.prescription_delete, name='delete'),
]
