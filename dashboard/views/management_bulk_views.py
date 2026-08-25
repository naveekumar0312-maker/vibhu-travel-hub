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
from datetime import datetime, date, timedelta
from website.models import BulkBooking, City

@login_required(login_url='/management/login/')
def management_bulk_list(request):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    queryset = BulkBooking.objects.all()

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
            Q(mobile_number__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(pickup_city__icontains=search_query)
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

    # Sorting
    sort_by = request.GET.get('sort', 'newest')
    if sort_by == 'oldest':
        queryset = queryset.order_by('created_at')
    else:
        queryset = queryset.order_by('-created_at')

    paginator = Paginator(queryset, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'total_count': total_count,
        'new_count': new_count,
        'contacted_count': contacted_count,
        'confirmed_count': confirmed_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'search_query': search_query,
        'status_filter': status_filter,
        'date_filter': date_filter,
        'sort_by': sort_by,
    }
    return render(request, 'dashboard/bulk_bookings/list.html', context)


@login_required(login_url='/management/login/')
def management_bulk_detail(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    booking = get_object_or_404(BulkBooking, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['New', 'Contacted', 'Confirmed', 'Completed', 'Cancelled']:
            booking.status = new_status
            booking.save()
            messages.success(request, f"Bulk Booking status updated to {new_status}.")
            return redirect('management_bulk_detail', pk=booking.pk)

    return render(request, 'dashboard/bulk_bookings/detail.html', {'booking': booking})


@login_required(login_url='/management/login/')
def management_bulk_edit(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    booking = get_object_or_404(BulkBooking, pk=pk)

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        mobile_number = request.POST.get('mobile_number', '').strip()
        pickup_date = request.POST.get('pickup_date')
        pickup_city = request.POST.get('pickup_city', '').strip()
        comments = request.POST.get('comments', '').strip()
        status = request.POST.get('status', '').strip()

        if not all([name, email, mobile_number, pickup_date, pickup_city]):
            messages.error(request, "Please fill in all required fields marked with *.")
        else:
            booking.name = name
            booking.email = email
            booking.mobile_number = mobile_number
            booking.pickup_date = pickup_date
            booking.pickup_city = pickup_city
            booking.comments = comments
            if status in ['New', 'Contacted', 'Confirmed', 'Completed', 'Cancelled']:
                booking.status = status
            booking.save()
            messages.success(request, "Bulk Booking updated successfully.")
            return redirect('management_bulk_detail', pk=booking.pk)

    cities = City.objects.filter(is_active=True)
    return render(request, 'dashboard/bulk_bookings/form.html', {'booking': booking, 'cities': cities})


@login_required(login_url='/management/login/')
def management_bulk_status(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    booking = get_object_or_404(BulkBooking, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['New', 'Contacted', 'Confirmed', 'Completed', 'Cancelled']:
            booking.status = new_status
            booking.save()
            messages.success(request, f"Bulk Booking status updated to {new_status}.")

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or f'/management/bulk-bookings/{pk}/'
    return redirect(next_url)


@login_required(login_url='/management/login/')
def management_bulk_delete(request, pk):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')

    booking = get_object_or_404(BulkBooking, pk=pk)
    if request.method == 'POST':
        booking.delete()
        messages.success(request, "Bulk Booking deleted successfully.")
        return redirect('management_bulk_list')

    return redirect('management_bulk_detail', pk=pk)
