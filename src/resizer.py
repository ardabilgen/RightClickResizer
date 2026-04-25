import os
from PIL import Image

def resize_image(image_path, max_width, max_height, quality):
    """Resizes an image maintaining aspect ratio."""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary (e.g. for PNG to JPG conversion if we wanted, 
            # but here we keep format mostly, except for transparency handling if needed)
            # For now, we just resize and save in same format or convert if needed.
            
            # Use thumbnail to resize maintaining aspect ratio and only if necessary
            img.thumbnail((max_width, max_height), Image.Resampling.BICUBIC)
            
            # Construct new filename
            directory, filename = os.path.split(image_path)
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_resized{ext}"
            new_path = os.path.join(directory, new_filename)
            
            # Save
            # Handle some formats that might need specific params
            if ext.lower() in ['.jpg', '.jpeg']:
                img.save(new_path, quality=quality)
            else:
                img.save(new_path, quality=quality)
                
            print(f"Resized: {image_path} -> {new_path}")
            return True
    except Exception as e:
        print(f"Error resizing {image_path}: {e}")
        return False
