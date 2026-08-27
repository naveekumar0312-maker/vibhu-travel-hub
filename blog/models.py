# pyrefly: ignore [missing-import]
from django.db import models
# pyrefly: ignore [missing-import]
from django.contrib.auth.models import User
# pyrefly: ignore [missing-import]
from django.utils.text import slugify

CATEGORY_CHOICES = (
    ('Travel Tips', 'Travel Tips'),
    ('Destinations', 'Destinations'),
    ('Travel Guides', 'Travel Guides'),
    ('Cab & Taxi', 'Cab & Taxi'),
    ('Family Travel', 'Family Travel'),
    ('Corporate Travel', 'Corporate Travel'),
)

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, default='Travel Tips')
    short_description = models.TextField(blank=True)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="blog/", blank=True, null=True)
    
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', null=True, blank=True)
    
    published_date = models.DateTimeField(auto_now_add=True)
    reading_time = models.CharField(max_length=30, default='5 min read')
    is_featured = models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-published_date']
        
    def __str__(self):
        return self.title
        
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def get_image_url(self):
        if not self.featured_image:
            # pyrefly: ignore [missing-import]
            from django.conf import settings
            return settings.STATIC_URL + 'images/destinations/ooty.avif'
        try:
            url = str(self.featured_image.url)
            if url.startswith('http://') or url.startswith('https://'):
                return url
            if url.startswith('/media/') or url.startswith('/static/'):
                return url
            # pyrefly: ignore [missing-import]
            from django.conf import settings
            return settings.MEDIA_URL + url.lstrip('/')
        except Exception:
            # pyrefly: ignore [missing-import]
            from django.conf import settings
            return settings.STATIC_URL + 'images/destinations/ooty.avif'


