import json
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

class CognitiveEnricher:
    """
    Analytical Enrichment Layer managed by the Cognitive Specialist.
    Translates quote text into deterministic aesthetic parameters.
    """
    
    AESTHETIC_MAP = {
        "Stoic": {
            "font_size": 55,
            "opacity": 0.25,
            "color": "#E0E0E0",
            "bg_img_duration": 0.45,
            "vibe": "dark_ambient"
        },
        "Motivational": {
            "font_size": 65,
            "opacity": 0.45,
            "color": "#FFFFFF",
            "bg_img_duration": 0.3,
            "vibe": "inspiring_upbeat"
        },
        "Melancholic": {
            "font_size": 50,
            "opacity": 0.2,
            "color": "#CCCCCC",
            "bg_img_duration": 0.6,
            "vibe": "soft_melodic"
        }
    }

    def __init__(self, model_id="gemini-2.0-flash"):
        self.model_id = model_id
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            print("Warning: GEMINI_API_KEY not found. Enrichment will use safe defaults.")
            self.client = None
        else:
            try:
                self.client = genai.Client(api_key=api_key)
            except Exception:
                self.client = None

    def enrich(self, quote, author):
        """
        Extracts emotional subtext and generates optimized metadata.
        """
        if not self.client:
             print("Skipping AI Enrichment (Client Initialization Failed). Using Stoic defaults.")
             return {
                "sentiment": "Stoic",
                "intensity": 0.5,
                "caption": f"{quote} - {author}",
                "hashtags": ["#wisdom", "#quotes"],
                "aesthetics": self.AESTHETIC_MAP["Stoic"]
            }
        
        print(f"Enriching content with {self.model_id}...")
        
        prompt = f"""
        Analyze the following quote by {author}:
        "{quote}"
        
        1. Identify the dominant emotional bucket: Stoic, Motivational, or Melancholic.
        2. Assign an intensity score from 0.1 to 1.0.
        3. Generate an Instagram-ready caption (plain text).
        4. Provide 5 highly relevant hashtags.
        
        Return ONLY a JSON object:
        {{
            "sentiment": "Stoic | Motivational | Melancholic",
            "intensity": 0.5,
            "caption": "...",
            "hashtags": ["#tag1", "#tag2", ...]
        }}
        """

        try:
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config={
                    'response_mime_type': 'application/json',
                }
            )
            
            enrichment_data = json.loads(response.text)
            
            # Map sentiment to aesthetics
            sentiment = enrichment_data.get("sentiment", "Stoic")
            # Fallback for unexpected AI response strings
            if "Motivational" in sentiment: sentiment = "Motivational"
            elif "Melancholic" in sentiment: sentiment = "Melancholic"
            else: sentiment = "Stoic"
            
            aesthetics = self.AESTHETIC_MAP.get(sentiment, self.AESTHETIC_MAP["Stoic"])
            enrichment_data["aesthetics"] = aesthetics
            
            print(f"Sentiment Analysis Results: {sentiment} (Intensity: {enrichment_data.get('intensity')})")
            return enrichment_data

        except Exception as e:
            print(f"Cognitive Enrichment Failed: {e}")
            # Safe Fallback
            return {
                "sentiment": "Stoic",
                "intensity": 0.5,
                "caption": f"{quote} - {author}",
                "hashtags": ["#wisdom", "#quotes"],
                "aesthetics": self.AESTHETIC_MAP["Stoic"]
            }

if __name__ == "__main__":
    enricher = CognitiveEnricher()
    test_quote = "Amor Fati: Love your fate, which is in fact your life."
    print(enricher.enrich(test_quote, "Friedrich Nietzsche"))
