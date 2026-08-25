# pyrefly: ignore [missing-import]
from django.shortcuts import render, get_object_or_404, redirect
# pyrefly: ignore [missing-import]
from django.contrib.auth.decorators import login_required
# pyrefly: ignore [missing-import]
from django.core.paginator import Paginator
# pyrefly: ignore [missing-import]
from django.contrib import messages
# pyrefly: ignore [missing-import]
from django.db.models import Q
from website.models import OneWayBooking, OneWayFare, City

@login_required(login_url='dashboard_login')
def oneway_booking_list(request):
    if not request.user.is_staff:
        return redirect('dashboard_login')
        
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    
    bookings = OneWayBooking.objects.all().order_by('-created_at')
    
    if query:
        bookings = bookings.filter(
            Q(name__icontains=query) |
            Q(mobile__icontains=query) |
            Q(email__icontains=query) |
            Q(pickup_city__icontains=query) |
            Q(drop_city__icontains=query)
        )

    if status_filter:
        bookings = bookings.filter(status=status_filter)

    paginator = Paginator(bookings, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    status_choices = [choice[0] for choice in OneWayBooking.STATUS_CHOICES]
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
        'status_choices': status_choices,
        'total_count': bookings.count(),
    }
    return render(request, 'dashboard/oneway_bookings/list.html', context)


@login_required(login_url='dashboard_login')
def oneway_booking_detail(request, pk):
    if not request.user.is_staff:
        return redirect('dashboard_login')

    booking = get_object_or_404(OneWayBooking, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid_statuses = [choice[0] for choice in OneWayBooking.STATUS_CHOICES]
        if new_status in valid_statuses:
            booking.status = new_status
            booking.save()
            messages.success(request, f"One-way booking status updated to '{new_status}'.")
            return redirect('oneway_booking_detail', pk=pk)
        else:
            messages.error(request, "Invalid status choice selected.")

    status_choices = OneWayBooking.STATUS_CHOICES
    context = {
        'booking': booking,
        'status_choices': status_choices,
    }
    return render(request, 'dashboard/oneway_bookings/detail.html', context)


@login_required(login_url='dashboard_login')
def oneway_booking_delete(request, pk):
    if not request.user.is_staff:
        return redirect('dashboard_login')
        
    if request.method == 'POST':
        booking = get_object_or_404(OneWayBooking, pk=pk)
        booking.delete()
        messages.success(request, 'One way booking deleted successfully.')
    return redirect('oneway_booking_list')


@login_required(login_url='dashboard_login')
def oneway_fare_list(request):
    if not request.user.is_staff:
        return redirect('dashboard_login')

    if request.method == 'POST':
        action_type = request.POST.get('action_type')
        if action_type == 'add_fare':
            from_c = request.POST.get('from_city', '').strip()
            to_c = request.POST.get('to_city', '').strip()
            fare_val = request.POST.get('fare', '').strip()
            if from_c and to_c and fare_val:
                OneWayFare.objects.create(from_city=from_c, to_city=to_c, fare=fare_val, is_active=True)
                City.objects.get_or_create(name=from_c, defaults={'is_active': True})
                City.objects.get_or_create(name=to_c, defaults={'is_active': True})
                messages.success(request, f"Fare from {from_c} to {to_c} added successfully.")
        elif action_type == 'delete_fare':
            fare_id = request.POST.get('fare_id')
            fare_obj = get_object_or_404(OneWayFare, pk=fare_id)
            fare_obj.delete()
            messages.success(request, "Fare deleted successfully.")

        return redirect('oneway_fare_list')

    fares = OneWayFare.objects.all().order_by('from_city', 'to_city')
    cities = City.objects.all().order_by('name')

    context = {
        'fares': fares,
        'cities': cities,
    }
    return render(request, 'dashboard/oneway_bookings/fares.html', context)
