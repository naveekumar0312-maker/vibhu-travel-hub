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

        return f"{self.name} | {self.vehicle} | {self.destination}"

class Vehicle(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, max_length=150, blank=True)
    category = models.CharField(max_length=100, help_text="e.g. SUV, Sedan, Mini Bus")
    model_name = models.CharField(max_length=100, blank=True, help_text="e.g. Etios / Dzire")
    
    price = models.CharField(max_length=50, blank=True, help_text="e.g. ₹1800 / Day")
    badge_text = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. Best Seller")
    
    image = models.ImageField(upload_to="vehicles/", validators=[validate_image_size, validate_image_extension])
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
    
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    whatsapp_enabled = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

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


