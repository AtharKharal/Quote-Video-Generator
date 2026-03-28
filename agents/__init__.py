"""
Consolidated module for all automated agents: QuoteCurator, MediaSourcer, and CaptionGenerator.
"""

import os, json, random, requests, shutil, io
from dotenv import load_dotenv

load_dotenv()

# --- Config & Defaults ---
FALLBACK_QUOTES = [
    {"quote": "The only thing I know is that I know nothing.", "author": "Socrates", "mood": "reflective", "theme": "philosophy"},
    {"quote": "He who has a why to live can bear almost any how.", "author": "Friedrich Nietzsche", "mood": "intense", "theme": "purpose"},
    {"quote": "The unexamined life is not worth living.", "author": "Socrates", "mood": "reflective", "theme": "philosophy"},
    {"quote": "Man is condemned to be free.", "author": "Jean-Paul Sartre", "mood": "dark", "theme": "existentialism"},
    {"quote": "One must imagine Sisyphus happy.", "author": "Albert Camus", "mood": "uplifting", "theme": "absurdism"},
    {"quote": "To live is to suffer, to survive is to find some meaning in the suffering.", "author": "Friedrich Nietzsche", "mood": "melancholic", "theme": "suffering"},
    {"quote": "Happiness is not something ready made. It comes from your own actions.", "author": "Dalai Lama", "mood": "uplifting", "theme": "happiness"},
    {"quote": "The soul that sees beauty may sometimes walk alone.", "author": "Johann Wolfgang von Goethe", "mood": "melancholic", "theme": "beauty"},
    {"quote": "We suffer more often in imagination than in reality.", "author": "Seneca", "mood": "calm", "theme": "stoicism"},
    {"quote": "No man is free who is not master of himself.", "author": "Epictetus", "mood": "intense", "theme": "stoicism"},
]

MOOD_AUDIO_MAP = {
    "reflective": "audios/1.mp3",
    "calm": "audios/1.mp3",
    "melancholic": "audios/3.mp3",
    "dark": "audios/3.mp3",
    "intense": "audios/2.mp3",
    "uplifting": "audios/4.mp3",
}

HOOK_EMOJIS = ["🔥", "💭", "🖤", "⚡", "🌙", "🗝️", "📖", "💀", "🧠", "🌊"]


class QuoteCurator:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        self.provider = os.getenv("LLM_PROVIDER", "gemini").lower()

    def curate(self, theme="philosophy and life"):
        if not self.api_key:
            return random.sample(FALLBACK_QUOTES, 5)
        try:
            prompt = f"Generate 5 viral-optimized short quotes for theme: {theme}. Return ONLY a JSON array with 'quote', 'author', 'mood', 'theme'."
            if self.provider == "gemini":
                import google.generativeai as genai
                genai.configure(api_key=self.api_key)
                model = genai.GenerativeModel("gemini-2.0-flash")
                response = model.generate_content(prompt)
                text = response.text.strip().strip("```json").strip("```")
            else: # openai fallback
                from openai import OpenAI
                client = OpenAI(api_key=self.api_key)
                response = client.chat.completions.create(model="gpt-4o-mini", messages=[{"role": "user", "content": prompt}])
                text = response.choices[0].message.content.strip()
            return json.loads(text)[:5]
        except Exception as e:
            print(f"[QuoteCurator] Error ({e}), using fallback.")
            return random.sample(FALLBACK_QUOTES, 5)


class MediaSourcer:
    def __init__(self):
        self.api_key = os.getenv("PEXELS_API_KEY")
        self.session_dir = os.path.join("images", "temp_session")

    def source(self, mood="reflective", theme="nature"):
        if os.path.exists(self.session_dir): shutil.rmtree(self.session_dir)
        os.makedirs(self.session_dir, exist_ok=True)
        audio = MOOD_AUDIO_MAP.get(mood, "audios/1.mp3")
        
        if not self.api_key:
            return {"images_path": "./images/images1", "audio_path": audio}
        
        try:
            resp = requests.get("https://api.pexels.com/v1/search", 
                               headers={"Authorization": self.api_key}, 
                               params={"query": f"{mood} {theme} cinematic", "orientation": "portrait", "per_page": 10}, 
                               timeout=15)
            photos = resp.json().get("photos", [])
            for i, p in enumerate(photos):
                img_data = requests.get(p["src"]["large2x"], timeout=30).content
                with open(os.path.join(self.session_dir, f"img_{i:02d}.jpg"), "wb") as f: f.write(img_data)
            return {"images_path": self.session_dir, "audio_path": audio}
        except Exception:
            return {"images_path": "./images/images1", "audio_path": audio}

    def cleanup(self):
        if os.path.exists(self.session_dir): shutil.rmtree(self.session_dir)


class CaptionGenerator:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")

    def generate(self, quote, author, mood="reflective"):
        if not self.api_key:
            return f"{random.choice(HOOK_EMOJIS)} This hits different.\n\n\"{quote}\"\n— {author}\n\nFollow @quill_of_humanity for more!"
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            prompt = f"Write a viral Instagram caption for: \"{quote}\" by {author}. Mode: {mood}. Include hook, full quote, CTA, and 25 hashtags."
            return model.generate_content(prompt).text.strip()
        except Exception:
            return f"💭 Reflective moment.\n\n\"{quote}\"\n— {author}\n\n#quotes #wisdom"
