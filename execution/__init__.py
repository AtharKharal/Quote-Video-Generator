"""
Consolidated module for video generation and publishing logic.
"""

import os, json, time, base64, uuid, requests, random, textwrap, glob
from moviepy import AudioFileClip
from moviepy.video.VideoClip import ImageClip, TextClip
from moviepy.video.compositing import CompositeVideoClip
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from PIL import Image
import numpy as np
from dotenv import load_dotenv

load_dotenv()

# --- Static Captions Data ---
FOLLOW_TEXT = "follow @quill_of_humanity for more content!"
CAPTIONS = {
    "Oscar Wilde": "Oscar Wilde was a famous Irish writer, poet, and playwright known for his sharp wit and Aesthetic Movement leadership.",
    "William Shaksphere": "William Shakespeare was the legendary English playwright of Hamlet, Macbeth, and Romeo and Juliet.",
    "Fyodor Dostoevsky": "Fyodor Dostoevsky was a Russian novelist exploring deep morality, faith, and the human mind.",
    "Carl Jung": "Carl Jung was a Swiss psychiatrist who founded analytical psychology and explored the collective unconscious.",
    "Bertrand Russell": "Bertrand Russell was a Nobel-winning philosopher and logician who championed reason and humanitarian ideals."
}

# --- Configuration Builder ---
def build_input(quote, author, output_name="output.mp4", font="fonts/font.ttf",
                audio="audios/3.mp3", images_path="./images/images1",
                random_images=False, caption_override=None):
    if caption_override:
        caption = caption_override
    else:
        bio = CAPTIONS.get(author, f"A quote by {author}.")
        caption = f"{quote}\n{FOLLOW_TEXT}\n\n{bio}"
    
    return {
        "quote": quote, "author": author, "outputName": output_name,
        "font": font, "audio": audio, "imagesPath": images_path,
        "random": random_images, "caption": caption, "file_path": f"./{output_name}",
    }

# --- Video Generation ---
class VideoGenerator:
    def __init__(self, quote, author_name, output_name, imagesPath, font, audio_path, randomImages):
        self.quote, self.author_name, self.output_name = quote, author_name, output_name
        self.height, self.width, self.duration = 1920, 1080, 7
        self.folder_path, self.font, self.audio_path, self.randomImages = imagesPath, font, audio_path, randomImages

    def _prepare_image(self, img_path):
        with Image.open(img_path) as img:
            img = img.convert("RGB")
            w, h = img.size
            target = self.width / self.height
            if w/h > target:
                nw = int(round(h * target))
                img = img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
            else:
                nh = int(round(w / target))
                img = img.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
            return ImageClip(np.array(img.resize((self.width, self.height), Image.Resampling.LANCZOS)))

    def generate(self):
        if self.randomImages:
            files = [f for f in glob.glob("./images/images*/*") if os.path.isfile(f)]
            img_list = random.sample(files, min(len(files), 10))
        else:
            img_list = [os.path.join(self.folder_path, f) for f in sorted(os.listdir(self.folder_path)) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        frames = [(self._prepare_image(p).get_frame(0) * 0.3).astype("uint8") for p in img_list]
        bg = ImageSequenceClip(frames * 10, durations=[0.2] * len(frames) * 10).with_duration(self.duration)
        
        wrapped = "\n".join(textwrap.wrap(self.quote, width=35))
        txt = TextClip(text=wrapped, font=self.font, font_size=55, color="white", method="caption", size=(980, None), text_align="center").with_position("center").with_duration(self.duration)
        auth = TextClip(text=self.author_name, font=self.font, font_size=45, color='white', method='caption', size=(980, None), text_align="center").with_position(("center", 0.52), relative=True).with_duration(self.duration)
        
        audio = AudioFileClip(self.audio_path)
        final = CompositeVideoClip.CompositeVideoClip([bg, txt, auth]).with_audio(audio).with_duration(min(self.duration, audio.duration))
        final.write_videofile(self.output_name, codec="libx264")

# --- Video Publishing ---
class VideoPublisher:
    def __init__(self, caption, file_path):
        self.caption, self.file_path = caption, file_path

    def publish_video(self):
        print("📤 Uploading to GitHub...")
        with open(self.file_path, "rb") as f: content = base64.b64encode(f.read()).decode('utf-8')
        headers = {"Authorization": f"Bearer {os.getenv('GITHUB_PAT')}", "Accept": "application/vnd.github+json"}
        url = f"{os.getenv('GITHUB_REPO_PATH')}/{uuid.uuid4()}.mp4"
        video_url = requests.put(url, json={"message": "Upload", "content": content}, headers=headers).json()["content"]["download_url"]

        print("🎬 Creating IG Reels container...")
        base_url = f"https://graph.facebook.com/v20.0/{os.getenv('BUSINESS_ACC_ID')}"
        token = os.getenv('ACCESS_TOKEN')
        cid = requests.post(f"{base_url}/media", json={"video_url": video_url, "caption": self.caption, "access_token": token, "media_type": "REELS", "share_to_feed": True}).json()["id"]

        while True:
            res = requests.get(f"https://graph.facebook.com/v20.0/{cid}?fields=status_code&access_token={token}").json()
            if res.get("status_code") == "FINISHED": break
            if res.get("status_code") == "ERROR": raise Exception(f"IG Error: {res}")
            time.sleep(5)

        print("🚀 Publishing...")
        return requests.post(f"{base_url}/media_publish?creation_id={cid}&access_token={token}").status_code
