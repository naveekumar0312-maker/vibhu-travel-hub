# pyrefly: ignore [missing-import]
from django.shortcuts import render, get_object_or_404, redirect
# pyrefly: ignore [missing-import]
from django.contrib.auth.decorators import login_required
# pyrefly: ignore [missing-import]
from django.core.paginator import Paginator
# pyrefly: ignore [missing-import]
from django.contrib import messages
from website.models import Enquiry
# pyrefly: ignore [missing-import]
from django.db.models import Q

@login_required(login_url='/admin/')
def enquiry_list(request):
    if not request.user.is_staff:
        return redirect('dashboard_login')
        
    query = request.GET.get('q', '')
    
    enquiries = Enquiry.objects.all().order_by('-created_at')
    
    if query:
        enquiries = enquiries.filter(
            Q(name__icontains=query) |
            Q(phone__icontains=query) |
            Q(email__icontains=query) |
            Q(pickup__icontains=query) |
            Q(drop__icontains=query)
        )

    paginator = Paginator(enquiries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'dashboard/enquiries/list.html', context)

@login_required(login_url='/admin/')
def enquiry_delete(request, pk):
    if not request.user.is_staff:
        return redirect('dashboard_login')
        
    if request.method == 'POST':
        enquiry = get_object_or_404(Enquiry, pk=pk)
        enquiry.delete()
        messages.success(request, 'Enquiry deleted successfully.')
    return redirect('dashboard_enquiries')
