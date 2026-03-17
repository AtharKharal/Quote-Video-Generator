"""
Media Sourcer Agent — fetches stock photos from Pexels API and selects audio.

Usage:
    sourcer = MediaSourcer()
    result = sourcer.source(mood="melancholic", theme="solitude")
    # result = {"images_path": "./images/temp_session", "audio_path": "audios/3.mp3"}
"""

import os, requests, shutil
from dotenv import load_dotenv

load_dotenv()

# Map moods to existing audio files.
# Expand this mapping as new audio is added to audios/
MOOD_AUDIO_MAP = {
    "reflective": "audios/1.mp3",
    "calm": "audios/1.mp3",
    "melancholic": "audios/3.mp3",
    "dark": "audios/3.mp3",
    "intense": "audios/2.mp3",
    "uplifting": "audios/4.mp3",
}
DEFAULT_AUDIO = "audios/1.mp3"

# Pexels orientation for 9:16 vertical Reels
PEXELS_ORIENTATION = "portrait"
PEXELS_PER_PAGE = 10


class MediaSourcer:
    def __init__(self):
        self.api_key = os.getenv("PEXELS_API_KEY")
        self.session_dir = os.path.join("images", "temp_session")

    def source(self, mood="reflective", theme="nature"):
        """Fetch stock images and select audio based on mood.

        Args:
            mood: Emotional tone (reflective, melancholic, intense, uplifting, dark, calm)
            theme: Topic keyword for image search (e.g., "mountains", "ocean", "solitude")

        Returns:
            dict with "images_path" and "audio_path"
        """
        audio_path = self._select_audio(mood)
        images_path = self._fetch_images(mood, theme)
        return {"images_path": images_path, "audio_path": audio_path}

    def _select_audio(self, mood):
        """Map mood to an audio file from the audios/ folder."""
        path = MOOD_AUDIO_MAP.get(mood, DEFAULT_AUDIO)
        if os.path.exists(path):
            return path
        print(f"[MediaSourcer] Audio '{path}' not found, using default.")
        return DEFAULT_AUDIO

    def _fetch_images(self, mood, theme):
        """Download portrait images from Pexels API matching the mood/theme."""
        # Clean up previous session
        if os.path.exists(self.session_dir):
            shutil.rmtree(self.session_dir)
        os.makedirs(self.session_dir, exist_ok=True)

        if not self.api_key:
            print("[MediaSourcer] No PEXELS_API_KEY set, falling back to local images.")
            return self._fallback_images()

        # Build search query: combine mood and theme for cinematic results
        query = f"{mood} {theme} cinematic"
        url = "https://api.pexels.com/v1/search"
        headers = {"Authorization": self.api_key}
        params = {
            "query": query,
            "orientation": PEXELS_ORIENTATION,
            "per_page": PEXELS_PER_PAGE,
            "size": "large",
        }

        try:
            resp = requests.get(url, headers=headers, params=params, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            photos = data.get("photos", [])

            if not photos:
                print(f"[MediaSourcer] No Pexels results for '{query}', using fallback.")
                return self._fallback_images()

            # Download each photo
            for i, photo in enumerate(photos):
                img_url = photo["src"]["large2x"]  # High-res portrait
                self._download_image(img_url, i)

            print(f"[MediaSourcer] Downloaded {len(photos)} images to {self.session_dir}")
            return self.session_dir

        except Exception as e:
            print(f"[MediaSourcer] Pexels API error ({e}), using fallback images.")
            return self._fallback_images()

    def _download_image(self, url, index):
        """Download a single image to the session directory."""
        try:
            resp = requests.get(url, timeout=30, stream=True)
            resp.raise_for_status()
            # Determine extension from content-type
            content_type = resp.headers.get("Content-Type", "image/jpeg")
            ext = "jpg" if "jpeg" in content_type or "jpg" in content_type else "png"
            filepath = os.path.join(self.session_dir, f"img_{index:02d}.{ext}")
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(8192):
                    f.write(chunk)
        except Exception as e:
            print(f"[MediaSourcer] Failed to download image {index}: {e}")

    def _fallback_images(self):
        """Use existing local images as fallback."""
        # Pick the first available local image folder
        for folder in ["images1", "images2", "images3", "images4"]:
            path = os.path.join("images", folder)
            if os.path.isdir(path) and os.listdir(path):
                print(f"[MediaSourcer] Fallback: using {path}")
                return f"./images/{folder}"
        return "./images/images1"

    def cleanup(self):
        """Remove the temp session directory after video is rendered."""
        if os.path.exists(self.session_dir):
            shutil.rmtree(self.session_dir)
            print("[MediaSourcer] Cleaned up temp images.")


if __name__ == "__main__":
    sourcer = MediaSourcer()
    result = sourcer.source(mood="melancholic", theme="solitude")
    print(f"\n  Images: {result['images_path']}")
    print(f"  Audio:  {result['audio_path']}")
