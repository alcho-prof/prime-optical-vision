from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
import uuid
import base64
import json

from apps.catalog.models import Product, ProductVariant
from .models import TryOnSession, TryOnPhoto, FaceDetectionCache, SpectacleFrame


def virtual_tryon_view(request, slug=None):
    """Main virtual try-on page"""
    product = None
    variants = []
    
    if slug:
        product = get_object_or_404(Product, slug=slug)
        variants = product.variants.all()
    else:
        # Show all products with try-on capability
        variants = ProductVariant.objects.filter(image__isnull=False)[:20]
    
    # Create or get session
    session_id = request.session.get('tryon_session_id')
    if not session_id:
        session_id = str(uuid.uuid4())
        request.session['tryon_session_id'] = session_id
        
        # Create session in database
        TryOnSession.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_id=session_id
        )
    
    context = {
        'product': product,
        'variants': variants,
        'session_id': session_id,
    }
    
    return render(request, 'virtual_tryon/tryon.html', context)


@csrf_exempt
@require_http_methods(["POST"])
def save_tryon_photo(request):
    """Save a photo from the virtual try-on session"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        variant_id = data.get('variant_id')
        photo_data = data.get('photo')  # Base64 encoded image
        
        # Get session
        session = get_object_or_404(TryOnSession, session_id=session_id)
        
        # Get variant
        variant = get_object_or_404(ProductVariant, id=variant_id)
        
        # Decode base64 image
        format, imgstr = photo_data.split(';base64,')
        ext = format.split('/')[-1]
        
        # Create photo
        photo = TryOnPhoto.objects.create(
            session=session,
            variant=variant
        )
        
        # Save image
        photo.photo.save(
            f'tryon_{session_id}_{variant_id}.{ext}',
            ContentFile(base64.b64decode(imgstr)),
            save=True
        )
        
        return JsonResponse({
            'success': True,
            'photo_id': photo.id,
            'photo_url': photo.photo.url
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@csrf_exempt
@require_http_methods(["POST"])
def cache_face_data(request):
    """Cache face detection data for performance"""
    try:
        data = json.loads(request.body)
        session_id = data.get('session_id')
        face_data = data.get('face_data')
        
        session = get_object_or_404(TryOnSession, session_id=session_id)
        
        # Create or update cache
        FaceDetectionCache.objects.update_or_create(
            session=session,
            defaults={'face_data': face_data}
        )
        
        return JsonResponse({'success': True})
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@require_http_methods(["GET"])
def get_variant_overlay(request, variant_id):
    """Get variant image data for overlay"""
    try:
        variant = get_object_or_404(ProductVariant, id=variant_id)
        
        return JsonResponse({
            'success': True,
            'variant_id': variant.id,
            'image_url': variant.image.url if variant.image else None,
            'product_name': variant.product.name,
            'color': variant.color_name,
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)


@require_http_methods(["GET"])
def get_frames_models(request):
    """Get list of available frames with 3D models and metadata"""
    try:
        frames = SpectacleFrame.objects.select_related('variant', 'variant__product').all()
        
        data = []
        for frame in frames:
            data.append({
                'id': frame.variant.id,
                'name': frame.variant.product.name,
                'color': frame.variant.color_name,
                'model_url': frame.model_file.url if frame.model_file else None,
                'thumbnail_url': frame.variant.image.url if frame.variant.image else None,
                'metadata': {
                    'scale': frame.scaling_factor,
                    'position': {
                        'x': frame.offset_x,
                        'y': frame.offset_y,
                        'z': frame.offset_z
                    },
                    'rotation': {
                        'x': frame.rotation_x,
                        'y': frame.rotation_y,
                        'z': frame.rotation_z
                    }
                }
            })
            
        return JsonResponse({
            'success': True,
            'frames': data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
