# pyrefly: ignore [missing-import]
from django.shortcuts import render, redirect, get_object_or_404
# pyrefly: ignore [missing-import]
from django.contrib import messages
from dashboard.utils import admin_required
from website.models import CitySEO

@admin_required
def seo_list(request):
    cities = CitySEO.objects.all().order_by('city_name')
    context = {
        'cities': cities
    }
    return render(request, 'dashboard/seo/list.html', context)

@admin_required
def seo_edit(request, city_id):
    city_seo = get_object_or_404(CitySEO, pk=city_id)
    if request.method == 'POST':
        city_seo.meta_title = request.POST.get('meta_title', '').strip()
        city_seo.meta_description = request.POST.get('meta_description', '').strip()
        city_seo.primary_keywords = request.POST.get('primary_keywords', '').strip()
        city_seo.route_keywords = request.POST.get('route_keywords', '').strip()
        city_seo.airport_keywords = request.POST.get('airport_keywords', '').strip()
        city_seo.corporate_keywords = request.POST.get('corporate_keywords', '').strip()
        city_seo.wedding_event_keywords = request.POST.get('wedding_event_keywords', '').strip()
        city_seo.segment_keywords = request.POST.get('segment_keywords', '').strip()
        city_seo.seo_content = request.POST.get('seo_content', '').strip()
        city_seo.image_alt_text = request.POST.get('image_alt_text', '').strip()
        city_seo.save()
        messages.success(request, f"SEO settings for {city_seo.city_name} updated successfully.")
        return redirect('dashboard_seo')
        
    context = {
        'city_seo': city_seo
    }
    return render(request, 'dashboard/seo/edit.html', context)
