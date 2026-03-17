---
description: Curate 5 viral-optimized quotes via Gemini/OpenAI LLM or fallback bank
---

# Quote Curation Skill

## Purpose
Generate 5 short, powerful quotes optimized for maximum Instagram engagement (saves, shares, reposts).

## Module
`agents/quote_curator.py` — `QuoteCurator` class

## Usage
```python
from agents.quote_curator import QuoteCurator

curator = QuoteCurator()
quotes = curator.curate(theme="stoicism and inner strength")
# Returns: list of 5 dicts with keys: quote, author, mood, theme
```

## How It Works
1. **With LLM_API_KEY set**: Sends a carefully engineered prompt to Gemini or OpenAI requesting 5 quotes optimized for virality. The prompt enforces:
   - Under 120 characters per quote (short = shareable)
   - Real quotes from known thinkers
   - Strong emotional hooks
   - No author repetition
   
2. **Without API key (fallback)**: Randomly selects 5 from a 15-quote curated bank in the source code.

## Environment Variables
| Variable | Required | Description |
|---|---|---|
| `LLM_API_KEY` | Optional | Gemini or OpenAI API key |
| `LLM_PROVIDER` | Optional | `gemini` (default) or `openai` |

## Output Schema
```json
[
  {"quote": "...", "author": "...", "mood": "reflective", "theme": "philosophy"},
  ...
]
```

## Mood Values
`reflective`, `melancholic`, `intense`, `uplifting`, `dark`, `calm`
