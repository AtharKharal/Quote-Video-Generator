import json, os
from captions import captions, follow_text


def build_input(quote, author, output_name="output.mp4", font="fonts/font.ttf",
                audio="audios/3.mp3", images_path="./images/images1",
                random_images=False, caption_override=None):
    """Build the input config dict dynamically.
    
    Args:
        quote: The quote text.
        author: The author name.
        output_name: Output video filename.
        font: Path to font file.
        audio: Path to audio file.
        images_path: Path to images folder.
        random_images: Whether to randomly select images from all folders.
        caption_override: If provided, use this as the IG caption instead of auto-building.
    
    Returns:
        dict with all config keys needed by VideoGenerator and VideoPublisher.
    """
    # Build caption: use override if given, else build from static bios
    if caption_override:
        caption = caption_override
    else:
        author_bio = captions.get(author, f"A quote by {author}.")
        caption = f"{quote}\n{follow_text}\n\n{author_bio}"

    return {
        "quote": quote,
        "author": author,
        "outputName": output_name,
        "font": font,
        "audio": audio,
        "imagesPath": images_path,
        "random": random_images,
        "caption": caption,
        "file_path": f"./{output_name}",
    }


def load_from_json(config_path="config.json"):
    """Load input config from a JSON file."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(script_dir, "..", config_path)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return build_input(**data)
    else:
        # Fallback to defaults for backward compat
        return build_input(
            quote="My being was never so low as to seek praise from some mere humans.",
            author="Fyodor Dostoevsky",
        )


# Backward compatibility: modules that `from input import input_dict` still work
input_dict = load_from_json()