# pyrefly: ignore [missing-import]
from django.db import models
# pyrefly: ignore [missing-import]
from django.utils import timezone
# pyrefly: ignore [missing-import]
from django.utils.text import slugify
# pyrefly: ignore [missing-import]
from django.urls import reverse
# pyrefly: ignore [missing-import]
from django.core.exceptions import ValidationError
import os

def validate_image_size(value):
    filesize = value.size
    if filesize > 5 * 1024 * 1024:
        raise ValidationError("Maximum upload size is 5MB")

def validate_image_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension. Only JPG, JPEG, PNG, WEBP are allowed.')

def validate_video_extension(value):
    ext = os.path.splitext(value.name)[1].lower()
    valid_extensions = ['.mp4', '.webm']
    if ext not in valid_extensions:
        raise ValidationError('Please upload a valid MP4 or WebM video.')


class Enquiry(models.Model):

    VEHICLE_CHOICES = [

        ("Taxi", "Taxi"),
        ("SUV", "SUV"),
        ("Tempo Traveller", "Tempo Traveller"),
        ("Mini Bus", "Mini Bus"),
        ("Bus", "Bus"),

    ]

    STATUS_CHOICES = [

        ("New", "New"),
        ("Contacted", "Contacted"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),

    ]

    # Customer Details
    name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    email = models.EmailField(blank=True, null=True)

    # Trip Details
    destination = models.CharField(max_length=255, blank=True, null=True, help_text="e.g. Tamil Nadu")
    tourist_place = models.CharField(max_length=255, blank=True, null=True, help_text="e.g. Marina Beach")
    pickup = models.CharField(max_length=255)
    drop = models.CharField(max_length=255, default='')
    travel_date = models.DateField()
    message = models.TextField(blank=True, null=True)

    # Enquiry Status
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="New"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Travel Enquiry"

        verbose_name_plural = "Travel Enquiries"

    def __str__(self):
        if self.destination:
            return f"{self.name} | {self.destination}"
        return f"{self.name}"

