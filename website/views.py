from urllib.parse import quote
# pyrefly: ignore [missing-import]
from django.shortcuts import redirect, render
from .models import Enquiry, Vehicle, OutstationRoute, NewsletterSubscriber
# pyrefly: ignore [missing-import]
from django.http import HttpResponse, JsonResponse
# pyrefly: ignore [missing-import]
from django.core.mail import send_mail
# pyrefly: ignore [missing-import]
from django.conf import settings



def home(request):
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    return render(request, "website/home.html", {'vehicles': vehicles})

def about(request):
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    return render(request, "website/about.html", {'vehicles': vehicles})

def contact(request):
    return render(request, "website/contact.html")

def send_enquiry(request):

    if request.method == "POST":

        travel_date = request.POST.get("travel_date")

        enquiry = Enquiry.objects.create(
            name=request.POST.get("name"),
            phone=request.POST.get("phone"),
            email=request.POST.get("email", ""),
            vehicle=request.POST.get("vehicle"),
            pickup=request.POST.get("pickup"),
            destination=request.POST.get("destination"),
            travel_date=travel_date,
            members=int(request.POST.get("members", 1)),
            trip_details=request.POST.get("trip_details"),
        )

        message = f""" *Vibhu Travel Hub*

Name: {enquiry.name}
Phone: {enquiry.phone}
Vehicle: {enquiry.vehicle}
Pickup: {enquiry.pickup}
Destination: {enquiry.destination}
Travel Date: {enquiry.travel_date}
Members: {enquiry.members}

Trip Details:
{enquiry.trip_details}
"""

        whatsapp = f"https://wa.me/919655866660?text={quote(message)}"

        return redirect(whatsapp)

    return redirect("home")

def local_taxi_service(request):
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    return render(request, "services/local_taxi_service.html", {'vehicles': vehicles})


def bus_booking(request):
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    return render(request, "services/bus_booking.html", {'vehicles': vehicles})


def tempo_traveller(request):
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    return render(request, "services/tempo_traveller.html", {'vehicles': vehicles})


def outstation_tours(request):
    routes = OutstationRoute.objects.filter(is_active=True).order_by('display_order')
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    return render(request, "services/outstation_tours.html", {"routes": routes, "vehicles": vehicles})


def pilgrimage_trips(request):
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    return render(request, "services/pilgrimage_trips.html", {'vehicles': vehicles})


def corporate_travel(request):
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    return render(request, "services/corporate_travel.html", {'vehicles': vehicles})



import os

def sitemap_xml(request):
    sitemap_path = os.path.join(settings.BASE_DIR, 'static', 'sitemap.xml')
    if os.path.exists(sitemap_path):
        with open(sitemap_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type="application/xml")
    return HttpResponse(status=404)

def robots_txt(request):
    robots_path = os.path.join(settings.BASE_DIR, 'static', 'robots.txt')
    if os.path.exists(robots_path):
        with open(robots_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return HttpResponse(content, content_type="text/plain")
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /dashboard/",
        "Sitemap: https://vibhutravelhub.com/sitemap.xml",
    ]
    return HttpResponse(
        "\n".join(lines),
        content_type="text/plain"
    )

def api_submit_enquiry(request):
    if request.method == "POST":
        # Check CSRF by relying on Django's csrf_protect (or just middleware)
        # But if we use AJAX, we might need a JsonResponse.
        # pyrefly: ignore [missing-import]
        from django.http import JsonResponse
        from .models import Enquiry
        
        try:
            full_name = request.POST.get('full_name')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email', '')
            state_destination = request.POST.get('state_destination', 'Tamil Nadu')
            tourist_place = request.POST.get('tourist_place', '')
            pickup_location = request.POST.get('pickup_location')
            drop_location = request.POST.get('drop_location')
            travel_date = request.POST.get('travel_date')
            message = request.POST.get('message', '')
            
            # Basic validation on server
            if not all([full_name, mobile, pickup_location, drop_location, travel_date]):
                return JsonResponse({'status': 'error', 'message': 'Please fill all required fields.'}, status=400)

            # Create the enquiry
            enquiry = Enquiry.objects.create(
                name=full_name,
                phone=mobile,
                email=email,
                destination=state_destination,
                tourist_place=tourist_place,
                pickup=pickup_location,
                drop=drop_location,
                travel_date=travel_date,
                message=message
            )
            
            # Format WhatsApp Message
            from datetime import datetime
            try:
                date_obj = datetime.strptime(travel_date, '%Y-%m-%d')
                formatted_date = date_obj.strftime('%d %B %Y')
            except:
                formatted_date = travel_date
                
            wa_text = f"Hello Vibhu Travel Hub,\n\nI would like to book a trip.\n\n"
            wa_text += f"Destination:\n{state_destination}\n\n"
            if tourist_place:
                wa_text += f"City:\n{tourist_place}\n\n"
            wa_text += f"Pickup:\n{pickup_location}\n\n"
            wa_text += f"Drop:\n{drop_location}\n\n"
            wa_text += f"Travel Date:\n{formatted_date}\n\n"
            wa_text += f"Name:\n{full_name}\n\n"
            wa_text += f"Phone:\n{mobile}\n\n"
            wa_text += "Please share the quotation and vehicle availability.\n\nThank you."

            return JsonResponse({
                'status': 'success', 
                'message': 'Enquiry saved successfully. Redirecting to WhatsApp...',
                'wa_text': wa_text,
                'enquiry_id': str(enquiry.id)
            })            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
            
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)

