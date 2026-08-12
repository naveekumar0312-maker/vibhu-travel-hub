# pyrefly: ignore [missing-import]
from django import template
from website.models import Vehicle

register = template.Library()

@register.simple_tag
def get_active_vehicles():
    """
    Returns all active vehicles from the Fleet database,
    ordered by their defined display_order.
    """
    return Vehicle.objects.filter(is_active=True).order_by("display_order", "name")

@register.simple_tag
def get_whatsapp_url(vehicle):
    from urllib.parse import quote
    
    msg = "Hello Vibhu Travel Hub,\n\nI am interested in booking the following vehicle:\n\n"
    msg += f"Vehicle: {vehicle.name}\n"
    if vehicle.model_name:
        msg += f"Model: {vehicle.model_name}\n\n"
    else:
        msg += "\n"
        
    msg += "Please share the availability, rental pricing, and booking details for this vehicle.\n\nThank you."
    
    encoded_msg = quote(msg)
    return f"https://wa.me/919655866660?text={encoded_msg}"
