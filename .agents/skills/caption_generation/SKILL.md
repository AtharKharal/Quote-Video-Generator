---
description: Generate viral Instagram captions with hooks, CTAs, and hashtags via LLM
---

# Caption Generation Skill

## Purpose
Create Instagram Reel captions optimized for engagement: scroll-stopping hooks, clear CTAs, and strategically mixed hashtags. Uses LLM when available, falls back to templates.

## Module
`agents/caption_generator.py` — `CaptionGenerator` class

## Usage
```python
from agents.caption_generator import CaptionGenerator

gen = CaptionGenerator()
caption = gen.generate(quote="...", author="Seneca", mood="reflective")
# Returns: complete caption string ready for Instagram
```

## Caption Structure (What the LLM Generates)
1. **Hook line** — under 60 chars with emoji (visible above "more" fold)
2. Full quote text with author attribution
3. CTA — "Follow @quill_of_humanity" + "Tag someone who needs this 👇"
4. 25 hashtags — mix of high-volume (#quotes, #motivation) and niche (#stoicism, #deepthoughts)

## Fallback Template
When no LLM is available, uses a template with:
- Random hook emoji from: 🔥 💭 🖤 ⚡ 🌙 🗝️ 📖 💀 🧠 🌊
- Standard CTA block
- 25 pre-selected hashtags covering quotes/philosophy/wisdom

## Environment Variables
| Variable | Required | Description |
|---|---|---|
| `LLM_API_KEY` | Optional | Same key as quote curation |
| `LLM_PROVIDER` | Optional | `gemini` (default) or `openai` |
