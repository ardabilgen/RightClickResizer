import json
import os

CONFIG_FILE = 'config.json'
DEFAULT_CONFIG = {
    "max_width": 1920,
    "max_height": 1080,
    "quality": 85
}

def load_config():
    """Loads configuration from config.json, or returns defaults."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, '..', CONFIG_FILE)
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception:
            return DEFAULT_CONFIG
    return DEFAULT_CONFIG

def save_config(config):
    """Saves configuration to config.json."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, '..', CONFIG_FILE)
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
