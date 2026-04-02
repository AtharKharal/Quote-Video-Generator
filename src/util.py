import requests, json, os, textwrap
from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import numpy as np
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client()
models = ["gemini-2.5-flash", "gemini-3-flash-preview", "gemini-3.1-flash-lite-preview"]
model = models[2] # When you hit max RPD of one model, switch to the other. You can add as many here as you like

def generate_caption(author, quote):
        print("Generating caption...")
        response = client.models.generate_content(
            model=model,
            contents=f"""Write a short short paragraph on {author} followed by a paragraph explaining both the history of his quote and the quote itself: {quote}. Write in pure plain text, do not use markdown formatting."""
        )

        follow_text= """———

follow @quill_of_humanity for more content!

———"""

        author_caption = response.text if response.text else author

        caption = f"{quote}\n\n{follow_text}\n\n{author_caption}"

        max_caption_size = 2200

        return caption[:max_caption_size]

def select_audio(quote):
        print("Selecting audio from gemini...")    
        response = client.models.generate_content(
                model=model,
                contents=f"""Out of the following names of audio-files and their descriptions, choose what you think ought to be best for the quote {quote}:\n\n{str(audio_data_dict)}\n\nRESPOND ONLY WITH THE FILE NAME AND NOTHING ELSE. DO NOT USE MARKDOWN FORMATTING, PLAIN-TEXT, FILE-NAME ONLY RESPONSE."""
        )

        print(f"Chose audio {response.text}.")

        return response.text

def get_random_quote():
    """Fetches a random quote from ZenQuotes API."""
    url = "https://zenquotes.io/api/random"
    try:
        r = json.loads(requests.get(url).content.decode("utf-8"))[0]
        q, a = r["q"], r["a"]
        return q, a
    except Exception as e:
        print(f"Error fetching random quote: {e}")
        return "The only way to do great work is to love what you do.", "Steve Jobs"

class MediaUtils:
    @staticmethod
    def smart_crop(img, target_width, target_height):
        """
        Intelligently crops an image to a target aspect ratio.
        Default is center-crop.
        """
        orig_w, orig_h = img.size
        target_ratio = target_width / target_height
        orig_ratio = orig_w / orig_h

        if orig_ratio > target_ratio:
            # Image is wider than target
            new_w = int(round(orig_h * target_ratio))
            left = (orig_w - new_w) // 2
            top = 0
            right = left + new_w
            bottom = orig_h
        else:
            # Image is taller than target
            new_h = int(round(orig_w / target_ratio))
            left = 0
            top = (orig_h - new_h) // 2
            right = orig_w
            bottom = top + new_h

        img = img.crop((left, top, right, bottom))
        img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        return img

    @staticmethod
    def apply_opacity(img, opacity):
        """Applies a 'fake' opacity by darkening the image."""
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(opacity)

    @staticmethod
    def wrap_text(text, width=30):
        """Wraps text to a specific width."""
        wrapper = textwrap.TextWrapper(width=width)
        return "\n".join(wrapper.wrap(text=text))

if __name__ == "__main__":
        q, a = get_random_quote()
        print(q, a)