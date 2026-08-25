# pyrefly: ignore [missing-import]
from django.shortcuts import render, redirect, get_object_or_404
# pyrefly: ignore [missing-import]
from django.contrib.auth.decorators import login_required
# pyrefly: ignore [missing-import]
from django.contrib import messages
# pyrefly: ignore [missing-import]
from django.db.models import Q
from datetime import datetime, date, timedelta
from website.models import RoundTripBooking

@login_required(login_url='/management/login/')
def management_roundtrip_list(request):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    queryset = RoundTripBooking.objects.all()

    # Dynamic Summary Counts
    total_count = queryset.count()
    pending_count = queryset.filter(Q(status='Pending') | Q(status='New')).count()
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
            Q(pickup_city__icontains=search_query)
        )

    # Status Filter
    status_filter = request.GET.get('status', '').strip()
    if status_filter:
        if status_filter == 'Pending':
            queryset = queryset.filter(Q(status='Pending') | Q(status='New'))
        else:
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
    else:
        queryset = queryset.order_by('-created_at')

    context = {
        'bookings': queryset,
        'total_count': total_count,
        'pending_count': pending_count,
        'confirmed_count': confirmed_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'search_query': search_query,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'custom_date': request.GET.get('custom_date', ''),
        'sort_by': sort_by,
    }
    return render(request, 'dashboard/roundtrip_bookings/list.html', context)


@login_required(login_url='/management/login/')
def management_roundtrip_detail(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    booking = get_object_or_404(RoundTripBooking, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Confirmed', 'Completed', 'Cancelled']:
            booking.status = new_status
            booking.save()
            messages.success(request, f"Booking status updated to {new_status}.")
            return redirect('management_roundtrip_detail', pk=booking.pk)

    return render(request, 'dashboard/roundtrip_bookings/detail.html', {'booking': booking})


@login_required(login_url='/management/login/')
def management_roundtrip_status(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    booking = get_object_or_404(RoundTripBooking, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['Pending', 'Confirmed', 'Completed', 'Cancelled']:
            booking.status = new_status
            booking.save()
            messages.success(request, f"Booking status updated to {new_status}.")

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or f'/management/round-trip/{pk}/'
    return redirect(next_url)


@login_required(login_url='/management/login/')
def management_roundtrip_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    booking = get_object_or_404(RoundTripBooking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Round Trip Booking deleted successfully.")
        return redirect('management_roundtrip_list')

    return redirect('management_roundtrip_detail', pk=pk)
