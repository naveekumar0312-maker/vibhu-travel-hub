import time
# pyrefly: ignore [missing-import]
from django.conf import settings

def static_version(request):
    """
    Provides a STATIC_VERSION variable to templates for cache busting.
    In DEBUG mode, it uses the current timestamp to ensure the browser always gets the latest version.
    In production, it uses a fixed version (or timestamp of server start).
    """
    if settings.DEBUG:
        return {'STATIC_VERSION': int(time.time())}
    return {'STATIC_VERSION': getattr(settings, 'STATIC_VERSION', '1.0.0')}

def global_context(request):
    from .models import Vehicle
    
    # Get distinct vehicle categories (or you can just pass featured vehicles)
    # Using raw objects so we have access to images if needed
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    
    destinations_list = []
    
    return {
        'destinations': destinations_list,
        'services_list': vehicles,
    }
