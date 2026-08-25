# pyrefly: ignore [missing-import]
from django.shortcuts import render, redirect, get_object_or_404
# pyrefly: ignore [missing-import]
from django.contrib.auth.decorators import login_required
# pyrefly: ignore [missing-import]
from django.contrib import messages
# pyrefly: ignore [missing-import]
from django.core.paginator import Paginator
# pyrefly: ignore [missing-import]
from django.db.models import Q
from decimal import Decimal
from website.models import HourlyRentalFare, City

VEHICLE_TYPES = [
    "Sedan / Hatchback",
    "SUV / MUV",
    "Tempo Traveller",
    "Luxury Bus"
]

HOURS_OPTIONS = [(i, f"{i} Hour" if i == 1 else f"{i} Hours") for i in range(1, 13)]

@login_required(login_url='/management/login/')
def hourly_fare_list(request):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    queryset = HourlyRentalFare.objects.all()

    # Search
    search_query = request.GET.get('search', '').strip()
    if search_query:
        queryset = queryset.filter(
            Q(city__icontains=search_query) |
            Q(vehicle_type__icontains=search_query)
        )

    # City filter
    city_filter = request.GET.get('city', '').strip()
    if city_filter:
        queryset = queryset.filter(city=city_filter)

    # Vehicle filter
    vehicle_filter = request.GET.get('vehicle_type', '').strip()
    if vehicle_filter:
        queryset = queryset.filter(vehicle_type=vehicle_filter)

    # Status filter
    status_filter = request.GET.get('status', '').strip()
    if status_filter == 'active':
        queryset = queryset.filter(is_active=True)
    elif status_filter == 'inactive':
        queryset = queryset.filter(is_active=False)

    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all_cities = City.objects.filter(is_active=True).values_list('name', flat=True)

    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'city_filter': city_filter,
        'vehicle_filter': vehicle_filter,
        'status_filter': status_filter,
        'all_cities': all_cities,
        'vehicle_types': VEHICLE_TYPES,
    }
    return render(request, 'dashboard/hourly_fares/list.html', context)


@login_required(login_url='/management/login/')
def hourly_fare_create(request):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    if request.method == 'POST':
        city = request.POST.get('city', '').strip()
        vehicle_type = request.POST.get('vehicle_type', '').strip()
        hours = request.POST.get('hours', '').strip()
        base_fare = request.POST.get('base_fare', '').strip()
        free_km = request.POST.get('free_km', '').strip()
        extra_km_fare = request.POST.get('extra_km_fare', '0').strip()
        extra_minute_fare = request.POST.get('extra_minute_fare', '0').strip()
        is_active = request.POST.get('is_active') == 'on' or request.POST.get('is_active') == '1'

        if not all([city, vehicle_type, hours, base_fare, free_km]):
            messages.error(request, "Please fill in all required fields marked with *.")
            return render(request, 'dashboard/hourly_fares/form.html', {
                'cities': City.objects.filter(is_active=True),
                'vehicle_types': VEHICLE_TYPES,
                'is_edit': False,
            })

        try:
            hours_val = int(hours)
            base_fare_val = Decimal(base_fare)
            free_km_val = int(free_km)
            extra_km_val = Decimal(extra_km_fare or '0')
            extra_min_val = Decimal(extra_minute_fare or '0')

            if hours_val <= 0 or base_fare_val < 0 or free_km_val < 0 or extra_km_val < 0 or extra_min_val < 0:
                messages.error(request, "Fare values and hours must be non-negative numbers.")
                return render(request, 'dashboard/hourly_fares/form.html', {
                    'cities': City.objects.filter(is_active=True),
                    'vehicle_types': VEHICLE_TYPES,
                    'is_edit': False,
                })

            HourlyRentalFare.objects.create(
                city=city,
                vehicle_type=vehicle_type,
                hours=hours_val,
                base_fare=base_fare_val,
                free_km=free_km_val,
                extra_km_fare=extra_km_val,
                extra_minute_fare=extra_min_val,
                is_active=is_active
            )
            messages.success(request, f"Hourly Rental Fare for {city} ({vehicle_type} - {hours_val} Hrs) created successfully.")
            return redirect('management_hourly_fare_list')
        except (ValueError, Exception) as e:
            messages.error(request, f"Invalid numerical input: {str(e)}")

    context = {
        'cities': City.objects.filter(is_active=True),
        'vehicle_types': VEHICLE_TYPES,
        'hours_options': HOURS_OPTIONS,
        'is_edit': False,
    }
    return render(request, 'dashboard/hourly_fares/form.html', context)


@login_required(login_url='/management/login/')
def hourly_fare_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    fare = get_object_or_404(HourlyRentalFare, pk=pk)

    if request.method == 'POST':
        city = request.POST.get('city', '').strip()
        vehicle_type = request.POST.get('vehicle_type', '').strip()
        hours = request.POST.get('hours', '').strip()
        base_fare = request.POST.get('base_fare', '').strip()
        free_km = request.POST.get('free_km', '').strip()
        extra_km_fare = request.POST.get('extra_km_fare', '0').strip()
        extra_minute_fare = request.POST.get('extra_minute_fare', '0').strip()
        is_active = request.POST.get('is_active') == 'on' or request.POST.get('is_active') == '1'

        if not all([city, vehicle_type, hours, base_fare, free_km]):
            messages.error(request, "Please fill in all required fields marked with *.")
        else:
            try:
                hours_val = int(hours)
                base_fare_val = Decimal(base_fare)
                free_km_val = int(free_km)
                extra_km_val = Decimal(extra_km_fare or '0')
                extra_min_val = Decimal(extra_minute_fare or '0')

                if hours_val <= 0 or base_fare_val < 0 or free_km_val < 0 or extra_km_val < 0 or extra_min_val < 0:
                    messages.error(request, "Fare values and hours must be non-negative numbers.")
                else:
                    fare.city = city
                    fare.vehicle_type = vehicle_type
                    fare.hours = hours_val
                    fare.base_fare = base_fare_val
                    fare.free_km = free_km_val
                    fare.extra_km_fare = extra_km_val
                    fare.extra_minute_fare = extra_min_val
                    fare.is_active = is_active
                    fare.save()
                    messages.success(request, f"Hourly Rental Fare for {city} updated successfully.")
                    return redirect('management_hourly_fare_list')
            except (ValueError, Exception) as e:
                messages.error(request, f"Invalid numerical input: {str(e)}")

    context = {
        'fare': fare,
        'cities': City.objects.filter(is_active=True),
        'vehicle_types': VEHICLE_TYPES,
        'hours_options': HOURS_OPTIONS,
        'is_edit': True,
    }
    return render(request, 'dashboard/hourly_fares/form.html', context)


@login_required(login_url='/management/login/')
def hourly_fare_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    fare = get_object_or_404(HourlyRentalFare, pk=pk)
    if request.method == 'POST':
        fare.delete()
        messages.success(request, "Hourly Rental Fare deleted successfully.")

    return redirect('management_hourly_fare_list')
