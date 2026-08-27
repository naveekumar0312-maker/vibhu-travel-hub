from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime, date, timedelta
from website.models import HourlyRentalBooking, Vehicle, City

@login_required(login_url='/management/login/')
def management_hourly_booking_list(request):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    queryset = HourlyRentalBooking.objects.all()

    # Dynamic Summary Counts
    total_count = queryset.count()
    new_count = queryset.filter(status='New').count()
    contacted_count = queryset.filter(status='Contacted').count()
    confirmed_count = queryset.filter(status='Confirmed').count()
    completed_count = queryset.filter(status='Completed').count()
    cancelled_count = queryset.filter(status='Cancelled').count()

    # Search Query
    search_query = request.GET.get('search', '').strip()
    if search_query:
        queryset = queryset.filter(
            Q(name__icontains=search_query) |
            Q(mobile__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(pickup_city__icontains=search_query) |
            Q(vehicle_type__icontains=search_query) |
            Q(hours__icontains=search_query)
        )

    # Filters
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        queryset = queryset.filter(status=status_filter)

    city_filter = request.GET.get('city', '').strip()
    if city_filter:
        queryset = queryset.filter(pickup_city__iexact=city_filter)

    vehicle_filter = request.GET.get('vehicle', '').strip()
    if vehicle_filter:
        queryset = queryset.filter(vehicle_type__icontains=vehicle_filter)

    date_filter = request.GET.get('date_filter', '').strip()
    today = date.today()
    if date_filter == 'today':
        queryset = queryset.filter(created_at__date=today)
    elif date_filter == 'this_week':
        start_week = today - timedelta(days=today.weekday())
        queryset = queryset.filter(created_at__date__gte=start_week)
    elif date_filter == 'this_month':
        queryset = queryset.filter(created_at__year=today.year, created_at__month=today.month)

    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'oldest':
        queryset = queryset.order_by('created_at')
    elif sort_by == 'pickup_date':
        queryset = queryset.order_by('pickup_date')
    else:
        queryset = queryset.order_by('-created_at')

    # Pagination
    per_page = request.GET.get('per_page', '10')
    try:
        per_page = int(per_page)
    except ValueError:
        per_page = 10

    paginator = Paginator(queryset, per_page)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Filter dropdown options
    cities = City.objects.filter(is_active=True).values_list('name', flat=True)

    context = {
        'page_obj': page_obj,
        'bookings': page_obj.object_list,
        'total_count': total_count,
        'new_count': new_count,
        'contacted_count': contacted_count,
        'confirmed_count': confirmed_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'search_query': search_query,
        'status_filter': status_filter,
        'city_filter': city_filter,
        'vehicle_filter': vehicle_filter,
        'date_filter': date_filter,
        'sort_by': sort_by,
        'per_page': per_page,
        'cities': cities,
    }
    return render(request, 'dashboard/hourly_bookings/list.html', context)


@login_required(login_url='/management/login/')
def management_hourly_booking_create(request):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    cities = City.objects.filter(is_active=True)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        pickup_city = request.POST.get('pickup_city', '').strip()
        pickup_date = request.POST.get('pickup_date')
        pickup_time = request.POST.get('pickup_time', '').strip()
        vehicle_type = request.POST.get('vehicle_type', '').strip()
        hours = request.POST.get('hours', '').strip()
        comments = request.POST.get('comments', '').strip()
        status = request.POST.get('status', 'New')

        if not all([name, mobile, pickup_city, pickup_date, hours]):
            messages.error(request, "Please fill in all required fields marked with *.")
            return render(request, 'dashboard/hourly_bookings/create_edit.html', {
                'is_edit': False,
                'vehicles': vehicles,
                'cities': cities,
                'statuses': HourlyRentalBooking.STATUS_CHOICES,
            })

        booking = HourlyRentalBooking.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            pickup_city=pickup_city,
            pickup_date=pickup_date,
            pickup_time=pickup_time or '09:00 AM',
            vehicle_type=vehicle_type or 'Sedan / Hatchback',
            hours=hours if 'Hour' in hours else f"{hours} Hours",
            comments=comments,
            status=status,
        )
        messages.success(request, f"Hourly Rental Booking #{booking.booking_id} created successfully!")
        return redirect('management_hourly_booking_detail', pk=booking.pk)

    context = {
        'is_edit': False,
        'vehicles': vehicles,
        'cities': cities,
        'statuses': HourlyRentalBooking.STATUS_CHOICES,
    }
    return render(request, 'dashboard/hourly_bookings/create_edit.html', context)


@login_required(login_url='/management/login/')
def management_hourly_booking_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    booking = get_object_or_404(HourlyRentalBooking, pk=pk)
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')
    cities = City.objects.filter(is_active=True)

    if request.method == 'POST':
        booking.name = request.POST.get('name', '').strip()
        booking.email = request.POST.get('email', '').strip()
        booking.mobile = request.POST.get('mobile', '').strip()
        booking.pickup_city = request.POST.get('pickup_city', '').strip()
        if request.POST.get('pickup_date'):
            booking.pickup_date = request.POST.get('pickup_date')
        if request.POST.get('pickup_time'):
            booking.pickup_time = request.POST.get('pickup_time').strip()
        booking.vehicle_type = request.POST.get('vehicle_type', '').strip()
        booking.hours = request.POST.get('hours', '').strip()
        booking.comments = request.POST.get('comments', '').strip()
        booking.status = request.POST.get('status', booking.status)
        booking.save()

        messages.success(request, f"Hourly Rental Booking #{booking.booking_id} updated successfully.")
        return redirect('management_hourly_booking_detail', pk=booking.pk)

    context = {
        'is_edit': True,
        'booking': booking,
        'vehicles': vehicles,
        'cities': cities,
        'statuses': HourlyRentalBooking.STATUS_CHOICES,
    }
    return render(request, 'dashboard/hourly_bookings/create_edit.html', context)


@login_required(login_url='/management/login/')
def management_hourly_booking_detail(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    booking = get_object_or_404(HourlyRentalBooking, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [s[0] for s in HourlyRentalBooking.STATUS_CHOICES]:
            booking.status = new_status
            booking.save()
            messages.success(request, f"Booking status updated to '{new_status}'.")
            return redirect('management_hourly_booking_detail', pk=booking.pk)

    context = {
        'booking': booking,
        'statuses': HourlyRentalBooking.STATUS_CHOICES,
    }
    return render(request, 'dashboard/hourly_bookings/detail.html', context)


@login_required(login_url='/management/login/')
def management_hourly_booking_status(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    booking = get_object_or_404(HourlyRentalBooking, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [s[0] for s in HourlyRentalBooking.STATUS_CHOICES]:
            booking.status = new_status
            booking.save()
            messages.success(request, f"Booking #{booking.booking_id} status updated to {new_status}.")

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or f'/management/hourly-bookings/{pk}/'
    return redirect(next_url)


@login_required(login_url='/management/login/')
def management_hourly_booking_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    booking = get_object_or_404(HourlyRentalBooking, pk=pk)
    if request.method == 'POST':
        booking_id = booking.booking_id
        booking.delete()
        messages.success(request, f"Hourly Rental Booking #{booking_id} has been deleted.")
        return redirect('management_hourly_booking_list')

    return redirect('management_hourly_booking_detail', pk=pk)
