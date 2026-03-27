from dotenv import load_dotenv 
from google import genai
from data.audio_data import audio_data_dict
import requests, json
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
        url = "https://zenquotes.io/api/random"

        r = json.loads(requests.get(url).content.decode("utf-8"))[0]
        q, a = r["q"], r["a"]
        return q, a

if __name__ == "__main__":
        q, a = get_random_quote()
        print(q, a)