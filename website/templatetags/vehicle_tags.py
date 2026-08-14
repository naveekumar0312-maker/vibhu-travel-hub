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
    
    vehicle_name = vehicle.name
    if vehicle.model_name and vehicle.model_name.strip():
        vehicle_name = f"{vehicle.name} ({vehicle.model_name.strip()})"
        
    passengers = vehicle.passengers if vehicle.passengers else 4

    msg = (
        "Hello Vibhu Travel Hub Team,\n\n"
        "I would like to enquire about booking this vehicle.\n\n"
        f"Vehicle: {vehicle_name}\n"
        f"Seating Capacity: {passengers} Passengers\n\n"
        "Please share the availability, pricing and booking details.\n\n"
        "Thank you,\n"
        "Vibhu Travel Hub"
    )
    
    encoded_msg = quote(msg)
    return f"https://wa.me/919655866660?text={encoded_msg}"

