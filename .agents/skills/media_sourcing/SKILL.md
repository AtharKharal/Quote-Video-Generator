---
description: Fetch portrait stock photos from Pexels API and select mood-matched audio
---

# Media Sourcing Skill

## Purpose

Source high-quality portrait-orientation stock photos and select background audio that matches the quote's emotional tone. Optimized for 9:16 vertical Instagram Reels.

## Module

`agents/media_sourcer.py` — `MediaSourcer` class

## Usage

```python
from agents.media_sourcer import MediaSourcer

sourcer = MediaSourcer()
result = sourcer.source(mood="melancholic", theme="solitude")
# result = {"images_path": "./images/temp_session", "audio_path": "audios/3.mp3"}

# After video is rendered, clean up temp images:
sourcer.cleanup()
```

## How It Works

### Image Sourcing (Pexels API)

1. Builds a search query combining mood + theme + "cinematic" for high-quality results
2. Requests 10 portrait-orientation images from Pexels
3. Downloads high-res versions to `images/temp_session/`
4. Falls back to existing local `images/images[1-4]/` folders if API is unavailable

### Audio Selection (Mood Mapping)

Maps quote mood to existing audio files:

| Mood | Audio File |
| --- | --- |
| reflective, calm | `audios/1.mp3` |
| intense | `audios/2.mp3` |
| melancholic, dark | `audios/3.mp3` |
| uplifting | `audios/4.mp3` |

## Environment Variables

| Variable | Required | Description |
| --- | --- | --- |
| `PEXELS_API_KEY` | Optional | Free key from [pexels.com/api](https://www.pexels.com/api/) |

## Notes

- `temp_session/` is auto-cleaned by `sourcer.cleanup()` after video render
- To expand audio options: add more `.mp3` files to `audios/` and update `MOOD_AUDIO_MAP` in the source
