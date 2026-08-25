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
from website.models import PartnerEnquiry

@login_required(login_url='dashboard_login')
def partner_enquiry_list(request):
    if not request.user.is_staff:
        return redirect('dashboard_login')
        
    query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    vehicle_filter = request.GET.get('vehicle_type', '').strip()
    service_filter = request.GET.get('preferred_service', '').strip()
    
    enquiries = PartnerEnquiry.objects.all().order_by('-created_at')
    
    if query:
        enquiries = enquiries.filter(
            Q(full_name__icontains=query) |
            Q(mobile_number__icontains=query) |
            Q(email__icontains=query) |
            Q(city__icontains=query) |
            Q(vehicle_details__icontains=query)
        )

    if status_filter:
        enquiries = enquiries.filter(status=status_filter)

    if vehicle_filter:
        enquiries = enquiries.filter(vehicle_type=vehicle_filter)

    if service_filter:
        enquiries = enquiries.filter(preferred_service=service_filter)

    paginator = Paginator(enquiries, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    status_choices = [choice[0] for choice in PartnerEnquiry.STATUS_CHOICES]
    vehicle_choices = [choice[0] for choice in PartnerEnquiry.VEHICLE_CHOICES]
    service_choices = [choice[0] for choice in PartnerEnquiry.SERVICE_CHOICES]
    
    context = {
        'page_obj': page_obj,
        'query': query,
        'status_filter': status_filter,
        'vehicle_filter': vehicle_filter,
        'service_filter': service_filter,
        'status_choices': status_choices,
        'vehicle_choices': vehicle_choices,
        'service_choices': service_choices,
        'total_count': enquiries.count(),
    }
    return render(request, 'dashboard/partner_enquiries/list.html', context)


@login_required(login_url='dashboard_login')
def partner_enquiry_detail(request, pk):
    if not request.user.is_staff:
        return redirect('dashboard_login')

    enquiry = get_object_or_404(PartnerEnquiry, pk=pk)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        valid_statuses = [choice[0] for choice in PartnerEnquiry.STATUS_CHOICES]
        if new_status in valid_statuses:
            enquiry.status = new_status
            enquiry.save()
            messages.success(request, f"Partner enquiry status updated to '{new_status}'.")
            return redirect('partner_enquiry_detail', pk=pk)
        else:
            messages.error(request, "Invalid status choice selected.")

    status_choices = PartnerEnquiry.STATUS_CHOICES
    context = {
        'enquiry': enquiry,
        'status_choices': status_choices,
    }
    return render(request, 'dashboard/partner_enquiries/detail.html', context)


@login_required(login_url='dashboard_login')
def partner_enquiry_delete(request, pk):
    if not request.user.is_staff:
        return redirect('dashboard_login')
        
    if request.method == 'POST':
        enquiry = get_object_or_404(PartnerEnquiry, pk=pk)
        enquiry.delete()
        messages.success(request, 'Partner enquiry deleted successfully.')
    return redirect('partner_enquiries_list')
