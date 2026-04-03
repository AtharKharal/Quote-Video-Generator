# 🚀 Quote2Vid Quickstart Guide

This guide explains how to run the Quote2Vid engine simply and reliably.

## 1. Fast Configuration
All your variables are now in a single file in the project root: **`settings.json`**.
Open it to modify:
- **`quote`**: The text you want in the video.
- **`author`**: The author's name.
- **`audio_file`**: Path to your mp3 (e.g., `audios/10.mp3`).
- **`images_path`**: The folder containing background images.

## 2. Running the Generator
To generate a video with your settings, simply run:
```powershell
python src/controller.py
```
This will:
1. Load your settings from `settings.json`.
2. Enrich the quote with AI sentiment analysis (Captions & Hashtags).
3. Generate `output.mp4`.

## 3. Troubleshooting (Audio/Visual)
If your output has no audio or the text looks wrong, run our diagnostic tool:
```powershell
python test_media.py
```
This will check your Python environment, verify asset paths, and generate a 3-second test clip (`diagnostic_test.mp4`) to confirm MoviePy is working correctly on your machine.

---
### 🏛️ Note on Architecture
The project uses a **Tri-Layer Hierarchy** (Law, Practitioners, Apparatus) designed for high-performance automation. While it looks complex, it ensures that once your settings are correct, the system can generate thousands of videos deterministically for multiple accounts without drifting from your brand standards.
