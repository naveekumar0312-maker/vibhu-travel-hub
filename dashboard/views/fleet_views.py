# pyrefly: ignore [missing-import]
from django.shortcuts import render, redirect, get_object_or_404
# pyrefly: ignore [missing-import]
from django.contrib import messages
# pyrefly: ignore [missing-import]
from django.core.paginator import Paginator
# pyrefly: ignore [missing-import]
from django.db.models import Q
# pyrefly: ignore [missing-import]
from django.utils.text import slugify
from dashboard.utils import admin_required
from website.models import Vehicle

@admin_required
def fleet_list(request):
    query = request.GET.get('q', '')
    vehicles = Vehicle.objects.all()

    if query:
        vehicles = vehicles.filter(
            Q(name__icontains=query) |
            Q(category__icontains=query)
        )

    paginator = Paginator(vehicles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'dashboard/fleet/list.html', context)

@admin_required
def fleet_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = request.POST.get('category')
        passengers = request.POST.get('seats')
        badge_text = request.POST.get('badge_text')
        short_description = request.POST.get('short_description')
        feature_tags = request.POST.get('features')
        display_order = request.POST.get('display_order') or 0
        is_active = request.POST.get('is_active') == 'on'
        
        # Handle Image
        image = request.FILES.get('image')

        # Generate slug
        slug = slugify(name)
        
        # Ensure unique slug
        original_slug = slug
        counter = 1
        while Vehicle.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        vehicle = Vehicle.objects.create(
            name=name,
            slug=slug,
            category=category,
            passengers=passengers,
            badge_text=badge_text,
            short_description=short_description,
            feature_tags=feature_tags,
            display_order=display_order,
            is_active=is_active
        )
        
        if image:
            vehicle.image = image
            vehicle.save()

        messages.success(request, f'Vehicle "{name}" created successfully!')
        return redirect('dashboard_fleet')

    return render(request, 'dashboard/fleet/form.html')

@admin_required
def fleet_edit(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)

    if request.method == 'POST':
        name = request.POST.get('name')
        
        if name != vehicle.name:
            slug = slugify(name)
            original_slug = slug
            counter = 1
            while Vehicle.objects.filter(slug=slug).exclude(id=vehicle_id).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            vehicle.slug = slug
            
        vehicle.name = name
        vehicle.category = request.POST.get('category')
        vehicle.passengers = request.POST.get('seats')
        vehicle.badge_text = request.POST.get('badge_text')
        vehicle.short_description = request.POST.get('short_description')
        vehicle.feature_tags = request.POST.get('features')
        vehicle.display_order = request.POST.get('display_order') or 0
        vehicle.is_active = request.POST.get('is_active') == 'on'
        
        # Handle Image
        if 'image' in request.FILES:
            vehicle.image = request.FILES['image']

        vehicle.save()
        messages.success(request, f'Vehicle "{vehicle.name}" updated successfully!')
        return redirect('dashboard_fleet')

    context = {
        'vehicle': vehicle,
    }
    return render(request, 'dashboard/fleet/form.html', context)

@admin_required
def fleet_delete(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    if request.method == 'POST':
        name = vehicle.name
        vehicle.delete()
        messages.success(request, f'Vehicle "{name}" deleted successfully.')
    return redirect('dashboard_fleet')
