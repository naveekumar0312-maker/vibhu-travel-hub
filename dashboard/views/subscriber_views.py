# pyrefly: ignore [missing-import]
from django.shortcuts import render, redirect, get_object_or_404
# pyrefly: ignore [missing-import]
from django.contrib.auth.decorators import login_required
from website.models import NewsletterSubscriber
# pyrefly: ignore [missing-import]
from django.db.models import Q
# pyrefly: ignore [missing-import]
from django.contrib import messages

@login_required(login_url='dashboard_login')
def subscriber_list(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    
    subscribers = NewsletterSubscriber.objects.all()
    
    if query:
        subscribers = subscribers.filter(
            Q(name__icontains=query) | Q(email__icontains=query)
        )
        
    if status == 'active':
        subscribers = subscribers.filter(is_active=True)
    elif status == 'inactive':
        subscribers = subscribers.filter(is_active=False)
        
    return render(request, 'dashboard/subscribers/list.html', {
        'subscribers': subscribers,
        'query': query,
        'status': status
    })

@login_required(login_url='dashboard_login')
def subscriber_detail(request, sub_id):
    subscriber = get_object_or_404(NewsletterSubscriber, id=sub_id)
    return render(request, 'dashboard/subscribers/detail.html', {'subscriber': subscriber})

@login_required(login_url='dashboard_login')
def subscriber_toggle(request, sub_id):
    subscriber = get_object_or_404(NewsletterSubscriber, id=sub_id)
    subscriber.is_active = not subscriber.is_active
    subscriber.save()
    messages.success(request, f"Subscriber {subscriber.email} status updated.")
    return redirect('dashboard_subscribers')

@login_required(login_url='dashboard_login')
def subscriber_delete(request, sub_id):
    if request.method == 'POST':
        subscriber = get_object_or_404(NewsletterSubscriber, id=sub_id)
        subscriber.delete()
        messages.success(request, f"Subscriber deleted successfully.")
    return redirect('dashboard_subscribers')
