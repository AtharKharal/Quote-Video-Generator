import os
import sys

# Ensure the 'src' directory is in the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.config_manager import ConfigManager
from util import get_random_quote, select_audio

def get_input_dict(config_path=None):
    """
    Returns a dictionary of input parameters for the generation pipeline,
    dynamically loaded from the ConfigManager.
    """
    config = ConfigManager(config_path)
    
    # Handle autogen quote logic
    quote = config["quote"]
    author = config["author"]
    if config["autogen_quote"] and (not quote or not author):
        # Only fetch random quote if not manually provided
        try:
            quote, author = get_random_quote()
        except Exception as e:
            print(f"Error fetching random quote: {e}")
            quote = "Wisdom is the reward you get for a lifetime of listening when you'd have rather talked."
            author = "Mark Twain"
            
    # Handle audio selection logic
    audio_path = config["audio"]
    if not config["manual_audio"]:
        try:
            selected_audio = select_audio(quote)
            audio_path = os.path.join("audios", selected_audio)
        except Exception as e:
            print(f"Error selecting audio: {e}")
            # Fallback to default audio in config
            audio_path = config["audio"]

    # Construct the input dictionary expected by generators
    input_dict = {
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
    
    # Map 'images_path' back to 'imgGenre' context if needed for old scripts
    # (though generators should ideally use imagesPath)
    
    return input_dict

# Initialize a default input_dict for backward compatibility
# (imported by vid_generator.py and others)
input_dict = get_input_dict()

if __name__ == "__main__":
    import pprint
    print("Generated Input Dictionary:")
    pprint.pprint(input_dict)