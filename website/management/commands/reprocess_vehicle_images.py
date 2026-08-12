from django.core.management.base import BaseCommand
from website.models import Vehicle

class Command(BaseCommand):
    help = 'Reprocesses all existing vehicle images to fit exactly 1200x700 with WebP optimization.'

    def handle(self, *args, **options):
        vehicles = Vehicle.objects.exclude(image='')
        total = vehicles.count()
        self.stdout.write(f"Found {total} vehicles with images.")
        
        success_count = 0
        for vehicle in vehicles:
            self.stdout.write(f"Processing image for {vehicle.name}...")
            # Flag it to force the model's save method to process the image
            setattr(vehicle, '_force_process_image', True)
            try:
                vehicle.save()
                success_count += 1
            except Exception as e:
                self.stderr.write(f"Failed to process {vehicle.name}: {e}")
                
        self.stdout.write(self.style.SUCCESS(f"Successfully processed {success_count} out of {total} images."))
