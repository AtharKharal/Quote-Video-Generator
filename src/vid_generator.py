from moviepy import AudioFileClip
from moviepy.video.VideoClip import ImageClip, TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from PIL import Image
import numpy as np
import os, glob, random
from util import MediaUtils

class VideoGenerator:
    """
    Refactored VideoGenerator utilizing MediaUtils for deterministic 
    layout and aspect ratio management.
    """
    def __init__(self, quote, author_name, output_name, imagesPath, font, audio_path, randomImages, opacity, bg_img_duration, font_size=55):
        self.quote = quote
        self.output_name = output_name
        self.author_name = author_name
        self.height = 1920
        self.width = 1080
        self.duration = 7  # Initial default, will be adjusted by audio
        self.folder_path = imagesPath
        self.font = font
        self.audio_path = audio_path
        self.randomImages = randomImages
        self.opacity = opacity
        self.bg_img_duration = bg_img_duration
        self.font_size = font_size
        self.watermark_text = "@quill_of_humanity"

    def get_image_list(self):
        """Retrieves a list of images, either random or from a specific folder."""
        if self.randomImages:
            # Look for images across all imagesX folders
            file_pattern = 'images[0-9]*/*'
            all_files = [f for f in glob.glob(f"./images/{file_pattern}", recursive=True) if os.path.isfile(f)]
            
            if not all_files:
                # Fallback to current folder if exists
                if os.path.exists(self.folder_path):
                   all_files = [os.path.join(self.folder_path, f) for f in os.listdir(self.folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
            
            num_to_select = min(len(all_files), 15)
            return random.sample(all_files, num_to_select) if all_files else []
        else:
            if not os.path.exists(self.folder_path):
                return []
            img_list = []
            for f in sorted(os.listdir(self.folder_path)):
                if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp')):
                    img_list.append(os.path.join(self.folder_path, f))
            return img_list

    def format_images(self):
        """Crops and applies opacity to background images using MediaUtils."""
        formatted_images = []
        img_list = self.get_image_list()
        
        if not img_list:
            raise Exception(f"No background images found in {self.folder_path}")

        for img_path in img_list:
            try:
                with Image.open(img_path) as img:
                    img = img.convert("RGB")
                    # Use SmartCrop for deterministic 9:16 aspect ratio
                    cropped_img = MediaUtils.smart_crop(img, self.width, self.height)
                    # Use MediaUtils for consistent opacity/dimming
                    dimmed_img = MediaUtils.apply_opacity(cropped_img, self.opacity)
                    formatted_images.append(np.array(dimmed_img))
            except Exception as e:
                print(f"Warning: Failed to process image {img_path}: {e}")
        
        return formatted_images

    def generate_bg_clip(self, total_duration):
        """Creates a looping image sequence for the background."""
        images = self.format_images()
        
        # Ensure we have enough images to cover the duration
        # If we have 10 images at 0.35s each = 3.5s. We might need a few loops.
        num_loops = int(np.ceil(total_duration / (len(images) * self.bg_img_duration))) + 1
        repeated_images = images * num_loops
        
        durations = [self.bg_img_duration] * len(repeated_images)
        bg_sequence = ImageSequenceClip(repeated_images, durations=durations)
        
        return bg_sequence.with_duration(total_duration)

    def generate_text_clips(self, total_duration):
        """Generates the main quote text and author credit clips."""
        # Standardize on wide wrapping (width 40) or better: MoviePy caption method
        # Using caption method with specific width (900) automatically wraps.
        quote_clip = TextClip(
            text=self.quote,
            font=self.font,
            font_size=self.font_size,
            color="white",
            method="caption",
            size=(900, None),
            text_align="center"
        ).with_position(("center", "center")).with_duration(total_duration)

        # Ensure the quote fits in the safe zone
        if not MediaUtils.is_within_safe_zone(quote_clip.h):
            print(f"Warning: Quote clip height ({quote_clip.h}) exceeds safe zone. Scaling down...")
            # Simple downscale if too large
            quote_clip = quote_clip.with_scale(0.8).with_position(("center", "center"))

        # Author clip positioned relative to the center, or at the bottom 1/4
        author_y_pos = (self.height / 2) + (quote_clip.h / 2) + 60
        if author_y_pos > self.height - 300: # Protect bottom Reels UI
            author_y_pos = self.height - 400

        author_clip = TextClip(
            text=f"- {self.author_name}",
            font=self.font,
            font_size=40,
            color='white',
            method='caption',
            size=(800, None),
            text_align="center"
        ).with_position(("center", author_y_pos)).with_duration(total_duration)

        return quote_clip, author_clip

    def generate(self):
        """Executes the full video generation pipeline."""
        print(f"Generating video for: {self.author_name}")
        
        # Determine duration from audio
        audio_clip = AudioFileClip(self.audio_path)
        total_duration = audio_clip.duration
        
        # Core layers
        bg_clip = self.generate_bg_clip(total_duration)
        quote_clip, author_clip = self.generate_text_clips(total_duration)
        
        # Mandatory Watermark (Rule from primary_task.md)
        watermark_clip = TextClip(
            text=self.watermark_text,
            font=self.font,
            font_size=25,
            color="white"
        ).with_opacity(0.4).with_position(("center", 1820)).with_duration(total_duration)

        # Assemble
        final_video = CompositeVideoClip([bg_clip, quote_clip, author_clip, watermark_clip])
        final_video = final_video.with_audio(audio_clip)
        
        # Write output
        # Remove threads=4 to avoid potential race conditions with audio injection on some systems
        final_video.write_videofile(
            self.output_name, 
            codec="libx264", 
            audio_codec="aac", 
            fps=24,
            logger='bar'
        )
        
        # Close audio explicitly to free file handles (Good practice)
        audio_clip.close()
        
        return self.output_name

if __name__ == "__main__":
    # For backward compatibility if run directly
    try:
        from input import input_dict
        vidGen = VideoGenerator(
            input_dict["quote"], 
            input_dict["author"], 
            input_dict["outputName"],
            input_dict["imagesPath"], 
            input_dict["font"], 
            input_dict["audio"], 
            input_dict["random"],
            input_dict["bg_img_opacity"], 
            input_dict["bg_img_duration"]
        )
        vidGen.generate()
    except ImportError:
        print("Error: Could not import input_dict. Run via src/controller.py")