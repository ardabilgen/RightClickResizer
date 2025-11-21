import os
from PIL import Image

def resize_image(image_path, max_width, max_height, quality):
    """Resizes an image maintaining aspect ratio."""
    try:
        with Image.open(image_path) as img:
            # Convert to RGB if necessary (e.g. for PNG to JPG conversion if we wanted, 
            # but here we keep format mostly, except for transparency handling if needed)
            # For now, we just resize and save in same format or convert if needed.
            
            # Calculate new size
            width, height = img.size
            aspect_ratio = width / height
            
            new_width = width
            new_height = height

            if width > max_width or height > max_height:
                if (max_width / width) < (max_height / height):
                    new_width = max_width
                    new_height = int(max_width / aspect_ratio)
                else:
                    new_height = max_height
                    new_width = int(max_height * aspect_ratio)
            
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Construct new filename
            directory, filename = os.path.split(image_path)
            name, ext = os.path.splitext(filename)
            new_filename = f"{name}_resized{ext}"
            new_path = os.path.join(directory, new_filename)
            
            # Save
            # Handle some formats that might need specific params
            if ext.lower() in ['.jpg', '.jpeg']:
                img.save(new_path, quality=quality, optimize=True)
            else:
                img.save(new_path, quality=quality)
                
            print(f"Resized: {image_path} -> {new_path}")
            return True
    except Exception as e:
        print(f"Error resizing {image_path}: {e}")
        return False