class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=150, blank=True)
    category = models.CharField(max_length=100, help_text="e.g. SUV, Sedan, Mini Bus")
    model_name = models.CharField(max_length=100, blank=True, help_text="e.g. Etios / Dzire")
    
    price = models.CharField(max_length=50, blank=True, help_text="e.g. ₹1800 / Day")
    badge_text = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. Best Seller")
    
    image = models.ImageField(upload_to="vehicles/", validators=[validate_image_size, validate_image_extension])
    vehicle_video = models.FileField(
        upload_to="vehicles/videos/",
        blank=True,
        null=True,
        validators=[validate_video_extension],
        verbose_name="Vehicle Video",
        help_text="Upload optional vehicle video (.mp4 or .webm)"
    )
    short_description = models.TextField(blank=True, help_text="Maximum 2 lines")
    
    # Specs
    passengers = models.PositiveIntegerField(default=4, help_text="Passenger Capacity")
    luggage = models.CharField(max_length=50, blank=True, help_text="e.g. 3 Bags")
    ac_type = models.CharField(max_length=50, default="AC", help_text="e.g. AC / Non AC")
    transmission = models.CharField(max_length=50, default="Manual", help_text="e.g. Manual / Automatic")
    fuel_type = models.CharField(max_length=50, default="Diesel", help_text="e.g. Diesel / Petrol / EV")
    
    # Booleans
    has_driver = models.BooleanField(default=True, verbose_name="Professional Driver")
    has_music = models.BooleanField(default=True, verbose_name="Music System")
    has_charging = models.BooleanField(default=True, verbose_name="Charging Port")
    has_pushback = models.BooleanField(default=False, verbose_name="Push Back Seat")
    
    # Features
    feature_tags = models.CharField(max_length=255, blank=True, help_text="Comma separated (e.g. GPS, Fast Charging, Luxury Seats)")
    
    # Official Tariff & Fare Structure Fields
    day_rent = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Day Rent Up To 400 KM (₹)")
    per_km_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Per KM Rate Up To 400 KM (₹)")
    flat_per_km_above_400 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Flat Per KM Above 400 KM (₹)")
    driver_pay_above_400 = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Driver Pay Above 400 KM (₹)")
    kerala_permit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Kerala Permit Cost (₹)")
    karnataka_permit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Karnataka Permit Cost (₹)")
    above_400_applicable = models.BooleanField(default=True, verbose_name="Above 400 KM Applicable")
    
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    whatsapp_enabled = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Dynamic Features & Specifications for Premium Fleet Showcase
    left_features = models.TextField(
        blank=True,
        default="Luxury Vehicles\nWell Maintained\nAC & Comfort\nLuggage Space\nDriver Included",
        help_text="Enter left feature card items (one per line)"
    )
    right_specifications = models.TextField(
        blank=True,
        default="12–17 Seater\nPremium Interiors\nAC & Comfortable Seats\nLuggage Space\nDriver & Fuel Included",
        help_text="Enter right specifications list items (one per line)"
    )

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self):
        return f"{self.name} - {self.model_name}"

    def save(self, *args, **kwargs):
        # Process main image if it's new or changed
        if self.image:
            try:
                old_instance = Vehicle.objects.get(pk=self.pk)
                if old_instance.image != self.image:
                    from website.utils import process_vehicle_image
                    self.image = process_vehicle_image(self.image)
            except Vehicle.DoesNotExist:
                from website.utils import process_vehicle_image
                self.image = process_vehicle_image(self.image)
                
        super().save(*args, **kwargs)

    @property
    def get_video_url(self):
        if self.vehicle_video:
            return self.vehicle_video.url
        import os
        # pyrefly: ignore [missing-import]
        from django.conf import settings
        if self.slug:
            for ext in ['mp4', 'webm']:
                rel_path = f"video/{self.slug}.{ext}"
                full_path = os.path.join(settings.BASE_DIR, 'static', rel_path)
                if os.path.exists(full_path):
                    return f"/static/{rel_path}"
        return None

    @property
    def left_features_list(self):
        if not self.left_features:
            return ["Luxury Vehicles", "Well Maintained", "AC & Comfort", "Luggage Space", "Driver Included"]
        return [f.strip() for f in self.left_features.split('\n') if f.strip()]

    @property
    def right_specifications_list(self):
        if not self.right_specifications:
            spec = f"{self.passengers} Seater" if self.passengers else "12–17 Seater"
            return [spec, "Premium Interiors", "AC & Comfortable Seats", "Luggage Space", "Driver & Fuel Included"]
        return [s.strip() for s in self.right_specifications.split('\n') if s.strip()]

    @property
    def get_feature_tags_list(self):
        if not self.feature_tags:
            return []
        
        seen = set()
        clean_features = []
        for f in self.feature_tags.split(','):
            tag = f.strip()
            if tag and tag not in seen:
                seen.add(tag)
                clean_features.append(tag)
                
        return clean_features

    @property
    def display_price(self):
        import re
        raw_val = (self.price or "").strip()
        if not raw_val and self.badge_text:
            raw_val = self.badge_text.strip()
            
        if not raw_val or raw_val in ['0', '0.0', '0.00']:
            return "Price on Request"
            
        numbers = re.findall(r'\d+', raw_val.replace(',', ''))
        if numbers:
            num_str = "".join(numbers)
            try:
                num = int(num_str)
                if num <= 0:
                    return "Price on Request"
                s = str(num)
                if len(s) <= 3:
                    formatted = s
                else:
                    last_three = s[-3:]
                    other_digits = s[:-3]
                    res = ""
                    while len(other_digits) > 2:
                        res = "," + other_digits[-2:] + res
                        other_digits = other_digits[:-2]
                    formatted = other_digits + res + "," + last_three
                return f"₹{formatted}"
            except ValueError:
                pass
                
        return "Price on Request"




class VehicleGallery(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="gallery")
    image = models.ImageField(upload_to="vehicles/gallery/", validators=[validate_image_size, validate_image_extension])
    caption = models.CharField(max_length=100, blank=True)
    display_order = models.IntegerField(default=0)

    class Meta:
        ordering = ["display_order"]

    def __str__(self):
        return f"Gallery Image for {self.vehicle.name}"

    def save(self, *args, **kwargs):
        if self.image:
            try:
                old_instance = VehicleGallery.objects.get(pk=self.pk)
                if old_instance.image != self.image:
                    from website.utils import process_vehicle_image
                    self.image = process_vehicle_image(self.image)
            except VehicleGallery.DoesNotExist:
                from website.utils import process_vehicle_image
                self.image = process_vehicle_image(self.image)
                
        super().save(*args, **kwargs)




