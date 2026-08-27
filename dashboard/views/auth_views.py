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
    OneWayBooking,
    RoundTripBooking,
    BulkBooking,
    HourlyRentalBooking,
    PartnerEnquiry,
    FleetPartnerInquiry,
)

def dashboard_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard_home')
        
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            return redirect('dashboard_home')
        else:
            messages.error(request, "Invalid username or password. Staff access required.")
            
    return render(request, 'dashboard/login.html')

def dashboard_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('dashboard_login')

@login_required(login_url='/management/login/')
def dashboard_home(request):
    if not request.user.is_staff:
        messages.error(request, "Management access required.")
        return redirect('dashboard_login')
    
    # Counts across booking modules
    oneway_count = OneWayBooking.objects.count()
    roundtrip_count = RoundTripBooking.objects.count()
    bulk_count = BulkBooking.objects.count()
    hourly_count = HourlyRentalBooking.objects.count()
    enquiries_count = Enquiry.objects.count()
    partner_count = PartnerEnquiry.objects.count() + FleetPartnerInquiry.objects.count()
    vehicles_count = Vehicle.objects.filter(is_active=True).count()
    
    total_bookings = oneway_count + roundtrip_count + bulk_count + hourly_count

    # Status Breakdown
    oneway_pending = OneWayBooking.objects.filter(status__in=['New', 'Pending']).count()
    roundtrip_pending = RoundTripBooking.objects.filter(status__in=['New', 'Pending']).count()
    bulk_pending = BulkBooking.objects.filter(status__in=['New', 'Pending']).count()
    hourly_pending = HourlyRentalBooking.objects.filter(status__in=['New', 'Pending']).count()
    partner_pending = PartnerEnquiry.objects.filter(status__in=['New', 'Pending']).count() + FleetPartnerInquiry.objects.filter(status__in=['New', 'Pending']).count()
    enquiry_pending = Enquiry.objects.filter(status__in=['New', 'Pending']).count()
    pending_count = oneway_pending + roundtrip_pending + bulk_pending + hourly_pending + partner_pending + enquiry_pending

    oneway_completed = OneWayBooking.objects.filter(status='Completed').count()
    roundtrip_completed = RoundTripBooking.objects.filter(status='Completed').count()
    bulk_completed = BulkBooking.objects.filter(status='Completed').count()
    hourly_completed = HourlyRentalBooking.objects.filter(status='Completed').count()
    completed_count = oneway_completed + roundtrip_completed + bulk_completed + hourly_completed

    oneway_cancelled = OneWayBooking.objects.filter(status='Cancelled').count()
    roundtrip_cancelled = RoundTripBooking.objects.filter(status='Cancelled').count()
    bulk_cancelled = BulkBooking.objects.filter(status='Cancelled').count()
    hourly_cancelled = HourlyRentalBooking.objects.filter(status='Cancelled').count()
    cancelled_count = oneway_cancelled + roundtrip_cancelled + bulk_cancelled + hourly_cancelled

    # Unified Recent Bookings List
    recent_oneway = list(OneWayBooking.objects.all().order_by('-created_at')[:5])
    recent_roundtrip = list(RoundTripBooking.objects.all().order_by('-created_at')[:5])
    recent_hourly = list(HourlyRentalBooking.objects.all().order_by('-created_at')[:5])
    recent_bulk = list(BulkBooking.objects.all().order_by('-created_at')[:5])
    recent_enquiries = list(Enquiry.objects.all().order_by('-created_at')[:5])

    context = {
        'total_bookings': total_bookings,
        'oneway_count': oneway_count,
        'roundtrip_count': roundtrip_count,
        'bulk_count': bulk_count,
        'hourly_count': hourly_count,
        'enquiries_count': enquiries_count,
        'partner_count': partner_count,
        'vehicles_count': vehicles_count,
        'pending_count': pending_count,
        'completed_count': completed_count,
        'cancelled_count': cancelled_count,
        'recent_oneway': recent_oneway,
        'recent_roundtrip': recent_roundtrip,
        'recent_hourly': recent_hourly,
        'recent_bulk': recent_bulk,
        'recent_enquiries': recent_enquiries,
    }
    return render(request, 'dashboard/index.html', context)
