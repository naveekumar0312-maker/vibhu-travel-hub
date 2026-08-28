# pyrefly: ignore [missing-import]
from django.shortcuts import render, redirect, get_object_or_404
# pyrefly: ignore [missing-import]
from django.contrib.auth.decorators import login_required
# pyrefly: ignore [missing-import]
from django.contrib import messages
# pyrefly: ignore [missing-import]
from django.db.models import Q
# pyrefly: ignore [missing-import]
from django.core.paginator import Paginator
from datetime import datetime, date, timedelta
from website.models import RoundTripBooking, Vehicle

@login_required(login_url='/management/login/')
def management_roundtrip_list(request):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    queryset = RoundTripBooking.objects.all()

    # Dynamic Summary Counts
    total_count = queryset.count()
    new_count = queryset.filter(status='New').count()
    confirmed_count = queryset.filter(status='Confirmed').count()
    assigned_count = queryset.filter(status='Assigned').count()
    in_progress_count = queryset.filter(status='In Progress').count()
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
            Q(destination__icontains=search_query) |
            Q(vehicle_type__icontains=search_query)
        )

    # Status Filter
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        queryset = queryset.filter(status=status_filter)

    # Date Filter
    date_filter = request.GET.get('date_filter', '').strip()
    today = date.today()
    if date_filter == 'today':
        queryset = queryset.filter(created_at__date=today)
    elif date_filter == 'this_week':
        start_week = today - timedelta(days=today.weekday())
        queryset = queryset.filter(created_at__date__gte=start_week)
    elif date_filter == 'this_month':
        queryset = queryset.filter(created_at__year=today.year, created_at__month=today.month)
    elif date_filter == 'custom' and request.GET.get('custom_date'):
        try:
            c_date = datetime.strptime(request.GET.get('custom_date'), '%Y-%m-%d').date()
            queryset = queryset.filter(created_at__date=c_date)
        except ValueError:
            pass

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

    context = {
        'page_obj': page_obj,
        'bookings': page_obj.object_list,
        'total_count': total_count,
        'new_count': new_count,
        'confirmed_count': confirmed_count,
        'assigned_count': assigned_count,
        'in_progress_count': in_progress_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'search_query': search_query,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'custom_date': request.GET.get('custom_date', ''),
        'sort_by': sort_by,
        'per_page': per_page,
    }
    return render(request, 'dashboard/roundtrip_bookings/list.html', context)


@login_required(login_url='/management/login/')
def management_roundtrip_create(request):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        mobile = request.POST.get('mobile', '').strip()
        pickup_city = request.POST.get('pickup_city', '').strip()
        destination = request.POST.get('destination', '').strip()
        pickup_date = request.POST.get('pickup_date')
        pickup_time = request.POST.get('pickup_time', '').strip()
        dropoff_date = request.POST.get('dropoff_date')
        dropoff_time = request.POST.get('dropoff_time', '').strip()
        vehicle_type = request.POST.get('vehicle_type', '').strip()
        passengers = request.POST.get('passengers', '').strip()
        comments = request.POST.get('comments', '').strip()
        status = request.POST.get('status', 'New')

        if not all([name, mobile, pickup_city, pickup_date, dropoff_date]):
            messages.error(request, "Please fill in all required fields marked with *.")
            return render(request, 'dashboard/roundtrip_bookings/create_edit.html', {
                'is_edit': False,
                'vehicles': vehicles,
                'statuses': RoundTripBooking.STATUS_CHOICES,
            })

        booking = RoundTripBooking.objects.create(
            name=name,
            email=email,
            mobile=mobile,
            pickup_city=pickup_city,
            destination=destination,
            pickup_date=pickup_date,
            pickup_time=pickup_time or '09:00 AM',
            dropoff_date=dropoff_date,
            dropoff_time=dropoff_time or '06:00 PM',
            vehicle_type=vehicle_type,
            passengers=passengers,
            comments=comments,
            status=status,
        )
        messages.success(request, f"Round Trip Booking #{booking.booking_id} created successfully!")
        return redirect('management_roundtrip_detail', pk=booking.pk)

    context = {
        'is_edit': False,
        'vehicles': vehicles,
        'statuses': RoundTripBooking.STATUS_CHOICES,
    }
    return render(request, 'dashboard/roundtrip_bookings/create_edit.html', context)


@login_required(login_url='/management/login/')
def management_roundtrip_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    booking = get_object_or_404(RoundTripBooking, pk=pk)
    vehicles = Vehicle.objects.filter(is_active=True).order_by('display_order')

    if request.method == 'POST':
        booking.name = request.POST.get('name', '').strip()
        booking.email = request.POST.get('email', '').strip()
        booking.mobile = request.POST.get('mobile', '').strip()
        booking.pickup_city = request.POST.get('pickup_city', '').strip()
        booking.destination = request.POST.get('destination', '').strip()
        if request.POST.get('pickup_date'):
            booking.pickup_date = request.POST.get('pickup_date')
        if request.POST.get('pickup_time'):
            booking.pickup_time = request.POST.get('pickup_time').strip()
        if request.POST.get('dropoff_date'):
            booking.dropoff_date = request.POST.get('dropoff_date')
        if request.POST.get('dropoff_time'):
            booking.dropoff_time = request.POST.get('dropoff_time').strip()
        booking.vehicle_type = request.POST.get('vehicle_type', '').strip()
        booking.passengers = request.POST.get('passengers', '').strip()
        booking.comments = request.POST.get('comments', '').strip()
        booking.status = request.POST.get('status', booking.status)
        booking.save()

        messages.success(request, f"Round Trip Booking #{booking.booking_id} updated successfully.")
        return redirect('management_roundtrip_detail', pk=booking.pk)

    context = {
        'is_edit': True,
        'booking': booking,
        'vehicles': vehicles,
        'statuses': RoundTripBooking.STATUS_CHOICES,
    }
    return render(request, 'dashboard/roundtrip_bookings/create_edit.html', context)


@login_required(login_url='/management/login/')
def management_roundtrip_detail(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    booking = get_object_or_404(RoundTripBooking, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [s[0] for s in RoundTripBooking.STATUS_CHOICES]:
            booking.status = new_status
            booking.save()
            messages.success(request, f"Booking status updated to '{new_status}'.")
            return redirect('management_roundtrip_detail', pk=booking.pk)

    context = {
        'booking': booking,
        'statuses': RoundTripBooking.STATUS_CHOICES,
    }
    return render(request, 'dashboard/roundtrip_bookings/detail.html', context)


@login_required(login_url='/management/login/')
def management_roundtrip_status(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    booking = get_object_or_404(RoundTripBooking, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in [s[0] for s in RoundTripBooking.STATUS_CHOICES]:
            booking.status = new_status
            booking.save()
            messages.success(request, f"Booking #{booking.booking_id} status updated to {new_status}.")

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or f'/management/round-trip/{pk}/'
    return redirect(next_url)


@login_required(login_url='/management/login/')
def management_roundtrip_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    booking = get_object_or_404(RoundTripBooking, pk=pk)
    if request.method == 'POST':
        booking_id = booking.booking_id
        booking.delete()
        messages.success(request, f"Round Trip Booking #{booking_id} has been deleted.")
        return redirect('management_roundtrip_list')

    return redirect('management_roundtrip_detail', pk=pk)
