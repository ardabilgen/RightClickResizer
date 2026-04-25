import os
import sys
from unittest import TestCase, main
from PIL import Image

# Add src to sys.path
sys.path.append(os.path.abspath("src"))

from config import load_config, save_config
from resizer import resize_image

class TestFixes(TestCase):
    def setUp(self):
        self.test_image = "test_input.jpg"
        self.resized_image = "test_input_resized.jpg"
        if not os.path.exists(self.test_image):
            img = Image.new("RGB", (2000, 1000), color="red")
            img.save(self.test_image)

    def tearDown(self):
        for f in [self.test_image, self.resized_image, "config.json"]:
            if os.path.exists(f):
                os.remove(f)

    def test_resizer_optimization(self):
        # Test resizing
        max_w, max_h, quality = 1000, 500, 85
        success = resize_image(self.test_image, max_w, max_h, quality)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(self.resized_image))
        
        with Image.open(self.resized_image) as img:
            width, height = img.size
            # Check if within bounds and aspect ratio maintained
            self.assertLessEqual(width, max_w)
            self.assertLessEqual(height, max_h)
            # Original ratio 2:1, new should be same or within bounds
            self.assertAlmostEqual(width/height, 2.0, places=1)

    def test_config_missing_keys(self):
        # Create a config with missing keys
        incomplete_config = {"max_width": 1000}
        save_config(incomplete_config)
        
        config = load_config()
        # Check if defaults are used (based on main.py logic)
        self.assertEqual(config.get("max_width"), 1000)
        self.assertIsNone(config.get("max_height")) 

if __name__ == "__main__":
    main()