from .models import Enquiry, Vehicle, OutstationRoute, NewsletterSubscriber, CitySEO
from .seo_utils import STATES_SEO_DATA, CITIES_SEO_DATA, TOURIST_PLACES_SEO_DATA, get_place_seo_data
# pyrefly: ignore [missing-import]
from django.http import Http404


def get_city_seo_dict():
    """Helper to return dict of CitySEO by slug"""
    return {c.slug: c for c in CitySEO.objects.all()}


def tamil_nadu_view(request):
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    city_seo = get_city_seo_dict()
    state_data = STATES_SEO_DATA.get('tamil-nadu', {})
    return render(request, 'destinations/tamilnadu.html', {
        'vehicles': vehicles,
        'city_seo': city_seo,
        'state_data': state_data,
    })

def kerala_view(request):
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    city_seo = get_city_seo_dict()
    state_data = STATES_SEO_DATA.get('kerala', {})
    return render(request, 'destinations/kerala.html', {
        'vehicles': vehicles,
        'city_seo': city_seo,
        'state_data': state_data,
    })

def karnataka_view(request):
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    city_seo = get_city_seo_dict()
    state_data = STATES_SEO_DATA.get('karnataka', {})
    return render(request, 'destinations/karnataka.html', {
        'vehicles': vehicles,
        'city_seo': city_seo,
        'state_data': state_data,
    })

def city_detail_view(request, state_slug, city_slug):
    city_data = CITIES_SEO_DATA.get(city_slug)
    if not city_data or city_data.get('state_slug') != state_slug:
        raise Http404("City page not found")
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    return render(request, 'destinations/city_detail.html', {
        'city_data': city_data,
        'vehicles': vehicles,
    })

def tourist_place_detail_view(request, state_slug, city_slug, place_slug):
    place_data = TOURIST_PLACES_SEO_DATA.get(place_slug)
    if not place_data:
        place_data = get_place_seo_data(place_slug)
        place_data = dict(place_data)
        place_data['state_slug'] = state_slug
        place_data['city_slug'] = city_slug
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    return render(request, 'destinations/tourist_place_detail.html', {
        'place_data': place_data,
        'vehicles': vehicles,
    })

def airport_transfer_service(request):
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    return render(request, 'services/airport_transfer.html', {
        'vehicles': vehicles,
    })

def newsletter_subscribe(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip()

        if not name or not email:
            return JsonResponse({"status": "error", "message": "Name and email are required."})
        
        # Check if already subscribed
        if NewsletterSubscriber.objects.filter(email__iexact=email).exists():
            return JsonResponse({"status": "error", "message": "This email address is already subscribed."})
        
        # Create subscriber
        subscriber = NewsletterSubscriber.objects.create(name=name, email=email)
        
        # Send email to admin
        try:
            admin_email = getattr(settings, 'ADMIN_NOTIFICATION_EMAIL', settings.DEFAULT_FROM_EMAIL)
            send_mail(
                subject="New Newsletter Subscriber – Vibhu Travel Hub",
                message=f"Hello Admin,\n\nYou have received a new newsletter subscription.\n\nSubscriber Details\n------------------\nName: {name}\nEmail: {email}\nSubscribed At: {subscriber.subscribed_at.strftime('%d %B %Y, %I:%M %p')}\n\nPlease review the subscriber from the Vibhu Travel Hub Admin Dashboard.\n\nRegards,\nVibhu Travel Hub\nPremium Travel Services",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[admin_email],
                fail_silently=True
            )
        except Exception:
            pass
            
        # Send welcome email to subscriber
        try:
            send_mail(
                subject="Welcome to Vibhu Travel Hub",
                message=f"Hello {name},\n\nThank you for subscribing to Vibhu Travel Hub.\n\nYou are now connected with us and will receive updates about our latest travel services, destinations and offers.\n\nWe look forward to helping you plan your next journey.\n\nRegards,\nVibhu Travel Hub\nPremium Travel Services",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=True
            )
        except Exception:
            pass
            
        return JsonResponse({"status": "success", "message": "You have successfully subscribed to Vibhu Travel Hub. We'll keep you updated with our latest travel offers and updates."})
        
    return JsonResponse({"status": "error", "message": "Invalid request."})

