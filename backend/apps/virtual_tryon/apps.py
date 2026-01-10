from django.apps import AppConfig


class VirtualTryonConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.virtual_tryon'

    def ready(self):
        import apps.virtual_tryon.signals
    verbose_name = 'Virtual Try-On'
