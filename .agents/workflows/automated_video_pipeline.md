---
description: Full automated pipeline — curate quotes, source media, generate video, publish to Instagram
---

# Automated Video Pipeline

This workflow runs the entire automated quote video pipeline with minimal human intervention.

## Prerequisites

- Python virtual environment activated
- Dependencies installed: `pip install -r requirements.txt`
- `.env` file configured with all API keys (see `.env.example`)

## Steps

1. **Run the full pipeline**

    // turbo

    ```bash
    cd e:\Computing\Quote-Video-Generator
    python pipeline.py --theme "stoicism"
    ```

2. **HITL: Pick a quote** — The pipeline will display 5 quotes. Type the number (1-5) to select one. Everything after this is automatic.

3. **Dry run (no publish)**

    // turbo

    ```bash
    python pipeline.py --dry-run --theme "dark motivation"
    ```

4. **Verify output** — Check `output.mp4` was generated correctly.

## Theme Ideas for High Engagement

- `stoicism` — consistently high saves/shares
- `dark motivation` — high watch time
- `existentialism` — niche but loyal audience
- `love and solitude` — high comment engagement
- `philosophy and life` — broad appeal (default)

## Troubleshooting

- **No LLM_API_KEY**: Pipeline uses fallback quotes and template captions (still works)
- **No PEXELS_API_KEY**: Pipeline uses local images from `images/` folders
- **Video won't render**: Ensure `ffmpeg` is installed and on PATH
- **Instagram publish fails**: Check ACCESS_TOKEN hasn't expired (they expire every 60 days)
