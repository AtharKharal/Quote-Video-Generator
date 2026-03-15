import os
from moviepy import AudioFileClip
from moviepy.video.VideoClip import ImageClip, TextClip
from moviepy.video.compositing import CompositeVideoClip
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from PIL import Image
import textwrap
import numpy as np

class VideoGenerator:
    def __init__(self, quote, author_name, output_name, font, audio_path):
        self.quote = quote
        self.output_name = output_name
        self.author_name = author_name
        self.height = 1920
        self.width = 1080
        self.duration = 7 # Seconds
        self.folder_path = "./images/images2"
        self.font = font
        self.audio_path = audio_path

    def crop_image(self, img_path):
        # 1. Load with PIL and force RGB mode
        with Image.open(img_path) as img:
            img = img.convert("RGB")
            orig_w, orig_h = img.size
            
            target_ratio = self.width / self.height
            orig_ratio = orig_w / orig_h

            if orig_ratio > target_ratio:
                # Image is wider than 9:16
                new_w = int(round(orig_h * target_ratio))
                left = (orig_w - new_w) // 2
                top = 0
                right = left + new_w
                bottom = orig_h
            else:
                # Image is taller than 9:16
                new_h = int(round(orig_w / target_ratio))
                left = 0
                top = (orig_h - new_h) // 2
                right = orig_w
                bottom = top + new_h
            
            # 2. Crop and Resize
            img = img.crop((left, top, right, bottom))
            img = img.resize((self.width, self.height), Image.Resampling.LANCZOS)
            
            # 3. Convert back to a MoviePy ImageClip
            # We convert the PIL image to a numpy array first
            return ImageClip(np.array(img))

    def get_images(self):
        images = []
        for f in sorted(os.listdir(self.folder_path)):
            if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                img_path = os.path.join(self.folder_path, f)

                cropped_img = self.crop_image(img_path)
                frame = cropped_img.get_frame(0) # Getting frame first for opacity effect

                frame_with_opacity = (frame * 0.3).astype("uint8") 
            
                images.append(frame_with_opacity)
        
        return images

    def generate_bg(self):
        _images = self.get_images()
        
        repeated_images = (lambda lst, n: [item for _ in range(n) for item in lst])(_images, 10)
        durations = (lambda arr: [0.2] * len(arr))(repeated_images)
        for img in repeated_images:
            print(img.size)

        print("------asdasdasd--------")
        clip = ImageSequenceClip(repeated_images, durations=durations)
        print("------zxcvbnm--------")

        
        return clip.with_duration(self.duration)

    def generate_text(self):
        # Manually wrapping text cuz I don't trust moviepy
        wrapper = textwrap.TextWrapper(width=35)
        wrapped_text = "\n".join(wrapper.wrap(text=self.quote))

        txt = TextClip(
            text=wrapped_text,
            font=self.font,
            font_size=55,
            color="white",
            method="caption",
            size=(980, None), # Padding on x-axis
            text_align="center",
            margin=(100, 150) # To avoid vertical text cut-off
        ).with_position(("center", "center")).with_duration(self.duration)

        txt_author = TextClip(
            text=self.author_name,
            font=self.font,
            font_size=45,
            color='white',
            method='caption',
            margin=(100, 150), # To avoid vertical text cut-off
            size=((1080 - 100), None), # Padding on x-axis
            text_align="center"
        ).with_position(("center", 0.52), relative=True).with_duration(self.duration)

        return txt, txt_author

    def generate(self):
        bg_clip = self.generate_bg()
        text_clip, author_text_clip = self.generate_text()
        audio_clip = AudioFileClip(self.audio_path)

        final_clip = CompositeVideoClip.CompositeVideoClip([bg_clip, text_clip, author_text_clip])
        final_clip = final_clip.with_audio(audio_clip)
        final_clip.write_videofile(self.output_name, codec="libx264")