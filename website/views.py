from urllib.parse import quote
# pyrefly: ignore [missing-import]
from django.shortcuts import redirect, render
from .models import (
    Enquiry,
    Vehicle,
    OutstationRoute,
    PartnerEnquiry,
    FleetPartnerInquiry,
    City,
    OneWayFare,
    OneWayBooking,
    RoundTripBooking,
    BulkBooking,
    HourlyRentalBooking,
)
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
        pickup = request.POST.get("pickup", "")
        drop = request.POST.get("drop", "")
        destination = request.POST.get("destination", "")
        msg = request.POST.get("message", "") or request.POST.get("trip_details", "")

        enquiry = Enquiry.objects.create(
            name=request.POST.get("name", ""),
            phone=request.POST.get("phone", ""),
            email=request.POST.get("email", ""),
            pickup=pickup,
            drop=drop,
            destination=destination,
            travel_date=travel_date,
            message=msg,
        )

        message_text = f""" *Vibhu Travel Hub*

Name: {enquiry.name}
Phone: {enquiry.phone}
Pickup: {enquiry.pickup}
Destination: {enquiry.destination}
Travel Date: {enquiry.travel_date}

Message:
{enquiry.message}
"""

        whatsapp = f"https://wa.me/919655866660?text={quote(message_text)}"
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

from .models import Enquiry, Vehicle, OutstationRoute, CitySEO
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
    place_data = get_place_seo_data(place_slug)
    if not place_data.get('state_slug'):
        place_data['state_slug'] = state_slug
    if not place_data.get('city_slug'):
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
        
    return JsonResponse({"status": "error", "message": "Invalid request."})


def fleet_partner_view(request):
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    return render(request, "website/fleet_partner.html", {
        "vehicles": vehicles,
    })


def api_submit_fleet_partner(request):
    if request.method == "POST":
        from .models import PartnerEnquiry, FleetPartnerInquiry
        try:
            full_name = (request.POST.get('full_name') or request.POST.get('name') or '').strip()
            mobile_number = (request.POST.get('mobile_number') or request.POST.get('mobile') or '').strip()
            email = request.POST.get('email', '').strip()
            city = request.POST.get('city', '').strip()
            vehicle_type = request.POST.get('vehicle_type', '').strip()
            vehicle_count = request.POST.get('vehicle_count', '').strip()
            vehicle_details = request.POST.get('vehicle_details', '').strip()
            preferred_service = (request.POST.get('preferred_service') or request.POST.get('service_type') or '').strip()
            message = request.POST.get('message', '').strip()

            # Backend Validation
            if not all([full_name, mobile_number, city, vehicle_type, vehicle_count, preferred_service]):
                return JsonResponse({
                    'status': 'error',
                    'message': 'Please fill in all required fields marked with *.'
                }, status=400)

            # Create PartnerEnquiry
            partner_enquiry = PartnerEnquiry.objects.create(
                full_name=full_name,
                mobile_number=mobile_number,
                email=email,
                city=city,
                vehicle_type=vehicle_type,
                vehicle_count=vehicle_count,
                vehicle_details=vehicle_details,
                preferred_service=preferred_service,
                message=message,
                status="New",
            )

            # Also create FleetPartnerInquiry for backward compatibility
            try:
                FleetPartnerInquiry.objects.create(
                    name=full_name,
                    mobile=mobile_number,
                    email=email,
                    city=city,
                    vehicle_count=vehicle_count,
                    vehicle_type=vehicle_type,
                    service_type=preferred_service,
                    message=message,
                    status="New",
                )
            except Exception:
                pass

            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for your interest in partnering with Vibhu Travel Hub. Our team will contact you shortly.',
                'inquiry_id': str(partner_enquiry.id),
            })
        except Exception:
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred while submitting your enquiry. Please try again.'
            }, status=500)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=405)


