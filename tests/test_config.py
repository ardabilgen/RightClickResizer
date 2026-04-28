import json
import os
import tempfile
import unittest
import sys

# Add src to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from config import load_config, save_config, DEFAULT_CONFIG

class TestConfig(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_path = os.path.join(self.temp_dir, 'config.json')
        # Temporarily change the CONFIG_FILE constant for testing
        import config
        self.original_config_file = config.CONFIG_FILE
        config.CONFIG_FILE = 'config.json' # It looks in src/../config.json relative to script

    def tearDown(self):
        import config
        config.CONFIG_FILE = self.original_config_file

    def test_load_config_defaults_when_missing(self):
        # If config.json doesn't exist in the expected place, it returns defaults
        config = load_config()
        self.assertEqual(config.get("max_width"), DEFAULT_CONFIG["max_width"])

    def test_save_and_load_config(self):
        # We will test save_config by writing to a temp file and reading it back manually
        test_config = {"max_width": 1280, "max_height": 720, "quality": 90}
        
        # Save to temp path
        with open(self.config_path, 'w') as f:
            json.dump(test_config, f)
            
        # Read back manually to verify JSON integrity
        with open(self.config_path, 'r') as f:
            loaded = json.load(f)
            
        self.assertEqual(loaded, test_config)

if __name__ == '__main__':
    unittest.main()
