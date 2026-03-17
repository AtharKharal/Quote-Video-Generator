"""
Quote Curator Agent — generates 5 viral-optimized quotes via Gemini API.

Usage:
    curator = QuoteCurator()
    quotes = curator.curate(theme="stoicism")  # returns list of 5 dicts
"""

import os, json, random
from dotenv import load_dotenv

load_dotenv()

# Fallback quotes bank when API is unavailable
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
    {"quote": "The only way to deal with an unfree world is to become so absolutely free that your very existence is an act of rebellion.", "author": "Albert Camus", "mood": "intense", "theme": "freedom"},
    {"quote": "It is not death that a man should fear, but he should fear never beginning to live.", "author": "Marcus Aurelius", "mood": "reflective", "theme": "stoicism"},
    {"quote": "The measure of intelligence is the ability to change.", "author": "Albert Einstein", "mood": "calm", "theme": "growth"},
    {"quote": "Everything we hear is an opinion, not a fact. Everything we see is a perspective, not the truth.", "author": "Marcus Aurelius", "mood": "reflective", "theme": "perception"},
    {"quote": "In the middle of difficulty lies opportunity.", "author": "Albert Einstein", "mood": "uplifting", "theme": "resilience"},
]

CURATION_PROMPT = """You are a viral content strategist for an Instagram quote page (@quill_of_humanity).
Generate exactly 5 short, powerful quotes optimized for maximum engagement (saves, shares, reposts) on Instagram Reels.

Theme/mood requested: {theme}

Requirements:
- Each quote must be under 120 characters (short = more shareable)
- Prefer REAL quotes from well-known philosophers, writers, psychologists, or thinkers
- Prioritize quotes that evoke strong emotion: awe, melancholy, motivation, existential punch
- Mix of authors — do NOT repeat the same author
- Each quote should work visually on a dark, cinematic background

Return ONLY a JSON array with exactly 5 objects, each having:
- "quote": the quote text
- "author": the author's full name
- "mood": one of [reflective, melancholic, intense, uplifting, dark, calm]
- "theme": one word theme

Example output:
[
  {{"quote": "He who has a why can bear almost any how.", "author": "Friedrich Nietzsche", "mood": "intense", "theme": "purpose"}},
  ...
]

Return ONLY the JSON array, no markdown fences, no commentary."""


class QuoteCurator:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        self.provider = os.getenv("LLM_PROVIDER", "gemini").lower()

    def curate(self, theme="philosophy and life"):
        """Return 5 viral-optimized quotes.
        
        Args:
            theme: Topic/mood to guide quote selection (e.g., "stoicism", "dark motivation")
        
        Returns:
            List of 5 dicts with keys: quote, author, mood, theme
        """
        if self.api_key:
            try:
                return self._curate_via_llm(theme)
            except Exception as e:
                print(f"[QuoteCurator] LLM call failed ({e}), using fallback quotes.")
                return self._curate_fallback()
        else:
            print("[QuoteCurator] No LLM_API_KEY set, using fallback quotes.")
            return self._curate_fallback()

    def _curate_via_llm(self, theme):
        """Call Gemini or OpenAI to generate quotes."""
        prompt = CURATION_PROMPT.format(theme=theme)

        if self.provider == "gemini":
            return self._call_gemini(prompt)
        elif self.provider == "openai":
            return self._call_openai(prompt)
        else:
            raise ValueError(f"Unknown LLM_PROVIDER: {self.provider}")

    def _call_gemini(self, prompt):
        """Call Google Gemini API."""
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return self._parse_response(response.text)

    def _call_openai(self, prompt):
        """Call OpenAI API."""
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.9,
        )
        return self._parse_response(response.choices[0].message.content)

    def _parse_response(self, text):
        """Parse LLM response into list of quote dicts."""
        # Strip markdown fences if present
        text = text.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1]  # remove first line
            text = text.rsplit("```", 1)[0]  # remove last fence
        
        quotes = json.loads(text.strip())
        
        if not isinstance(quotes, list) or len(quotes) < 5:
            raise ValueError(f"Expected 5 quotes, got {len(quotes) if isinstance(quotes, list) else 'non-list'}")
        
        return quotes[:5]

    def _curate_fallback(self):
        """Return 5 random quotes from the fallback bank."""
        return random.sample(FALLBACK_QUOTES, 5)


if __name__ == "__main__":
    curator = QuoteCurator()
    quotes = curator.curate(theme="stoicism and inner strength")
    for i, q in enumerate(quotes, 1):
        print(f"\n  [{i}] \"{q['quote']}\"")
        print(f"      — {q['author']}  (mood: {q['mood']}, theme: {q['theme']})")
