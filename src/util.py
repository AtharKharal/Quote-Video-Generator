from dotenv import load_dotenv 
from google import genai
load_dotenv()

client = genai.Client()

def generate_caption(author, quote):
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

if __name__ == "__main__":
        r = generate_caption("Albert Einstein ", "There are only two ways to live your life. One is as though nothing is a miracle. The other is as though everything is a miracle.")
        print(r)