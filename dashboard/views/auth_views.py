# pyrefly: ignore [missing-import]
from django.shortcuts import render, redirect
# pyrefly: ignore [missing-import]
from django.contrib.auth import authenticate, login, logout
# pyrefly: ignore [missing-import]
from django.contrib.auth.decorators import login_required
# pyrefly: ignore [missing-import]
from django.contrib import messages
# pyrefly: ignore [missing-import]
from django.db.models import Count
# pyrefly: ignore [missing-import]
from django.db.models.functions import TruncMonth
import datetime
import json
from website.models import Enquiry, Vehicle, NewsletterSubscriber

def dashboard_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('dashboard_home')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember = request.POST.get('remember')
        
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            if not remember:
                # Expire session on browser close
                request.session.set_expiry(0)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect('dashboard_home')
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, 'dashboard/login.html')

def dashboard_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('dashboard_login')

@login_required(login_url='dashboard_login')
def dashboard_home(request):
    if not request.user.is_staff:
        return redirect('dashboard_login')
    
    # Real metrics
    total_enquiries = Enquiry.objects.count()
    total_subscribers = NewsletterSubscriber.objects.count()
    total_vehicles = Vehicle.objects.filter(is_active=True).count()
    
    # Monthly Enquiries Chart (Current Year)
    current_year = datetime.date.today().year
    monthly_data = (
        Enquiry.objects.filter(created_at__year=current_year)
        .annotate(month=TruncMonth('created_at'))
        .values('month')
        .annotate(count=Count('id'))
        .order_by('month')
    )
    
    # Initialize array with 0 for all 12 months
    monthly_enquiries_array = [0] * 12
    for item in monthly_data:
        month_index = item['month'].month - 1
        monthly_enquiries_array[month_index] = item['count']
        
    # Destinations & Services Chart
    active_destinations = 3
    total_services = 6 # (Local Taxi, Bus Booking, Tempo Traveller, Outstation Tours, Pilgrimage Trips, Corporate Travel)
    
    # Recent Enquiries
    recent_enquiries = Enquiry.objects.all().order_by('-created_at')[:5]
    
    context = {
        'total_enquiries': total_enquiries,
        'total_subscribers': total_subscribers,
        'total_vehicles': total_vehicles,
        'monthly_enquiries': json.dumps(monthly_enquiries_array),
        'active_destinations': active_destinations,
        'total_services': total_services,
        'recent_enquiries': recent_enquiries,
    }
    return render(request, 'dashboard/index.html', context)
