import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from PIL import Image

# Add src to path
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from resizer import resize_image

class TestResizer(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        # Create a small test image
        self.test_image_path = os.path.join(self.temp_dir, 'test.jpg')
        self.img = Image.new('RGB', (1920, 1080), color='red')
        self.img.save(self.test_image_path)

    def test_resize_image_success(self):
        result = resize_image(self.test_image_path, 800, 600, 85)
        self.assertTrue(result)
        
        new_path = os.path.join(self.temp_dir, 'test_resized.jpg')
        self.assertTrue(os.path.exists(new_path))
        
        with Image.open(new_path) as img:
            self.assertLessEqual(img.width, 800)
            self.assertLessEqual(img.height, 600)

    def test_resize_image_invalid_path(self):
        result = resize_image("non_existent.jpg", 800, 600, 85)
        self.assertFalse(result)

    def test_resize_image_maintains_aspect_ratio(self):
        result = resize_image(self.test_image_path, 400, 400, 85)
        self.assertTrue(result)
        
        new_path = os.path.join(self.temp_dir, 'test_resized.jpg')
        with Image.open(new_path) as img:
            # Original is 16:9 (1920x1080). If max is 400x400, width should be 400, height should be 225.
            self.assertLessEqual(img.width, 400)
            self.assertLessEqual(img.height, 400)

if __name__ == '__main__':
    unittest.main()
