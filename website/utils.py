import os
from io import BytesIO
# pyrefly: ignore [missing-import]
from PIL import Image, ImageChops, ImageOps
# pyrefly: ignore [missing-import]
from django.core.files.base import ContentFile

def trim_image(im):
    """
    Trims empty space (either transparent or matching the top-left pixel color)
    from the image.
    """
    # Convert to RGBA to ensure we have an alpha channel for transparency checks
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    
    # Try to trim based on top-left pixel color (useful for solid white/gray backgrounds)
    bg = Image.new(im.mode, im.size, im.getpixel((0,0)))
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    diff_bbox = diff.getbbox()
    
    if diff_bbox:
        return im.crop(diff_bbox)
    
    # Fallback: just get bbox of non-transparent areas
    bbox = im.getbbox()
    if bbox:
        return im.crop(bbox)
        
    return im

def process_vehicle_image(image_field, target_size=(1200, 800)):
    """
    Processes an uploaded vehicle image:
    1. Trims empty space.
    2. Resizes while maintaining aspect ratio to fit within target_size.
    3. Pastes onto a centered transparent/white canvas of exactly target_size.
    4. Returns a WebP ContentFile ready to be saved to Django models.
    """
    if not image_field or not hasattr(image_field, 'read'):
        return image_field
        
    try:
        image_field.seek(0)
        img = Image.open(image_field)
        
        # Handle EXIF orientation
        img = ImageOps.exif_transpose(img)
        
        # Trim empty space
        img = trim_image(img)
        
        # Calculate resize ratio to fit within target_size
        ratio = min(target_size[0] / img.width, target_size[1] / img.height)
        new_size = (int(img.width * ratio), int(img.height * ratio))
        
        # Resize safely
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Create new canvas (white for RGB, transparent for RGBA)
        if img.mode == 'RGBA':
            canvas = Image.new('RGBA', target_size, (255, 255, 255, 0))
        else:
            canvas = Image.new('RGB', target_size, (255, 255, 255))
        
        # Calculate paste position (center)
        paste_pos = (
            (target_size[0] - new_size[0]) // 2,
            (target_size[1] - new_size[1]) // 2
        )
        
        # Paste using the image itself as mask if RGBA, else just paste
        canvas.paste(img, paste_pos, img if img.mode == 'RGBA' else None)
        
        # Save to buffer
        buffer = BytesIO()
        # WebP supports RGBA (transparency) natively and offers great compression
        canvas.save(buffer, format='WebP', quality=90, method=6)
        
        # Extract filename and ensure it ends with .webp
        original_name = os.path.basename(image_field.name)
        file_name, _ = os.path.splitext(original_name)
        
        # pyrefly: ignore [missing-import]
        from django.utils.text import slugify
        import uuid
        
        safe_name = slugify(file_name)
        if not safe_name:
            safe_name = "vehicle"
            
        unique_id = uuid.uuid4().hex[:8]
        new_filename = f"{safe_name}-{unique_id}.webp"
        
        return ContentFile(buffer.getvalue(), name=new_filename)
        
    except Exception as e:
        print(f"Error processing vehicle image: {e}")
        return image_field