class OutstationRoute(models.Model):
    route_name = models.CharField(max_length=100, help_text="e.g. Coimbatore to Chennai")
    destination_name = models.CharField(max_length=100, help_text="e.g. Chennai")
    image = models.ImageField(upload_to="outstation_routes/", validators=[validate_image_size, validate_image_extension])
    badge_text = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. Popular, Trending")
    short_description = models.TextField(help_text="SEO friendly short description.")
    travel_time = models.CharField(max_length=50, help_text="e.g. 8 Hours 30 Mins")
    distance = models.CharField(max_length=50, help_text="e.g. 510 Kms")
    vehicle_types = models.CharField(max_length=255, help_text="e.g. Sedan, SUV, Innova Crysta, TT")
    starting_price = models.CharField(max_length=50, help_text="e.g. 4999")
    display_order = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["display_order"]
        verbose_name = "Outstation Route"
        verbose_name_plural = "Outstation Routes"

    def __str__(self):
        return self.route_name

class NewsletterSubscriber(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-subscribed_at"]
        verbose_name = "Newsletter Subscriber"
        verbose_name_plural = "Newsletter Subscribers"

    def __str__(self):
        return f"{self.name} ({self.email})"


class CitySEO(models.Model):
    city_name = models.CharField(max_length=100, unique=True, help_text="e.g. Coimbatore, Madurai, Chennai, Bangalore, Kochi")
    slug = models.SlugField(unique=True, max_length=100)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    primary_keywords = models.TextField(blank=True, help_text="Priority A keywords (comma or newline separated)")
    route_keywords = models.TextField(blank=True, help_text="Priority C route keywords (comma or newline separated)")
    airport_keywords = models.TextField(blank=True, help_text="Airport keywords (comma or newline separated)")
    corporate_keywords = models.TextField(blank=True, help_text="Corporate & B2B keywords (comma or newline separated)")
    wedding_event_keywords = models.TextField(blank=True, help_text="Wedding & Event keywords (comma or newline separated)")
    segment_keywords = models.TextField(blank=True, help_text="Tour Segment keywords like School/College/Family/Pilgrimage (comma or newline separated)")
    seo_content = models.TextField(blank=True, help_text="Custom HTML/Text content block for city page")
    image_alt_text = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["city_name"]
        verbose_name = "City SEO Content"
        verbose_name_plural = "City SEO Content"

    def __str__(self):
        return f"City SEO - {self.city_name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.city_name)
        super().save(*args, **kwargs)

    @property
    def get_primary_keywords_list(self):
        if not self.primary_keywords:
            return []
        return [k.strip() for k in self.primary_keywords.replace('\n', ',').split(',') if k.strip()]

    @property
    def get_route_keywords_list(self):
        if not self.route_keywords:
            return []
        return [k.strip() for k in self.route_keywords.replace('\n', ',').split(',') if k.strip()]

    @property
    def get_airport_keywords_list(self):
        if not self.airport_keywords:
            return []
        return [k.strip() for k in self.airport_keywords.replace('\n', ',').split(',') if k.strip()]

    @property
    def get_corporate_keywords_list(self):
        if not self.corporate_keywords:
            return []
        return [k.strip() for k in self.corporate_keywords.replace('\n', ',').split(',') if k.strip()]

    @property
    def get_wedding_keywords_list(self):
        if not self.wedding_event_keywords:
            return []
        return [k.strip() for k in self.wedding_event_keywords.replace('\n', ',').split(',') if k.strip()]

    @property
    def get_segment_keywords_list(self):
        if not self.segment_keywords:
            return []
        return [k.strip() for k in self.segment_keywords.replace('\n', ',').split(',') if k.strip()]


class FleetPartnerInquiry(models.Model):
    STATUS_CHOICES = [
        ("New", "New"),
        ("Contacted", "Contacted"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    VEHICLE_CHOICES = [
        ("Sedan", "Sedan"),
        ("SUV", "SUV"),
        ("Luxury Car", "Luxury Car"),
        ("Tempo Traveller", "Tempo Traveller"),
        ("Mini Bus", "Mini Bus"),
        ("Tourist Bus", "Tourist Bus"),
    ]

    SERVICE_CHOICES = [
        ("Local Travel", "Local Travel"),
        ("Airport Transfer", "Airport Transfer"),
        ("Outstation Travel", "Outstation Travel"),
        ("Tour Packages", "Tour Packages"),
        ("Corporate Travel", "Corporate Travel"),
        ("All Services", "All Services"),
    ]

    name = models.CharField(max_length=100, verbose_name="Name")
    mobile = models.CharField(max_length=20, verbose_name="Mobile Number")
    email = models.EmailField(verbose_name="Email Address")
    city = models.CharField(max_length=100, verbose_name="City")
    vehicle_count = models.CharField(max_length=50, verbose_name="Number of Vehicles")
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_CHOICES, verbose_name="Vehicle Type")
    service_type = models.CharField(max_length=100, choices=SERVICE_CHOICES, verbose_name="Service Preference", blank=True, null=True)
    message = models.TextField(blank=True, null=True, verbose_name="Message")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="New",
        verbose_name="Status"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Fleet Partner Application"
        verbose_name_plural = "Fleet Partner Applications"

    def __str__(self):
        return f"{self.name} - {self.city} ({self.vehicle_type} x {self.vehicle_count})"


class PartnerEnquiry(models.Model):
    STATUS_CHOICES = [
        ("New", "New"),
        ("Contacted", "Contacted"),
        ("In Progress", "In Progress"),
        ("Converted", "Converted"),
        ("Rejected", "Rejected"),
    ]

    VEHICLE_CHOICES = [
        ("Car", "Car"),
        ("Sedan", "Sedan"),
        ("SUV", "SUV"),
        ("Tempo Traveller", "Tempo Traveller"),
        ("Luxury Bus", "Luxury Bus"),
        ("Other", "Other"),
    ]

    SERVICE_CHOICES = [
        ("Local Cab Service", "Local Cab Service"),
        ("Outstation Travel", "Outstation Travel"),
        ("Airport Transfer", "Airport Transfer"),
        ("Corporate Travel", "Corporate Travel"),
        ("Tourist Packages", "Tourist Packages"),
        ("All Services", "All Services"),
    ]

    full_name = models.CharField(max_length=100, verbose_name="Full Name")
    mobile_number = models.CharField(max_length=20, verbose_name="Mobile Number")
    email = models.EmailField(verbose_name="Email Address", blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name="City")
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_CHOICES, verbose_name="Vehicle Type")
    vehicle_count = models.CharField(max_length=50, verbose_name="Number of Vehicles")
    vehicle_details = models.CharField(max_length=255, verbose_name="Vehicle Model / Details", blank=True, null=True)
    preferred_service = models.CharField(max_length=100, choices=SERVICE_CHOICES, verbose_name="Preferred Service")
    message = models.TextField(blank=True, null=True, verbose_name="Message")

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="New",
        verbose_name="Status"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Partner Enquiry"
        verbose_name_plural = "Partner Enquiries"

    def __str__(self):
        return f"{self.full_name} - {self.city} ({self.vehicle_type} x {self.vehicle_count})"


class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="City Name")
    is_active = models.BooleanField(default=True, verbose_name="Active Status")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        return self.name


