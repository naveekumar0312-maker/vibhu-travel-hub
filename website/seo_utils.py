"""
SEO Utilities for Vibhu Travel Hub
Dynamic keyword definitions, city mappings, meta generators, and schema helpers.
"""

# 26 Target Keywords definitions
SEO_KEYWORDS = [
    "Innova rental in {city}",
    "26 seater Tempo Traveller in {city}",
    "Innova Crysta rental in {city}",
    "Force Urbania rental in {city}",
    "Ertiga rental in {city}",
    "minibus rental in {city}",
    "sedan car rental in {city}",
    "20 seater bus rental in {city}",
    "SUV car rental in {city}",
    "30 seater bus rental in {city}",
    "7 seater car rental in {city}",
    "35 seater bus rental in {city}",
    "luxury car rental in {city}",
    "40 seater bus rental in {city}",
    "Tempo Traveller rental in {city}",
    "45 seater bus rental in {city}",
    "AC Tempo Traveller in {city}",
    "50 seater bus rental in {city}",
    "12 seater Tempo Traveller in {city}",
    "54 seater bus rental in {city}",
    "14 seater Tempo Traveller in {city}",
    "AC bus rental in {city}",
    "17 seater Tempo Traveller in {city}",
    "non AC bus rental in {city}",
    "20 seater Tempo Traveller in {city}",
    "luxury coach rental in {city}"
]

DESTINATION_CITIES = {
    "tamilnadu": ["Coimbatore", "Chennai", "Madurai", "Trichy"],
    "kerala": ["Kochi", "Trivandrum", "Thrissur", "Calicut"],
    "karnataka": ["Bangalore", "Mysore", "Coorg", "Chikmagalur"]
}

VEHICLE_SEO_MAP = {
    "innova": ["Innova rental in {city}", "Innova Crysta rental in {city}", "7 seater car rental in {city}"],
    "innova_crysta": ["Innova Crysta rental in {city}", "Innova rental in {city}", "7 seater car rental in {city}", "luxury car rental in {city}"],
    "ertiga": ["Ertiga rental in {city}", "7 seater car rental in {city}", "SUV car rental in {city}"],
    "sedan": ["sedan car rental in {city}", "luxury car rental in {city}"],
    "suv": ["SUV car rental in {city}", "7 seater car rental in {city}", "luxury car rental in {city}"],
    "tempo_traveller_12": ["12 seater Tempo Traveller in {city}", "Tempo Traveller rental in {city}", "AC Tempo Traveller in {city}"],
    "tempo_traveller_14": ["14 seater Tempo Traveller in {city}", "Tempo Traveller rental in {city}", "AC Tempo Traveller in {city}"],
    "tempo_traveller_17": ["17 seater Tempo Traveller in {city}", "Tempo Traveller rental in {city}", "AC Tempo Traveller in {city}"],
    "tempo_traveller_20": ["20 seater Tempo Traveller in {city}", "Tempo Traveller rental in {city}", "AC Tempo Traveller in {city}"],
    "tempo_traveller_26": ["26 seater Tempo Traveller in {city}", "Tempo Traveller rental in {city}", "AC Tempo Traveller in {city}"],
    "urbania": ["Force Urbania rental in {city}", "Tempo Traveller rental in {city}", "AC Tempo Traveller in {city}", "luxury car rental in {city}"],
    "minibus": ["minibus rental in {city}", "20 seater bus rental in {city}", "30 seater bus rental in {city}", "AC bus rental in {city}"],
    "bus_35": ["35 seater bus rental in {city}", "AC bus rental in {city}", "non AC bus rental in {city}", "luxury coach rental in {city}"],
    "bus_40": ["40 seater bus rental in {city}", "AC bus rental in {city}", "non AC bus rental in {city}", "luxury coach rental in {city}"],
    "bus_45": ["45 seater bus rental in {city}", "AC bus rental in {city}", "non AC bus rental in {city}", "luxury coach rental in {city}"],
    "bus_50": ["50 seater bus rental in {city}", "54 seater bus rental in {city}", "AC bus rental in {city}", "luxury coach rental in {city}"]
}


def get_city_keywords(city_name):
    """Generate dynamic keywords for a specific city."""
    return [kw.format(city=city_name) for kw in SEO_KEYWORDS]


def get_vehicle_city_keyword(vehicle_type, city_name, index=0):
    """Get dynamic vehicle keyword for specific vehicle type and city."""
    patterns = VEHICLE_SEO_MAP.get(vehicle_type, ["{city} vehicle rental"])
    pattern = patterns[index % len(patterns)]
    return pattern.format(city=city_name)


def get_city_schema(city_name, region_name):
    """Generate JSON-LD Service schema dict for city vehicle rentals."""
    return {
        "@context": "https://schema.org",
        "@type": "CarRental",
        "name": f"Vibhu Travel Hub - Vehicle Rental in {city_name}",
        "description": f"Book Innova, Innova Crysta, Ertiga, 12 to 26 seater Tempo Traveller, Force Urbania, and 20 to 54 seater luxury bus rentals in {city_name}, {region_name}.",
        "url": f"https://www.vibhutravelhub.com/destinations/{region_name.lower().replace(' ', '-')}/",
        "telephone": "+91-9655866660",
        "address": {
            "@type": "PostalAddress",
            "addressLocality": city_name,
            "addressRegion": region_name,
            "addressCountry": "IN"
        },
        "areaServed": city_name,
        "makesOffer": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"Innova Crysta rental in {city_name}"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"Tempo Traveller rental in {city_name}"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"Force Urbania rental in {city_name}"}},
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": f"AC bus rental in {city_name}"}}
        ]
    }
