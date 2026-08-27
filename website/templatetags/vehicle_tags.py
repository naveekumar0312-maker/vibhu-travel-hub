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
    
    vehicle_name = getattr(vehicle, 'name', 'Vehicle')
    if getattr(vehicle, 'model_name', None) and vehicle.model_name.strip():
        vehicle_name = f"{vehicle.name} ({vehicle.model_name.strip()})"
        
    vehicle_type = getattr(vehicle, 'category', 'Cab Rental') or 'Cab Rental'
    passengers = getattr(vehicle, 'passengers', '4')
    capacity_text = f"{passengers} Passengers" if str(passengers).isdigit() else str(passengers)

    msg = (
        "Hello Vibhu Travel Hub,\n\n"
        "I am interested in booking the following vehicle:\n\n"
        f"Vehicle: {vehicle_name}\n"
        f"Vehicle Type: {vehicle_type}\n"
        f"Seating Capacity: {capacity_text}\n\n"
        "I would like to know the availability and booking details.\n\n"
        "Please assist me with the booking.\n\n"
        "Thank you."
    )
    
    encoded_msg = quote(msg)
    return f"https://wa.me/919655866660?text={encoded_msg}"