class OneWayFare(models.Model):
    from_city = models.CharField(max_length=100, verbose_name="From City")
    to_city = models.CharField(max_length=100, verbose_name="To City")
    fare = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Starting Fare (₹)")
    is_active = models.BooleanField(default=True, verbose_name="Active Status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["from_city", "to_city"]
        verbose_name = "One Way Fare"
        verbose_name_plural = "One Way Fares"

    @property
    def destination(self):
        return self.to_city

    def __str__(self):
        return f"{self.from_city} → {self.to_city} (₹{self.fare})"


class OneWayBooking(models.Model):
    STATUS_CHOICES = [
        ("New", "New"),
        ("Contacted", "Contacted"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField(verbose_name="Email ID")
    mobile = models.CharField(max_length=20, verbose_name="Mobile Number")
    pickup_date = models.DateField(verbose_name="Pickup Date")
    pickup_time = models.CharField(max_length=50, verbose_name="Pick Up Time")
    pickup_city = models.CharField(max_length=100, verbose_name="Pickup City")
    drop_city = models.CharField(max_length=100, verbose_name="Drop Off City")
    comments = models.TextField(blank=True, null=True, verbose_name="Comments")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="New",
        verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Submitted Date")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "One Way Booking"
        verbose_name_plural = "One Way Bookings"

    @property
    def mobile_number(self):
        return self.mobile

    @property
    def drop_off_city(self):
        return self.drop_city

    def __str__(self):
        return f"{self.name} - {self.pickup_city} to {self.drop_city} ({self.pickup_date})"


class RoundTripFare(models.Model):
    from_city = models.CharField(max_length=100, verbose_name="From City")
    place = models.CharField(max_length=150, verbose_name="Place / Route")
    distance_km = models.CharField(max_length=50, verbose_name="Km")
    trip_duration = models.CharField(max_length=50, verbose_name="Trip Duration")
    sedan_fare = models.CharField(max_length=50, verbose_name="Sedan Fare")
    mini_fare = models.CharField(max_length=50, verbose_name="Mini / SUV Fare")
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True, verbose_name="Active Status")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["from_city", "display_order"]
        verbose_name = "Round Trip Fare"
        verbose_name_plural = "Round Trip Fares"

    def __str__(self):
        return f"{self.from_city} → {self.place} (Sedan: {self.sedan_fare}, Mini: {self.mini_fare})"


class RoundTripBooking(models.Model):
    STATUS_CHOICES = [
        ("New", "New"),
        ("Contacted", "Contacted"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField(verbose_name="Email ID")
    mobile = models.CharField(max_length=20, verbose_name="Mobile Number")
    pickup_city = models.CharField(max_length=100, verbose_name="Pickup City")
    pickup_date = models.DateField(verbose_name="Pickup Date")
    pickup_time = models.CharField(max_length=50, verbose_name="Pick Up Time")
    dropoff_date = models.DateField(verbose_name="Drop Off Date")
    dropoff_time = models.CharField(max_length=50, verbose_name="Drop Off Time")
    comments = models.TextField(blank=True, null=True, verbose_name="Comments")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="New",
        verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Submitted Date")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Round Trip Booking"
        verbose_name_plural = "Round Trip Bookings"

    def __str__(self):
        return f"{self.name} - {self.pickup_city} ({self.pickup_date} to {self.dropoff_date})"


class HourlyRentalFare(models.Model):
    VEHICLE_CATEGORIES = [
        ("Sedan / Hatchback", "Sedan / Hatchback"),
        ("SUV / MUV", "SUV / MUV"),
        ("Tempo Traveller", "Tempo Traveller"),
        ("Luxury Bus", "Luxury Bus"),
    ]

    city = models.CharField(max_length=100, verbose_name="City")
    vehicle_type = models.CharField(max_length=100, choices=VEHICLE_CATEGORIES, verbose_name="Vehicle Type")
    hours = models.IntegerField(default=1, verbose_name="Hours")
    base_fare = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Base Fare")
    free_km = models.IntegerField(default=10, verbose_name="Free KM")
    extra_km_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Extra KM Fare")
    extra_minute_fare = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Extra Minute Fare")
    is_active = models.BooleanField(default=True, verbose_name="Active Status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["city", "vehicle_type", "hours"]
        verbose_name = "Hourly Rental Fare"
        verbose_name_plural = "Hourly Rental Fares"

    def __str__(self):
        return f"{self.city} - {self.vehicle_type} ({self.hours} Hrs - ₹{self.base_fare})"


class BulkBooking(models.Model):
    STATUS_CHOICES = [
        ("New", "New"),
        ("Contacted", "Contacted"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]

    name = models.CharField(max_length=100, verbose_name="Name")
    email = models.EmailField(verbose_name="Email ID")
    mobile_number = models.CharField(max_length=20, verbose_name="Mobile Number")
    pickup_date = models.DateField(verbose_name="Pickup Date")
    pickup_city = models.CharField(max_length=100, verbose_name="Pickup City")
    comments = models.TextField(blank=True, null=True, verbose_name="Comments")
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="New",
        verbose_name="Status"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Submitted Date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Bulk Booking"
        verbose_name_plural = "Bulk Bookings"

    def __str__(self):
        return f"{self.name} - {self.pickup_city} ({self.pickup_date})"










