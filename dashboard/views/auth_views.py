# pyrefly: ignore [missing-import]
from django.shortcuts import render, redirect
# pyrefly: ignore [missing-import]
from django.contrib.auth import authenticate, login, logout
# pyrefly: ignore [missing-import]
from django.contrib.auth.decorators import login_required
# pyrefly: ignore [missing-import]
from django.contrib import messages
# pyrefly: ignore [missing-import]
from django.db.models import Count, Q
# pyrefly: ignore [missing-import]
from django.db.models.functions import TruncMonth
import datetime
import json
from website.models import (
    Enquiry,
    Vehicle,
    NewsletterSubscriber,
    OneWayBooking,
    RoundTripBooking,
    BulkBooking,
    PartnerEnquiry,
    FleetPartnerInquiry,
)

def dashboard_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        next_url = request.GET.get('next') or request.POST.get('next') or 'dashboard_home'
        return redirect(next_url)
        
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        remember = request.POST.get('remember')
        next_url = request.POST.get('next') or 'dashboard_home'
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            if not remember:
                request.session.set_expiry(0)
            messages.success(request, f"Welcome back to Vibhu Management, {user.username}!")
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'dashboard/login.html', {'next': request.GET.get('next', '')})

def dashboard_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('dashboard_login')

@login_required(login_url='/management/login/')
def dashboard_home(request):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')
    
    # Counts
    oneway_count = OneWayBooking.objects.count()
    roundtrip_count = RoundTripBooking.objects.count()
    bulk_count = BulkBooking.objects.count()
    hourly_count = Enquiry.objects.filter(message__icontains='Hourly').count()
    general_enquiries_count = Enquiry.objects.exclude(Q(message__icontains='Hourly') | Q(message__icontains='Bulk')).count()
    partner_count = PartnerEnquiry.objects.count() + FleetPartnerInquiry.objects.count()
    
    total_bookings = oneway_count + roundtrip_count + bulk_count + hourly_count + general_enquiries_count

    # Pending & Completed
    oneway_pending = OneWayBooking.objects.filter(status__in=['New', 'Pending']).count()
    roundtrip_pending = RoundTripBooking.objects.filter(status__in=['New', 'Pending']).count()
    bulk_new = BulkBooking.objects.filter(status='New').count()
    partner_pending = PartnerEnquiry.objects.filter(status__in=['New', 'Pending']).count() + FleetPartnerInquiry.objects.filter(status__in=['New', 'Pending']).count()
    enquiry_pending = Enquiry.objects.filter(status__in=['New', 'Pending']).count()
    pending_count = oneway_pending + roundtrip_pending + bulk_new + partner_pending + enquiry_pending

    oneway_completed = OneWayBooking.objects.filter(status='Completed').count()
    roundtrip_completed = RoundTripBooking.objects.filter(status='Completed').count()
    bulk_completed = BulkBooking.objects.filter(status='Completed').count()
    partner_completed = PartnerEnquiry.objects.filter(status__in=['Converted', 'Approved', 'Completed']).count()
    enquiry_completed = Enquiry.objects.filter(status='Completed').count()
    completed_count = oneway_completed + roundtrip_completed + bulk_completed + partner_completed + enquiry_completed

    # Recent items across models
    recent_oneway = list(OneWayBooking.objects.all().order_by('-created_at')[:5])
    recent_roundtrip = list(RoundTripBooking.objects.all().order_by('-created_at')[:5])
    recent_bulk = list(BulkBooking.objects.all().order_by('-created_at')[:5])

    context = {
        'total_bookings': total_bookings,
        'oneway_count': oneway_count,
        'roundtrip_count': roundtrip_count,
        'bulk_count': bulk_count,
        'hourly_count': hourly_count,
        'partner_count': partner_count,
        'pending_count': pending_count,
        'completed_count': completed_count,
        'recent_oneway': recent_oneway,
        'recent_roundtrip': recent_roundtrip,
        'recent_bulk': recent_bulk,
    }
    return render(request, 'dashboard/index.html', context)
