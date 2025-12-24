from django.contrib import admin
from .models import TryOnSession, TryOnPhoto, FaceDetectionCache


@admin.register(TryOnSession)
class TryOnSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'user', 'created_at', 'photo_count']
    list_filter = ['created_at']
    search_fields = ['session_id', 'user__username', 'user__email']
    readonly_fields = ['session_id', 'created_at', 'updated_at']
    
    def photo_count(self, obj):
        return obj.photos.count()
    photo_count.short_description = 'Photos'


@admin.register(TryOnPhoto)
class TryOnPhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'variant', 'created_at', 'photo_thumbnail']
    list_filter = ['created_at']
    search_fields = ['session__session_id', 'variant__product__name']
    readonly_fields = ['created_at', 'photo_preview']
    
    def photo_thumbnail(self, obj):
        if obj.photo:
            return f'<img src="{obj.photo.url}" width="50" height="50" style="object-fit: cover;" />'
        return '-'
    photo_thumbnail.short_description = 'Thumbnail'
    photo_thumbnail.allow_tags = True
    
    def photo_preview(self, obj):
        if obj.photo:
            return f'<img src="{obj.photo.url}" width="300" style="max-width: 100%;" />'
        return '-'
    photo_preview.short_description = 'Photo Preview'
    photo_preview.allow_tags = True


@admin.register(FaceDetectionCache)
class FaceDetectionCacheAdmin(admin.ModelAdmin):
    list_display = ['id', 'session', 'created_at']
    list_filter = ['created_at']
    search_fields = ['session__session_id']
    readonly_fields = ['created_at', 'face_data_display']
    
    def face_data_display(self, obj):
        import json
        return f'<pre>{json.dumps(obj.face_data, indent=2)}</pre>'
    face_data_display.short_description = 'Face Data'
    face_data_display.allow_tags = True
