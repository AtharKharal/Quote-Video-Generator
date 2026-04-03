import os
import json
from dotenv import load_dotenv

load_dotenv()

class ConfigManager:
    """
    A robust configuration manager to manage application settings from
    JSON files, environment variables, and defaults.
    """
    DEFAULTS = {
        "quote": None,
        "author": None,
        "vid_output_name": "output.mp4",
        "img_output_name": "output.png",
        "autogen_quote": True,
        "imgGenre": 1,
        "random": True,
        "audio": "audios/10.mp3",
        "manual_audio": False,
        "font": "fonts/font.ttf",
        "bg_img_opacity": 0.3,
        "bg_img_duration": 0.35,
        "images_path": "images/images1",
        "watermark": "@quill_of_humanity"
    }

    def __init__(self, config_path=None):
        self.config = self.DEFAULTS.copy()
        if config_path and os.path.exists(config_path):
            self.load_from_json(config_path)
        self.load_from_env()

    def load_from_json(self, path):
        """Loads configuration from a JSON file."""
        try:
            with open(path, 'r') as f:
                data = json.load(f)
                self.config.update(data)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load config from {path}: {e}")

    def load_from_env(self):
        """Loads configuration from environment variables (e.g., QUOTE, AUTHOR)."""
        for key in self.config:
            env_val = os.getenv(key.upper())
            if env_val is not None:
                # Basic type conversion based on default value type
                if isinstance(self.config[key], bool):
                    self.config[key] = env_val.lower() == 'true'
                elif isinstance(self.config[key], int):
                    try:
                        self.config[key] = int(env_val)
                    except ValueError:
                        pass
                elif isinstance(self.config[key], float):
                    try:
                        self.config[key] = float(env_val)
                    except ValueError:
                        pass
                else:
                    self.config[key] = env_val

    def get(self, key, default=None):
        """Retrieves a configuration value by key."""
        return self.config.get(key, default)

    def __getitem__(self, key):
        """Allows dictionary-like access to configuration values."""
        return self.config[key]

    def to_dict(self):
        """Returns the entire configuration as a dictionary."""
        return self.config

    def __repr__(self):
        return f"<ConfigManager {self.config}>"
