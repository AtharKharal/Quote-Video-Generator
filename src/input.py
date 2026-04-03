import os
import sys

# Ensure the 'src' directory is in the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.config_manager import ConfigManager
from util import get_random_quote, select_audio

def get_input_dict(config_path=None):
    """
    Returns a dictionary of input parameters, prioritizing settings.json
    in the project root, then falling back to the ConfigManager.
    """
    settings_file = "settings.json"
    
    # Try local settings.json first for simplicity
    if os.path.exists(settings_file):
        try:
            with open(settings_file, "r") as f:
                settings = json.load(f)
                input_dict = {
                    "quote": settings.get("quote"),
                    "author": settings.get("author"),
                    "outputName": settings.get("vid_output_name", "output.mp4"),
                    "imgOutputName": settings.get("img_output_name", "output.png"),
                    "autogen_quote": settings.get("autogen_quote", False),
                    "manual_audio": settings.get("manual_audio", True),
                    "audio": settings.get("audio_file", "audios/1.mp3"),
                    "font": settings.get("font", "fonts/font.ttf"),
                    "imagesPath": settings.get("images_path", "images/images1"),
                    "random": settings.get("random", True),
                    "bg_img_opacity": settings.get("bg_img_opacity", 0.3),
                    "bg_img_duration": settings.get("bg_img_duration", 0.35),
                    "watermark": settings.get("watermark", "@quill_of_humanity")
                }
                
                # Still handle autogen logic if requested
                if input_dict["autogen_quote"] and (not input_dict["quote"] or not input_dict["author"]):
                    input_dict["quote"], input_dict["author"] = get_random_quote()
                
                return input_dict
        except Exception as e:
            print(f"Warning: Failed to load {settings_file}: {e}. Falling back to ConfigManager.")

    # Fallback to the original ConfigManager logic
    config = ConfigManager(config_path)
    
    # Handle autogen quote logic
    quote = config["quote"]
    author = config["author"]
    if config["autogen_quote"] and (not quote or not author):
        try:
            quote, author = get_random_quote()
        except Exception:
            quote, author = "The only way to do great work is to love what you do.", "Steve Jobs"
            
    # Handle audio selection logic
    audio_path = config["audio"]
    if not config["manual_audio"]:
        try:
            selected_audio = select_audio(quote)
            audio_path = os.path.join("audios", selected_audio)
        except Exception:
            audio_path = config["audio"]

    return {
        "quote": quote,
        "author": author,
        "outputName": config["vid_output_name"],
        "imgOutputName": config["img_output_name"],
        "font": config["font"],
        "audio": audio_path,
        "imagesPath": config["images_path"],
        "random": config["random"],
        "bg_img_opacity": config["bg_img_opacity"],
        "bg_img_duration": config["bg_img_duration"],
        "watermark": config["watermark"]
    }

# Initialize a default input_dict for backward compatibility
input_dict = get_input_dict()

if __name__ == "__main__":
    import pprint
    print("Generated Input Dictionary:")
    pprint.pprint(input_dict)