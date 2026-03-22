from dotenv import load_dotenv 
from google import genai
from data.audio_data import audio_data_dict
load_dotenv()

client = genai.Client()

def generate_caption(author, quote):
        print("Generating caption...")
        response = client.models.generate_content(
            model="gemini-3-flash-preview", 
            contents=f"""Write a short short paragraph on {author} followed by a paragraph explaining both the history of his quote and the quote itself: {quote}. Write in pure plain text, do not use markdown formatting."""
        )

        follow_text= """———

follow @quill_of_humanity for more content!

———"""

        author_caption = response.text if response.text else author

        caption = f"{quote}\n\n{follow_text}\n\n{author_caption}"

        return caption

def select_audio(quote):
        print("Selecting audio from gemini...")    
        response = client.models.generate_content(
                model="gemini-3-flash-preview", 
                contents=f"""Out of the following names of audio-files and their descriptions, choose what you think ought to be best for the quote {quote}:\n\n{str(audio_data_dict)}\n\nRESPOND ONLY WITH THE FILE NAME AND NOTHING ELSE. DO NOT USE MARKDOWN FORMATTING, PLAIN-TEXT, FILE-NAME ONLY RESPONSE."""
        )

        print(f"Chose audio {response.text}.")

        return response.text

if __name__ == "__main__":
        r = select_audio("Hell is empty, and all the devils are here.")
        print(r)