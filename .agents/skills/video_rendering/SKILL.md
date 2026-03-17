---
description: Render quote videos using MoviePy with dynamic configuration
---

# Video Rendering Skill

## Purpose
Generate 1080×1920 (9:16) MP4 videos with animated background images, quote text overlay, and background audio using the existing `VideoGenerator` engine.

## Module
`execution/vid_generator.py` — `VideoGenerator` class

## Usage
```python
from execution.vid_generator import VideoGenerator

vid_gen = VideoGenerator(
    quote="We suffer more often in imagination than in reality.",
    author_name="Seneca",
    output_name="output.mp4",
    imagesPath="./images/temp_session",
    font="fonts/font.ttf",
    audio_path="audios/3.mp3",
    randomImages=False,
)
vid_gen.generate()  # Writes output.mp4
```

## Config Parameters
| Parameter | Type | Description |
|---|---|---|
| `quote` | str | Quote text to display |
| `author_name` | str | Author attribution below quote |
| `output_name` | str | Output filename (e.g., `output.mp4`) |
| `imagesPath` | str | Path to folder with background images |
| `font` | str | Path to TTF font file |
| `audio_path` | str | Path to MP3 background audio |
| `randomImages` | bool | If True, randomly picks images from all `images/` subfolders |

## How It Works
1. Loads images from the specified folder, crops to 9:16, applies 30% opacity darkening
2. Creates an animated slideshow (0.2s per frame, looped to fill duration)
3. Overlays the quote text (center, 55pt) and author name (below center, 45pt)
4. Composites everything with audio, writes to MP4 via libx264

## Dependencies
- `moviepy`, `pillow`, `numpy`, `imageio-ffmpeg`
- System: `ffmpeg` must be on PATH
