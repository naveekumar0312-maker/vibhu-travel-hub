import json
from django.urls import reverse

def generate_keywords(base_name, location_name=""):
    """Generate dynamic keywords."""
    keywords = [
        base_name,
        f"{base_name} Tour Packages",
        "Travel",
        "Tourism",
        "Vibhu Travel Hub"
    ]
    if location_name:
        keywords.extend([
            location_name,
            f"{base_name} in {location_name}",
            f"Cab Rental {location_name}",
            f"Tempo Traveller {location_name}"
        ])
    else:
        keywords.extend([
            "Cab Rental",
            "Tempo Traveller"
        ])
    return ", ".join(keywords)

def get_seo_data(request, obj, obj_type):
    """
    Generate dynamic SEO data based on object type.
    obj_type choices: 'destination', 'city', 'service', 'place'
    """
    base_url = request.build_absolute_uri('/')[:-1]
    
    seo_data = {
        'title': '',
        'meta_description': '',
        'meta_keywords': '',
        'canonical_url': '',
        'og_title': '',
        'og_description': '',
        'og_image': '',
        'schema_breadcrumb': '',
        'schema_entity': '',
        'schema_faq': ''
    }
    
    # Defaults
    image_url = ''
    breadcrumbs = []
    
    if obj_type == 'destination':
        seo_data['title'] = f"{obj.name} Tour Packages | Vibhu Travel Hub"
        seo_data['canonical_url'] = base_url + reverse('destination_detail', kwargs={'destination_key': obj.destination_key})
        desc = obj.short_description or f"Explore the best {obj.name} tour packages with Vibhu Travel Hub."
        seo_data['meta_description'] = desc[:155]
        seo_data['meta_keywords'] = generate_keywords(obj.name)
        if obj.featured_image:
            image_url = base_url + obj.featured_image.url
        breadcrumbs = [
            {'name': 'Home', 'item': base_url},
            {'name': 'Destinations', 'item': base_url + '#'},
            {'name': obj.name, 'item': seo_data['canonical_url']}
        ]
        
        # Schema for Destination
        entity_schema = {
            "@context": "https://schema.org",
            "@type": "TouristDestination",
            "name": obj.name,
            "description": seo_data['meta_description'],
            "url": seo_data['canonical_url']
        }
        if image_url:
            entity_schema["image"] = image_url
        seo_data['schema_entity'] = json.dumps(entity_schema)
        
        # FAQ Schema if faqs exist
        faqs = obj.faqs.filter(status='Published')
        if faqs.exists():
            faq_schema = {
                "@context": "https://schema.org",
                "@type": "FAQPage",
                "mainEntity": []
            }
            for faq in faqs:
                faq_schema["mainEntity"].append({
                    "@type": "Question",
                    "name": faq.question,
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": faq.answer
                    }
                })
            seo_data['schema_faq'] = json.dumps(faq_schema)

    elif obj_type == 'city':
        seo_data['title'] = f"Cab Rental in {obj.name} | Vibhu Travel Hub"
        seo_data['canonical_url'] = base_url + reverse('city_detail', kwargs={'destination_key': obj.destination_key, 'city_slug': obj.slug})
        desc = obj.short_description or f"Premium Cab Rental and Travel Services in {obj.name}."
        seo_data['meta_description'] = desc[:155]
        seo_data['meta_keywords'] = generate_keywords(obj.name, obj.get_destination_key_display())
        if obj.featured_image:
            image_url = base_url + obj.featured_image.url
        breadcrumbs = [
            {'name': 'Home', 'item': base_url},
            {'name': 'Destinations', 'item': base_url + '#'},
            {'name': obj.get_destination_key_display(), 'item': base_url + reverse('destination_detail', kwargs={'destination_key': obj.destination_key})},
            {'name': obj.name, 'item': seo_data['canonical_url']}
        ]
        entity_schema = {
            "@context": "https://schema.org",
            "@type": "City",
            "name": obj.name,
            "description": seo_data['meta_description'],
            "url": seo_data['canonical_url']
        }
        if image_url:
            entity_schema["image"] = image_url
        seo_data['schema_entity'] = json.dumps(entity_schema)

    elif obj_type == 'service':
        seo_data['title'] = f"{obj.name} in {obj.city.name} | Vibhu Travel Hub"
        seo_data['canonical_url'] = base_url + reverse('service_detail', kwargs={'destination_key': obj.city.destination_key, 'city_slug': obj.city.slug, 'service_slug': obj.slug})
        desc = obj.short_description or f"Book {obj.name} in {obj.city.name} with Vibhu Travel Hub."
        seo_data['meta_description'] = desc[:155]
        seo_data['meta_keywords'] = generate_keywords(obj.name, obj.city.name)
        if obj.banner_image:
            image_url = base_url + obj.banner_image.url
        breadcrumbs = [
            {'name': 'Home', 'item': base_url},
            {'name': 'Destinations', 'item': base_url + '#'},
            {'name': obj.city.get_destination_key_display(), 'item': base_url + reverse('destination_detail', kwargs={'destination_key': obj.city.destination_key})},
            {'name': obj.city.name, 'item': base_url + reverse('city_detail', kwargs={'destination_key': obj.city.destination_key, 'city_slug': obj.city.slug})},
            {'name': obj.name, 'item': seo_data['canonical_url']}
        ]
        entity_schema = {
            "@context": "https://schema.org",
            "@type": "Service",
            "name": obj.name,
            "provider": {
                "@type": "Organization",
                "name": "Vibhu Travel Hub"
            },
            "description": seo_data['meta_description'],
            "url": seo_data['canonical_url']
        }
        seo_data['schema_entity'] = json.dumps(entity_schema)

    elif obj_type == 'place':
        seo_data['title'] = f"{obj.name} Travel Guide | Vibhu Travel Hub"
        seo_data['canonical_url'] = base_url + reverse('place_detail', kwargs={'destination_key': obj.city.destination_key, 'city_slug': obj.city.slug, 'service_slug': obj.slug})
        desc = obj.short_description or f"Discover {obj.name}, a must-visit place in {obj.city.name}."
        seo_data['meta_description'] = desc[:155]
        seo_data['meta_keywords'] = generate_keywords(obj.name, obj.city.name)
        if obj.featured_image:
            image_url = base_url + obj.featured_image.url
        breadcrumbs = [
            {'name': 'Home', 'item': base_url},
            {'name': 'Destinations', 'item': base_url + '#'},
            {'name': obj.city.get_destination_key_display(), 'item': base_url + reverse('destination_detail', kwargs={'destination_key': obj.city.destination_key})},
            {'name': obj.city.name, 'item': base_url + reverse('city_detail', kwargs={'destination_key': obj.city.destination_key, 'city_slug': obj.city.slug})},
            {'name': obj.name, 'item': seo_data['canonical_url']}
        ]
        entity_schema = {
            "@context": "https://schema.org",
            "@type": "TouristAttraction",
            "name": obj.name,
            "description": seo_data['meta_description'],
            "url": seo_data['canonical_url']
        }
        if image_url:
            entity_schema["image"] = image_url
        seo_data['schema_entity'] = json.dumps(entity_schema)

    # Common Meta setup
    seo_data['og_title'] = seo_data['title']
    seo_data['og_description'] = seo_data['meta_description']
    seo_data['og_url'] = seo_data['canonical_url']
    if image_url:
        seo_data['og_image'] = image_url



    # Breadcrumb Schema Builder
    if breadcrumbs:
        breadcrumb_schema = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": []
        }
        for index, bc in enumerate(breadcrumbs, start=1):
            breadcrumb_schema["itemListElement"].append({
                "@type": "ListItem",
                "position": index,
                "name": bc['name'],
                "item": bc['item']
            })
        seo_data['schema_breadcrumb'] = json.dumps(breadcrumb_schema)

    return seo_data
