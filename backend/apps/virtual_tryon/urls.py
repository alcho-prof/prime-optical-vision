from django.urls import path
from . import views

app_name = 'virtual_tryon'

urlpatterns = [
    path('', views.virtual_tryon_view, name='index'),
    path('product/<slug:slug>/', views.virtual_tryon_view, name='product'),
    path('api/save-photo/', views.save_tryon_photo, name='save_photo'),
    path('api/cache-face/', views.cache_face_data, name='cache_face'),
    path('api/variant/<int:variant_id>/', views.get_variant_overlay, name='variant_overlay'),
    path('api/models/', views.get_frames_models, name='frames_models'),
]
