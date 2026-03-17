"""
Caption Generator Agent — creates viral Instagram captions + hashtags via LLM.

Usage:
    gen = CaptionGenerator()
    caption = gen.generate(quote="...", author="...", mood="reflective")
"""

import os, json
from dotenv import load_dotenv

load_dotenv()

CAPTION_PROMPT = """You are a viral Instagram content writer for a quote page (@quill_of_humanity).

Write an Instagram Reel caption for this quote:
Quote: "{quote}"
Author: {author}
Mood: {mood}

Requirements:
1. First line: a SHORT hook (under 60 chars) that makes people stop scrolling. Use an emoji.
2. Then a blank line.
3. The full quote text.
4. Author attribution with an em dash.
5. A blank line, then a CTA: "Follow @quill_of_humanity for more" and "Tag someone who needs this 👇"
6. A blank line, then 25 hashtags. Mix high-volume (1M+ posts) and niche hashtags. Include: #quotes #motivation #philosophy #wisdom #quotestoliveby and mood-relevant tags.

Return ONLY the caption text, ready to paste into Instagram. No JSON, no markdown fences."""

FALLBACK_TEMPLATE = """{hook_emoji} This hits different.

"{quote}"
— {author}

———
Follow @quill_of_humanity for more content!
Tag someone who needs to hear this 👇
———

#quotes #quotestoliveby #motivation #philosophy #wisdom #deepquotes #lifequotes #inspirationalquotes #dailyquotes #quotesdaily #quoteoftheday #motivationalquotes #thinkdeeply #mindset #innerpeace #selfreflection #personalgrowth #stoicism #existentialism #bookquotes #poetryoflife #wordsofwisdom #literaryquotes #thoughtprovoking #soulquotes"""

HOOK_EMOJIS = ["🔥", "💭", "🖤", "⚡", "🌙", "🗝️", "📖", "💀", "🧠", "🌊"]


class CaptionGenerator:
    def __init__(self):
        self.api_key = os.getenv("LLM_API_KEY")
        self.provider = os.getenv("LLM_PROVIDER", "gemini").lower()

    def generate(self, quote, author, mood="reflective"):
        """Generate a viral Instagram caption for the given quote.
        
        Args:
            quote: The quote text.
            author: Author name.
            mood: Emotional tone for hashtag selection.
        
        Returns:
            Complete caption string ready for Instagram.
        """
        if self.api_key:
            try:
                return self._generate_via_llm(quote, author, mood)
            except Exception as e:
                print(f"[CaptionGenerator] LLM call failed ({e}), using template.")
                return self._generate_fallback(quote, author, mood)
        else:
            print("[CaptionGenerator] No LLM_API_KEY set, using template caption.")
            return self._generate_fallback(quote, author, mood)

    def _generate_via_llm(self, quote, author, mood):
        """Call Gemini or OpenAI to generate caption."""
        prompt = CAPTION_PROMPT.format(quote=quote, author=author, mood=mood)

        if self.provider == "gemini":
            return self._call_gemini(prompt)
        elif self.provider == "openai":
            return self._call_openai(prompt)
        else:
            raise ValueError(f"Unknown LLM_PROVIDER: {self.provider}")

    def _call_gemini(self, prompt):
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text.strip()

    def _call_openai(self, prompt):
        from openai import OpenAI
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,
        )
        return response.choices[0].message.content.strip()

    def _generate_fallback(self, quote, author, mood):
        """Use a template-based caption when no LLM is available."""
        import random
        emoji = random.choice(HOOK_EMOJIS)
        return FALLBACK_TEMPLATE.format(hook_emoji=emoji, quote=quote, author=author)


if __name__ == "__main__":
    gen = CaptionGenerator()
    caption = gen.generate(
        quote="We suffer more often in imagination than in reality.",
        author="Seneca",
        mood="reflective",
    )
    print("\n--- Generated Caption ---")
    print(caption)
