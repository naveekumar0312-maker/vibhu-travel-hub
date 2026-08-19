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
        ac_type = request.POST.get('ac_type') or "AC"
        passengers = request.POST.get('seats') or 4
        price_val = request.POST.get('price') or request.POST.get('badge_text') or "Price on Request"
        badge_text = request.POST.get('badge_text') or request.POST.get('price') or ""
        short_description = request.POST.get('short_description', '')
        feature_tags = request.POST.get('features', '')
        left_features = request.POST.get('left_features', '')
        right_specifications = request.POST.get('right_specifications', '')
        display_order = request.POST.get('display_order') or 0
        is_active = request.POST.get('is_active') == 'on'
        
        # Tariff Fields
        day_rent = request.POST.get('day_rent') or None
        per_km_rate = request.POST.get('per_km_rate') or None
        flat_per_km_above_400 = request.POST.get('flat_per_km_above_400') or None
        driver_pay_above_400 = request.POST.get('driver_pay_above_400') or None
        kerala_permit = request.POST.get('kerala_permit') or None
        karnataka_permit = request.POST.get('karnataka_permit') or None
        above_400_applicable = request.POST.get('above_400_applicable') == 'on'
        
        # Handle Main Image
        image = request.FILES.get('image')

        # Generate slug
        slug = slugify(name)
        original_slug = slug
        counter = 1
        while Vehicle.objects.filter(slug=slug).exists():
            slug = f"{original_slug}-{counter}"
            counter += 1

        vehicle = Vehicle.objects.create(
            name=name,
            slug=slug,
            category=category,
            ac_type=ac_type,
            passengers=passengers,
            price=price_val,
            badge_text=badge_text,
            short_description=short_description,
            feature_tags=feature_tags,
            left_features=left_features,
            right_specifications=right_specifications,
            display_order=display_order,
            is_active=is_active,
            day_rent=day_rent,
            per_km_rate=per_km_rate,
            flat_per_km_above_400=flat_per_km_above_400,
            driver_pay_above_400=driver_pay_above_400,
            kerala_permit=kerala_permit,
            karnataka_permit=karnataka_permit,
            above_400_applicable=above_400_applicable
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
        vehicle.ac_type = request.POST.get('ac_type') or "AC"
        vehicle.passengers = request.POST.get('seats') or 4
        price_val = request.POST.get('price') or request.POST.get('badge_text') or "Price on Request"
        vehicle.price = price_val
        vehicle.badge_text = request.POST.get('badge_text') or price_val
        vehicle.short_description = request.POST.get('short_description', '')
        vehicle.feature_tags = request.POST.get('features', '')
        vehicle.left_features = request.POST.get('left_features', '')
        vehicle.right_specifications = request.POST.get('right_specifications', '')
        vehicle.display_order = request.POST.get('display_order') or 0
        vehicle.is_active = request.POST.get('is_active') == 'on'
        
        # Tariff Fields
        vehicle.day_rent = request.POST.get('day_rent') or None
        vehicle.per_km_rate = request.POST.get('per_km_rate') or None
        vehicle.flat_per_km_above_400 = request.POST.get('flat_per_km_above_400') or None
        vehicle.driver_pay_above_400 = request.POST.get('driver_pay_above_400') or None
        vehicle.kerala_permit = request.POST.get('kerala_permit') or None
        vehicle.karnataka_permit = request.POST.get('karnataka_permit') or None
        vehicle.above_400_applicable = request.POST.get('above_400_applicable') == 'on'
        
        # Handle Main Image update
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
