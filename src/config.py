import json
import os

CONFIG_FILE = 'config.json'
DEFAULT_CONFIG = {
    # Image settings
    "max_width": 1920,
    "max_height": 1080,
    "quality": 85,
    # Video settings
    "video_crf": 23,          # 18-28 (lower = better quality, higher = smaller file)
    "video_preset": "medium",  # faster, medium, slow (slower = smaller file)
    "video_max_width": 1920,
    "video_max_height": 1080,
}


def load_config():
    """Loads configuration from config.json, or returns defaults."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, '..', CONFIG_FILE)
    
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                loaded = json.load(f)
                # Merge with defaults to include any new settings
                config = {**DEFAULT_CONFIG, **loaded}
                return config
        except Exception:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()


def save_config(config):
    """Saves configuration to config.json."""
    base_path = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(base_path, '..', CONFIG_FILE)
    
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
