# pyrefly: ignore [missing-import]
from django.core.management.base import BaseCommand
from blog.models import BlogPost
# pyrefly: ignore [missing-import]
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Seed initial realistic travel blog posts for Vibhu Travel Hub'

    def handle(self, *args, **options):
        author = User.objects.first()
        
        sample_blogs = [
            {
                'title': 'Best Weekend Getaways from Coimbatore: Top 7 Scenic Destinations',
                'slug': 'best-weekend-getaways-from-coimbatore',
                'category': 'Destinations',
                'short_description': 'Discover breathtaking hill stations, serene lakes, and wildlife sanctuaries within 4 hours drive from Coimbatore.',
                'content': '''<h2>Escape the City Routine with Unforgettable Weekend Trips</h2>
<p>Coimbatore, known as the Manchester of South India, is perfectly situated near some of the most spectacular hill stations and nature reserves in the Western Ghats. Whether you are looking for a quick day trip or a 2-day weekend excursion with family or friends, Vibhu Travel Hub provides comfortable cabs and Tempo Travellers for hassle-free travel.</p>

<h3>1. Ooty & Coonoor — The Queen of Hill Stations</h3>
<p>Located just 85 km from Coimbatore, Ooty and Coonoor offer cool weather, tea plantations, and scenic viewpoints like Doddabetta Peak and Dolphin's Nose. Booking a round-trip cab allows you to enjoy the panoramic mountain roads without driving stress.</p>

<h3>2. Valparai & Topslip — Tea Estates & Wildlife</h3>
<p>For nature lovers, Valparai is a pristine hill station with 40 hairpin bends, lush tea gardens, and frequent sightings of Nilgiri Tahr and hornbills. Pair it with a visit to Topslip tiger reserve for an immersive rainforest experience.</p>

<h3>3. Kodaikanal — The Princess of Hill Stations</h3>
<p>A 170 km drive from Coimbatore brings you to Kodaikanal. Explore Kodai Lake, Coaker's Walk, and Pillar Rocks in complete comfort with our experienced outstation drivers.</p>

<h3>Why Book Outstation Cabs with Vibhu Travel Hub?</h3>
<ul>
    <li>Clean, sanitized sedans, SUVs, and luxury Tempo Travellers</li>
    <li>Experienced, courteous drivers who know local routes and sight-seeing spots</li>
    <li>Transparent per-km and flat-rate pricing with no hidden charges</li>
</ul>''',
                'reading_time': '5 min read',
                'is_featured': True,
                'is_published': True,
                'featured_image': 'blog/coimbatore-getaways.jpg'
            },
            {
                'title': 'Complete Guide to Planning a South India Road Trip',
                'slug': 'complete-guide-planning-south-india-road-trip',
                'category': 'Travel Guides',
                'short_description': 'Everything you need to know about routes, best travel seasons, vehicle selection, and essential road trip tips for South India.',
                'content': '''<h2>Planning the Ultimate South Indian Highway Adventure</h2>
<p>South India offers a diverse blend of coastal highways, mountain passes, temple heritage circuits, and backwater retreats. Planning a road trip across Tamil Nadu, Kerala, and Karnataka requires careful route selection and choosing the right mode of transport.</p>

<h3>Choosing the Right Travel Vehicle</h3>
<p>Depending on your group size, choosing between a Sedan, SUV, or Tempo Traveller is crucial:</p>
<ul>
    <li><strong>Sedans (Dzire, Etios):</strong> Ideal for couples or small families (up to 4 passengers) for intercity travel.</li>
    <li><strong>SUVs (Innova, Ertiga):</strong> Perfect for 6–7 passengers traveling with luggage on mountain routes.</li>
    <li><strong>Tempo Travellers (12–26 Seater):</strong> The ultimate choice for family reunions and corporate groups.</li>
</ul>

<h3>Popular Road Trip Routes</h3>
<p>1. <strong>Coimbatore → Munnar → Alleppey → Cochin:</strong> The best mountain to backwaters circuit.</p>
<p>2. <strong>Chennai → Pondicherry → Tanjore → Madurai:</strong> The rich cultural and coastal heritage tour.</p>''',
                'reading_time': '7 min read',
                'is_featured': False,
                'is_published': True,
                'featured_image': 'blog/south-india-road-trip.jpg'
            },
            {
                'title': 'Cab vs Tempo Traveller: Which One Should You Choose for Group Travel?',
                'slug': 'cab-vs-tempo-traveller-group-travel-choice',
                'category': 'Cab & Taxi',
                'short_description': 'Comparing multi-cab booking versus hiring a single Tempo Traveller for family vacations, wedding groups, and corporate tours.',
                'content': '''<h2>Making the Right Vehicle Choice for Your Travel Group</h2>
<p>When traveling with 6 or more people, deciding whether to book two separate taxis or a single Tempo Traveller can significantly impact your budget, comfort, and group bonding.</p>

<h3>Benefits of Hiring a Tempo Traveller</h3>
<ul>
    <li><strong>Group Unity:</strong> Everyone travels together in a single spacious push-back seating cabin.</li>
    <li><strong>Cost Efficiency:</strong> Split toll fees, driver allowances, and fuel across 12-26 seats rather than multiple cars.</li>
    <li><strong>Ample Luggage Space:</strong> Roof carriers and rear boots easily fit large suitcases.</li>
</ul>''',
                'reading_time': '4 min read',
                'is_featured': False,
                'is_published': True,
                'featured_image': 'blog/tempo-traveller-group.jpg'
            },
            {
                'title': 'Top 10 Hidden Gem Places to Visit in Kerala in 2026',
                'slug': 'top-10-hidden-gem-places-visit-kerala-2026',
                'category': 'Destinations',
                'short_description': 'Beyond Munnar and Alleppey: explore secret waterfalls, misty hill stations, and quiet beaches across God’s Own Country.',
                'content': '''<h2>Discover Kerala Beyond the Tourist Trails</h2>
<p>Kerala is world-famous for its backwaters and tea hills, but South India harbors secluded spots that offer peace away from crowded resorts.</p>

<h3>1. Vagamon — Misty Meadows & Pine Forests</h3>
<p>Located in Idukki, Vagamon offers rolling green meadows, pine forests, and quiet trekking trails.</p>

<h3>2. Athirapally & Vazhachal Waterfalls</h3>
<p>Known as the Niagara of India, Athirapally Falls features thunderous cascades in dense tropical rainforests.</p>''',
                'reading_time': '6 min read',
                'is_featured': False,
                'is_published': True,
                'featured_image': 'blog/kerala-hidden-gems.jpg'
            },
            {
                'title': 'Essential Tips for a Comfortable Family Road Trip',
                'slug': 'essential-tips-comfortable-family-road-trip',
                'category': 'Family Travel',
                'short_description': 'How to ensure a smooth, enjoyable road journey when traveling with kids and senior family members.',
                'content': '''<h2>Family Travel Made Effortless and Enjoyable</h2>
<p>Road trips with family create lifelong memories. Here are top tips from Vibhu Travel Hub experienced drivers for smooth multi-generation trips.</p>

<h3>Plan Frequent Stretch Breaks</h3>
<p>Plan stops every 2 to 3 hours at clean highway plazas for snacks, restroom breaks, and leg stretching.</p>''',
                'reading_time': '4 min read',
                'is_featured': False,
                'is_published': True,
                'featured_image': 'blog/family-road-trip.jpg'
            },
            {
                'title': 'How to Plan a Corporate Group Trip Effortlessly',
                'slug': 'how-to-plan-corporate-group-trip-effortlessly',
                'category': 'Corporate Travel',
                'short_description': 'Key logistics, vehicle selection, itinerary scheduling, and GST billing for corporate team outings.',
                'content': '''<h2>Streamlining Transport Logistics for Corporate Offsites</h2>
<p>Organizing corporate travel requires punctuality, comfortable vehicles, and reliable billing documentation.</p>

<h3>Why Companies Trust Vibhu Travel Hub</h3>
<p>We provide luxury buses, Tempo Travellers, and executive cabs with GST invoicing, verified drivers, and 24/7 helpline support.</p>''',
                'reading_time': '5 min read',
                'is_featured': False,
                'is_published': True,
                'featured_image': 'blog/corporate-group-travel.jpg'
            }
        ]

        count = 0
        updated = 0
        for b_data in sample_blogs:
            slug = b_data['slug']
            post = BlogPost.objects.filter(slug=slug).first()
            if not post:
                BlogPost.objects.create(
                    title=b_data['title'],
                    slug=slug,
                    category=b_data['category'],
                    short_description=b_data['short_description'],
                    content=b_data['content'],
                    reading_time=b_data['reading_time'],
                    is_featured=b_data['is_featured'],
                    is_published=b_data['is_published'],
                    author=author,
                    featured_image=b_data['featured_image']
                )
                count += 1
            else:
                post.featured_image = b_data['featured_image']
                post.category = b_data['category']
                post.is_featured = b_data['is_featured']
                post.save()
                updated += 1
                
        self.stdout.write(self.style.SUCCESS(f'Successfully seeded {count} new posts and updated {updated} posts with premium travel images.'))