def book_cab(request):
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    if request.method == "POST":
        try:
            name = (request.POST.get('name') or request.POST.get('full_name') or '').strip()
            phone = (request.POST.get('phone') or request.POST.get('mobile_number') or '').strip()
            email = request.POST.get('email', '').strip()
            pickup = request.POST.get('pickup', '').strip()
            drop = request.POST.get('drop', '').strip()
            travel_date = request.POST.get('travel_date')
            travel_time = request.POST.get('travel_time', '').strip()
            vehicle_type = request.POST.get('vehicle_type', '').strip()
            passengers = request.POST.get('passengers', '').strip()
            trip_type = request.POST.get('trip_type', '').strip()
            message = request.POST.get('message', '').strip()

            if not all([name, phone, pickup, drop, travel_date, vehicle_type]):
                return JsonResponse({'status': 'error', 'message': 'Please fill in all required fields marked with *.'}, status=400)

            details_parts = []
            if trip_type: details_parts.append(f"Trip Type: {trip_type}")
            if vehicle_type: details_parts.append(f"Vehicle: {vehicle_type}")
            if passengers: details_parts.append(f"Passengers: {passengers}")
            if travel_time: details_parts.append(f"Time: {travel_time}")
            if message: details_parts.append(f"Notes: {message}")

            details_str = " | ".join(details_parts)

            enquiry = Enquiry.objects.create(
                name=name,
                phone=phone,
                email=email,
                pickup=pickup,
                drop=drop,
                destination=drop,
                travel_date=travel_date,
                message=details_str,
            )

            return JsonResponse({
                'status': 'success',
                'message': 'Thank you! Your cab booking request has been submitted successfully. Our team will contact you shortly.',
                'booking_id': str(enquiry.id),
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Server Error: {str(e)}'}, status=500)

    return render(request, "website/book_cab.html", {'vehicles': vehicles})


def book_cab_one_way(request):
    import json
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    cities = City.objects.filter(is_active=True).order_by('name')
    fares = OneWayFare.objects.filter(is_active=True).order_by('from_city', 'to_city')

    origin_order = ['Coimbatore', 'Trichy', 'Karur', 'Tirupur', 'Salem', 'Erode']
    fares_by_from_city = {}
    fare_lookup = {}
    for fare_item in fares:
        from_c = fare_item.from_city.strip()
        fares_by_from_city.setdefault(from_c, []).append(fare_item)
        key = f"{from_c.lower()}___{fare_item.to_city.strip().lower()}"
        fare_lookup[key] = float(fare_item.fare)

    # Reorder according to specified origins list
    ordered_fares_by_city = []
    for origin in origin_order:
        matching_fares = fares_by_from_city.get(origin, [])
        ordered_fares_by_city.append({
            'origin': origin,
            'fares': matching_fares
        })

    if request.method == "POST":
        try:
            name = (request.POST.get('name') or request.POST.get('full_name') or '').strip()
            email = request.POST.get('email', '').strip()
            mobile = (request.POST.get('mobile') or request.POST.get('mobile_number') or request.POST.get('phone') or '').strip()
            pickup_date = request.POST.get('pickup_date') or request.POST.get('travel_date')
            pickup_time = (request.POST.get('pickup_time') or request.POST.get('travel_time') or '').strip()
            pickup_city = (request.POST.get('pickup_city') or request.POST.get('pickup') or '').strip()
            drop_city = (request.POST.get('drop_off_city') or request.POST.get('drop_city') or request.POST.get('drop') or '').strip()
            comments = (request.POST.get('comments') or request.POST.get('message') or '').strip()

            if not all([name, email, mobile, pickup_date, pickup_time, pickup_city, drop_city]):
                return JsonResponse({'status': 'error', 'message': 'Please fill in all required fields marked with *.'}, status=400)

            # Create OneWayBooking
            booking = OneWayBooking.objects.create(
                name=name,
                email=email,
                mobile=mobile,
                pickup_date=pickup_date,
                pickup_time=pickup_time,
                pickup_city=pickup_city,
                drop_city=drop_city,
                comments=comments,
                status="New"
            )

            # Create compatibility Enquiry
            try:
                Enquiry.objects.create(
                    name=name,
                    phone=mobile,
                    email=email,
                    pickup=pickup_city,
                    drop=drop_city,
                    destination=drop_city,
                    travel_date=pickup_date,
                    message=f"One Way Cab Booking | Time: {pickup_time} | Comments: {comments}",
                    status="New"
                )
            except Exception:
                pass

            return JsonResponse({
                'status': 'success',
                'title': 'Your one-way cab booking request has been received.',
                'message': 'Thank you for choosing Vibhu Travel Hub. Our team will contact you shortly.',
                'booking_id': str(booking.id)
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Server Error: {str(e)}'}, status=500)

    context = {
        'vehicles': vehicles,
        'cities': cities,
        'fares': fares,
        'ordered_fares_by_city': ordered_fares_by_city,
        'fare_lookup_json': json.dumps(fare_lookup),
    }
    return render(request, "book_cab/one_way.html", context)




def book_cab_round_trip(request):
    from .models import RoundTripBooking, RoundTripFare, City, Enquiry, Vehicle
    from datetime import datetime

    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    cities = City.objects.filter(is_active=True).order_by('name')

    # Seed initial RoundTripFare data if table is empty
    if not RoundTripFare.objects.exists():
        initial_fares = [
            # Coimbatore
            ("Coimbatore", "Ooty-Coonoor-Kotagiri", "250Km", "18Hrs", "Rs.4525/-*", "Rs.4275/-*", 1),
            ("Coimbatore", "Kodaikanal", "350Km", "24Hrs", "Rs.6250/-*", "Rs.5850/-*", 2),
            ("Coimbatore", "Munnar", "320Km", "24Hrs", "Rs.5800/-*", "Rs.5400/-*", 3),
            ("Coimbatore", "Madurai", "440Km", "24Hrs", "Rs.7200/-*", "Rs.6800/-*", 4),
            ("Coimbatore", "Mysore-Bangalore", "700Km", "48Hrs", "Rs.11500/-*", "Rs.10800/-*", 5),
            # Chennai
            ("Chennai", "Pondicherry", "320Km", "24Hrs", "Rs.5200/-*", "Rs.4800/-*", 1),
            ("Chennai", "Tirupati", "300Km", "24Hrs", "Rs.4900/-*", "Rs.4500/-*", 2),
            ("Chennai", "Mahabalipuram", "120Km", "12Hrs", "Rs.2800/-*", "Rs.2500/-*", 3),
            ("Chennai", "Vellore", "280Km", "18Hrs", "Rs.4500/-*", "Rs.4200/-*", 4),
            # Trichy
            ("Trichy", "Tanjore-Kumbakonam", "200Km", "18Hrs", "Rs.3800/-*", "Rs.3500/-*", 1),
            ("Trichy", "Velankanni", "300Km", "24Hrs", "Rs.4900/-*", "Rs.4600/-*", 2),
            ("Trichy", "Rameswaram", "480Km", "36Hrs", "Rs.7800/-*", "Rs.7200/-*", 3),
            # Madurai
            ("Madurai", "Rameswaram-Dhanushkodi", "360Km", "24Hrs", "Rs.5900/-*", "Rs.5500/-*", 1),
            ("Madurai", "Kanyakumari", "490Km", "36Hrs", "Rs.7900/-*", "Rs.7300/-*", 2),
            ("Madurai", "Kodaikanal", "240Km", "18Hrs", "Rs.4400/-*", "Rs.4100/-*", 3),
            # Erode
            ("Erode", "Yercaud", "220Km", "18Hrs", "Rs.3900/-*", "Rs.3600/-*", 1),
            ("Erode", "Ooty", "300Km", "24Hrs", "Rs.4900/-*", "Rs.4500/-*", 2),
            ("Erode", "Coimbatore", "200Km", "12Hrs", "Rs.3200/-*", "Rs.2900/-*", 3),
            # Salem
            ("Salem", "Yercaud-Hogenakkal", "260Km", "18Hrs", "Rs.4300/-*", "Rs.3900/-*", 1),
            ("Salem", "Bangalore", "420Km", "24Hrs", "Rs.6800/-*", "Rs.6300/-*", 2),
            ("Salem", "Ooty", "440Km", "36Hrs", "Rs.7200/-*", "Rs.6700/-*", 3),
            # Tirupur
            ("Tirupur", "Valparai-Topslip", "280Km", "24Hrs", "Rs.4800/-*", "Rs.4400/-*", 1),
            ("Tirupur", "Ooty-Coonoor", "280Km", "24Hrs", "Rs.4800/-*", "Rs.4400/-*", 2),
            ("Tirupur", "Kodaikanal", "340Km", "24Hrs", "Rs.5900/-*", "Rs.5500/-*", 3),
            # Pollachi
            ("Pollachi", "Topslip-Parambikulam", "160Km", "14Hrs", "Rs.3200/-*", "Rs.2900/-*", 1),
            ("Pollachi", "Valparai-Athirapally", "280Km", "24Hrs", "Rs.4900/-*", "Rs.4500/-*", 2),
            ("Pollachi", "Munnar", "240Km", "18Hrs", "Rs.4300/-*", "Rs.3900/-*", 3),
            # Karur
            ("Karur", "Namakkal-Kolli Hills", "220Km", "18Hrs", "Rs.3900/-*", "Rs.3600/-*", 1),
            ("Karur", "Madurai", "300Km", "24Hrs", "Rs.4900/-*", "Rs.4500/-*", 2),
            ("Karur", "Kodaikanal", "360Km", "24Hrs", "Rs.6000/-*", "Rs.5600/-*", 3),
            # Tirunelveli
            ("Tirunelveli", "Courtallam-Tenkasi", "180Km", "14Hrs", "Rs.3400/-*", "Rs.3100/-*", 1),
            ("Tirunelveli", "Kanyakumari-Trivandrum", "320Km", "24Hrs", "Rs.5400/-*", "Rs.4900/-*", 2),
            ("Tirunelveli", "Mundanthurai-Manimuthar", "160Km", "12Hrs", "Rs.3100/-*", "Rs.2800/-*", 3),
        ]
        for f_city, pl, dist, dur, sed, mini, ord_val in initial_fares:
            RoundTripFare.objects.create(
                from_city=f_city,
                place=pl,
                distance_km=dist,
                trip_duration=dur,
                sedan_fare=sed,
                mini_fare=mini,
                display_order=ord_val
            )

    origin_order = ['Coimbatore', 'Chennai', 'Trichy', 'Madurai', 'Erode', 'Salem', 'Tirupur', 'Pollachi', 'Karur', 'Tirunelveli']
    all_fares = RoundTripFare.objects.filter(is_active=True).order_by('from_city', 'display_order')
    
    fares_by_from_city = {}
    for fare_item in all_fares:
        from_c = fare_item.from_city.strip()
        fares_by_from_city.setdefault(from_c, []).append(fare_item)

    ordered_fares_by_city = []
    for origin in origin_order:
        matching_fares = fares_by_from_city.get(origin, [])
        ordered_fares_by_city.append({
            'origin': origin,
            'fares': matching_fares
        })

    if request.method == "POST":
        try:
            name = (request.POST.get('name') or request.POST.get('full_name') or '').strip()
            email = request.POST.get('email', '').strip()
            mobile = (request.POST.get('mobile') or request.POST.get('mobile_number') or request.POST.get('phone') or '').strip()
            pickup_city = (request.POST.get('pickup_city') or request.POST.get('pickup') or '').strip()
            pickup_date = request.POST.get('pickup_date') or request.POST.get('departure_date')
            pickup_time = (request.POST.get('pickup_time') or request.POST.get('departure_time') or '').strip()
            dropoff_date = request.POST.get('dropoff_date') or request.POST.get('drop_off_date') or request.POST.get('return_date')
            dropoff_time = (request.POST.get('dropoff_time') or request.POST.get('drop_off_time') or request.POST.get('return_time') or '').strip()
            destination = (request.POST.get('destination') or request.POST.get('destination_city') or request.POST.get('drop_off_city') or request.POST.get('place') or '').strip()
            vehicle_type = (request.POST.get('vehicle_type') or request.POST.get('car_type') or '').strip()
            passengers = (request.POST.get('passengers') or request.POST.get('persons') or '').strip()
            comments = (request.POST.get('comments') or request.POST.get('message') or '').strip()

            if not all([name, email, mobile, pickup_city, pickup_date, pickup_time, dropoff_date, dropoff_time]):
                return JsonResponse({'status': 'error', 'message': 'Please fill in all required fields marked with *.'}, status=400)

            # Date validation: dropoff_date cannot be earlier than pickup_date
            try:
                p_date_obj = datetime.strptime(pickup_date, '%Y-%m-%d').date()
                d_date_obj = datetime.strptime(dropoff_date, '%Y-%m-%d').date()
                if d_date_obj < p_date_obj:
                    return JsonResponse({'status': 'error', 'message': 'Drop-off date cannot be earlier than Pickup date.'}, status=400)
            except Exception:
                pass

            # Create RoundTripBooking
            booking = RoundTripBooking.objects.create(
                name=name,
                email=email,
                mobile=mobile,
                pickup_city=pickup_city,
                destination=destination,
                pickup_date=pickup_date,
                pickup_time=pickup_time,
                dropoff_date=dropoff_date,
                dropoff_time=dropoff_time,
                vehicle_type=vehicle_type,
                passengers=passengers,
                comments=comments,
                status="New"
            )

            # Compatibility Enquiry
            try:
                Enquiry.objects.create(
                    name=name,
                    phone=mobile,
                    email=email,
                    pickup=pickup_city,
                    drop=f"Round Trip ({pickup_city})",
                    destination=f"Round Trip ({pickup_city})",
                    travel_date=pickup_date,
                    message=f"Round Trip Cab Booking | Return: {dropoff_date} {dropoff_time} | Pick Time: {pickup_time} | Comments: {comments}",
                    status="New"
                )
            except Exception:
                pass

            return JsonResponse({
                'status': 'success',
                'title': 'Your round trip booking request has been received.',
                'message': 'Your round trip booking request has been submitted successfully. Our team will contact you shortly.',
                'booking_id': str(booking.id)
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Server Error: {str(e)}'}, status=500)

    context = {
        'vehicles': vehicles,
        'cities': cities,
        'ordered_fares_by_city': ordered_fares_by_city,
    }
    return render(request, "book_cab/round_trip.html", context)


def book_cab_hourly(request):
    from .models import HourlyRentalFare, City, Enquiry, Vehicle

    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')

    # Seed initial HourlyRentalFare dataset for 1 through 12 Hours if empty
    if not HourlyRentalFare.objects.exists():
        initial_fares = [
            # Coimbatore Sedan / Hatchback (1 to 12 Hours)
            ("Coimbatore", "Sedan / Hatchback", 1, 378.00, 10, 17.00, 2.00),
            ("Coimbatore", "Sedan / Hatchback", 2, 750.00, 20, 17.00, 2.00),
            ("Coimbatore", "Sedan / Hatchback", 3, 1100.00, 30, 17.00, 2.00),
            ("Coimbatore", "Sedan / Hatchback", 4, 1450.00, 40, 17.00, 2.00),
            ("Coimbatore", "Sedan / Hatchback", 5, 1800.00, 50, 17.00, 2.00),
            ("Coimbatore", "Sedan / Hatchback", 6, 2150.00, 60, 17.00, 2.00),
            ("Coimbatore", "Sedan / Hatchback", 7, 2500.00, 70, 17.00, 2.00),
            ("Coimbatore", "Sedan / Hatchback", 8, 2850.00, 80, 17.00, 2.00),
            ("Coimbatore", "Sedan / Hatchback", 9, 3200.00, 90, 17.00, 2.00),
            ("Coimbatore", "Sedan / Hatchback", 10, 3550.00, 100, 17.00, 2.00),
            ("Coimbatore", "Sedan / Hatchback", 11, 3900.00, 110, 17.00, 2.00),
            ("Coimbatore", "Sedan / Hatchback", 12, 4250.00, 120, 17.00, 2.00),

            # Coimbatore SUV / MUV (1 to 12 Hours)
            ("Coimbatore", "SUV / MUV", 1, 550.00, 10, 20.00, 3.00),
            ("Coimbatore", "SUV / MUV", 2, 1050.00, 20, 20.00, 3.00),
            ("Coimbatore", "SUV / MUV", 3, 1550.00, 30, 20.00, 3.00),
            ("Coimbatore", "SUV / MUV", 4, 2050.00, 40, 20.00, 3.00),
            ("Coimbatore", "SUV / MUV", 5, 2550.00, 50, 20.00, 3.00),
            ("Coimbatore", "SUV / MUV", 6, 3050.00, 60, 20.00, 3.00),
            ("Coimbatore", "SUV / MUV", 7, 3550.00, 70, 20.00, 3.00),
            ("Coimbatore", "SUV / MUV", 8, 4050.00, 80, 20.00, 3.00),
            ("Coimbatore", "SUV / MUV", 9, 4550.00, 90, 20.00, 3.00),
            ("Coimbatore", "SUV / MUV", 10, 5050.00, 100, 20.00, 3.00),
            ("Coimbatore", "SUV / MUV", 11, 5550.00, 110, 20.00, 3.00),
            ("Coimbatore", "SUV / MUV", 12, 6050.00, 120, 20.00, 3.00),

            # Chennai
            ("Chennai", "Sedan / Hatchback", 1, 450.00, 10, 18.00, 2.50),
            ("Chennai", "Sedan / Hatchback", 2, 850.00, 20, 18.00, 2.50),
            ("Chennai", "Sedan / Hatchback", 4, 1650.00, 40, 18.00, 2.50),
            ("Chennai", "Sedan / Hatchback", 8, 3150.00, 80, 18.00, 2.50),
            ("Chennai", "Sedan / Hatchback", 12, 4500.00, 120, 18.00, 2.50),

            # Trichy
            ("Trichy", "Sedan / Hatchback", 1, 350.00, 10, 16.00, 2.00),
            ("Trichy", "Sedan / Hatchback", 2, 700.00, 20, 16.00, 2.00),
            ("Trichy", "Sedan / Hatchback", 4, 1350.00, 40, 16.00, 2.00),
            ("Trichy", "Sedan / Hatchback", 8, 2500.00, 80, 16.00, 2.00),
            ("Trichy", "Sedan / Hatchback", 12, 3700.00, 120, 16.00, 2.00),

            # Madurai
            ("Madurai", "Sedan / Hatchback", 1, 370.00, 10, 17.00, 2.00),
            ("Madurai", "Sedan / Hatchback", 2, 720.00, 20, 17.00, 2.00),
            ("Madurai", "Sedan / Hatchback", 4, 1400.00, 40, 17.00, 2.00),
            ("Madurai", "Sedan / Hatchback", 8, 2650.00, 80, 17.00, 2.00),
            ("Madurai", "Sedan / Hatchback", 12, 3850.00, 120, 17.00, 2.00),
        ]
        for c, v, h, bf, fkm, ekm, emin in initial_fares:
            HourlyRentalFare.objects.create(
                city=c,
                vehicle_type=v,
                hours=h,
                base_fare=bf,
                free_km=fkm,
                extra_km_fare=ekm,
                extra_minute_fare=emin
            )

    if request.method == "POST":
        try:
            name = (request.POST.get('name') or request.POST.get('full_name') or '').strip()
            mobile = (request.POST.get('mobile') or request.POST.get('mobile_number') or request.POST.get('phone') or '').strip()
            email = request.POST.get('email', '').strip()
            pickup_city = (request.POST.get('pickup_city') or request.POST.get('pickup') or request.POST.get('city') or '').strip()
            pickup_date = request.POST.get('pickup_date') or request.POST.get('travel_date')
            pickup_time = (request.POST.get('pickup_time') or request.POST.get('start_time') or '').strip()
            hours_package = (request.POST.get('hours') or request.POST.get('rental_duration') or '').strip()
            vehicle_type = (request.POST.get('vehicle_type') or 'Sedan / Hatchback').strip()
            comments = (request.POST.get('comments') or request.POST.get('message') or '').strip()

            if not all([name, mobile, pickup_city, pickup_date, hours_package]):
                return JsonResponse({'status': 'error', 'message': 'Please fill in all required fields marked with *.'}, status=400)

            details_parts = [
                "Type: Hourly Cab Rental",
                f"City: {pickup_city}",
                f"Vehicle Type: {vehicle_type}",
                f"Duration: {hours_package} Hours",
            ]
            if pickup_time: details_parts.append(f"Start Time: {pickup_time}")
            if comments: details_parts.append(f"Notes: {comments}")

            booking = HourlyRentalBooking.objects.create(
                name=name,
                mobile=mobile,
                email=email,
                pickup_city=pickup_city,
                pickup_date=pickup_date,
                pickup_time=pickup_time or '09:00 AM',
                vehicle_type=vehicle_type,
                hours=f"{hours_package} Hours" if str(hours_package).isdigit() else str(hours_package),
                comments=comments,
                status="New"
            )

            # Compatibility Enquiry
            Enquiry.objects.create(
                name=name,
                phone=mobile,
                email=email,
                pickup=pickup_city,
                drop=f"Hourly Rental ({hours_package} Hrs - {vehicle_type})",
                destination=f"Hourly Rental ({hours_package} Hrs)",
                travel_date=pickup_date,
                message=" | ".join(details_parts),
                status="New"
            )

            return JsonResponse({
                'status': 'success',
                'title': 'Your Hourly Rental booking request has been received.',
                'message': 'Thank you! Your Hourly Cab Rental request has been submitted successfully. Our team will contact you shortly.',
                'booking_id': booking.booking_id
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Server Error: {str(e)}'}, status=500)

    # GET Filter parameters
    selected_city = request.GET.get('city', '').strip()
    selected_vehicle = request.GET.get('vehicle_type', '').strip()
    selected_hours = request.GET.get('hours', '').strip()
    filter_submitted = 'city' in request.GET or 'vehicle_type' in request.GET or 'hours' in request.GET

    filter_error = None
    if filter_submitted:
        if not selected_city or not selected_vehicle or not selected_hours:
            filter_error = "Please select City, Vehicle Type, and Hours to search hourly rental fares."

    fares_qs = HourlyRentalFare.objects.filter(is_active=True)

    if selected_city:
        fares_qs = fares_qs.filter(city__iexact=selected_city)
    if selected_vehicle:
        fares_qs = fares_qs.filter(vehicle_type__iexact=selected_vehicle)
    if selected_hours and selected_hours.isdigit():
        fares_qs = fares_qs.filter(hours=int(selected_hours))

    # Available Filter Dropdown Data
    active_cities_db = list(City.objects.filter(is_active=True).values_list('name', flat=True))
    fare_cities_db = list(HourlyRentalFare.objects.filter(is_active=True).values_list('city', flat=True).distinct())
    combined_cities = sorted(list(set(active_cities_db + fare_cities_db)))

    vehicle_categories = [
        "Sedan / Hatchback",
        "SUV / MUV",
        "Tempo Traveller",
        "Luxury Bus"
    ]

    hours_options = [(i, f"{i} Hour" if i == 1 else f"{i} Hours") for i in range(1, 13)]

    context = {
        'vehicles': vehicles,
        'fares': fares_qs,
        'cities': combined_cities,
        'vehicle_categories': vehicle_categories,
        'hours_options': hours_options,
        'selected_city': selected_city,
        'selected_vehicle': selected_vehicle,
        'selected_hours': selected_hours,
        'filter_error': filter_error,
        'filter_submitted': filter_submitted,
        'filtered_count': fares_qs.count(),
    }
    return render(request, "book_cab/hourly_rental.html", context)


def book_cab_bulk(request):
    from .models import BulkBooking, City, Enquiry, Vehicle

    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    cities = City.objects.filter(is_active=True).order_by('name')

    if request.method == "POST":
        try:
            name = (request.POST.get('name') or request.POST.get('full_name') or '').strip()
            email = request.POST.get('email', '').strip()
            mobile = (request.POST.get('mobile_number') or request.POST.get('mobile') or request.POST.get('phone') or '').strip()
            pickup_date = request.POST.get('pickup_date') or request.POST.get('travel_date')
            pickup_city = (request.POST.get('pickup_city') or request.POST.get('city') or request.POST.get('pickup') or '').strip()
            comments = (request.POST.get('comments') or request.POST.get('message') or '').strip()

            if not all([name, email, mobile, pickup_date, pickup_city]):
                return JsonResponse({'status': 'error', 'message': 'Please fill in all required fields marked with *.'}, status=400)

            # Create BulkBooking in database
            booking = BulkBooking.objects.create(
                name=name,
                email=email,
                mobile_number=mobile,
                pickup_date=pickup_date,
                pickup_city=pickup_city,
                comments=comments,
                status="New"
            )

            # Compatibility Enquiry
            try:
                Enquiry.objects.create(
                    name=name,
                    phone=mobile,
                    email=email,
                    pickup=pickup_city,
                    drop=f"Bulk Booking ({pickup_city})",
                    destination=f"Bulk Booking ({pickup_city})",
                    travel_date=pickup_date,
                    message=f"Bulk Booking Request | Date: {pickup_date} | City: {pickup_city} | Comments: {comments}",
                    status="New"
                )
            except Exception:
                pass

            return JsonResponse({
                'status': 'success',
                'title': 'Your bulk booking request has been received.',
                'message': 'Your bulk booking request has been submitted successfully. Our team will contact you shortly.',
                'booking_id': str(booking.id)
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': f'Server Error: {str(e)}'}, status=500)

    context = {
        'vehicles': vehicles,
        'cities': cities,
    }
    return render(request, "book_cab/bulk_booking.html", context)


# Aliases for backward compatibility
one_way_trip = book_cab_one_way
round_trip = book_cab_round_trip
hourly_rental = book_cab_hourly
bulk_booking = book_cab_bulk







