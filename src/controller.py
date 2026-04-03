import os
import sys
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("QuoteEngine")

# Ensure the 'src' directory is in the path for internal imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from input import get_input_dict
# VideoGenerator and ImageGenerator will be imported dynamically or at top level
# Since they are in the same directory, we can import them directly
from vid_generator import VideoGenerator
from img_generator import ImageGenerator
from enricher import CognitiveEnricher

class QuoteEngine:
    """
    Main controller for the Quote2Vid engine, orchestrating the
    enrichment, generation, and publication pipeline.
    """
    def __init__(self, config_path=None):
        logger.info("Initializing QuoteEngine...")
        self.input_dict = get_input_dict(config_path)
        self.enricher = CognitiveEnricher()
        logger.info(f"Loaded configuration for quote: {self.input_dict['quote'][:50]}...")

    def enrich_content(self):
        """Runs the cognitive specialist's enrichment layer."""
        enrichment = self.enricher.enrich(self.input_dict["quote"], self.input_dict["author"])
        
        # Overlay enriched aesthetic parameters
        aesthetics = enrichment.get("aesthetics", {})
        self.input_dict["bg_img_opacity"] = aesthetics.get("opacity", self.input_dict["bg_img_opacity"])
        self.input_dict["bg_img_duration"] = aesthetics.get("bg_img_duration", self.input_dict["bg_img_duration"])
        self.input_dict["font_size"] = aesthetics.get("font_size", 55)
        
        # Store metadata for publishing
        self.input_dict["caption"] = enrichment.get("caption", self.input_dict["quote"])
        self.input_dict["hashtags"] = enrichment.get("hashtags", [])
        
        return enrichment

    def generate_video(self):
        """Generates the video content based on the input dictionary."""
        logger.info("Starting video generation...")
        try:
            gen = VideoGenerator(
                quote=self.input_dict["quote"],
                author_name=self.input_dict["author"],
                output_name=self.input_dict["outputName"],
                imagesPath=self.input_dict["imagesPath"],
                font=self.input_dict["font"],
                audio_path=self.input_dict["audio"],
                randomImages=self.input_dict["random"],
                opacity=self.input_dict["bg_img_opacity"],
                bg_img_duration=self.input_dict["bg_img_duration"],
                font_size=self.input_dict.get("font_size", 55)
            )
            gen.generate()
            logger.info(f"Video generation complete: {self.input_dict['outputName']}")
            return self.input_dict["outputName"]
        except Exception as e:
            logger.error(f"Video generation failed: {e}")
            raise

    def generate_image(self):
        """Generates the square post image."""
        logger.info("Starting image generation...")
        try:
            gen = ImageGenerator(
                quote=self.input_dict["quote"],
                author=self.input_dict["author"],
                output_name=self.input_dict["imgOutputName"]
            )
            # Note: ImageGenerator uses its own default watermark and font for now
            # In Phase 3/4 we will unify this.
            gen.generate()
            logger.info(f"Image generation complete: {self.input_dict['imgOutputName']}")
            return self.input_dict["imgOutputName"]
        except Exception as e:
            logger.error(f"Image generation failed: {e}")
            return None

    def run_full_pipeline(self):
        """Runs the entire pipeline (Enrichment -> Generation -> Publication)."""
        logger.info("Running full pipeline...")
        
        # 1. Enrichment
        self.enrich_content()
        
        # 2. Generation
        video_path = self.generate_video()
        image_path = self.generate_image()
        
        # Publication step (Phase 5)
        # self.publish(video_path, image_path)
        
        return {
            "video": video_path,
            "image": image_path
        }

if __name__ == "__main__":
    # Quick test execution
    engine = QuoteEngine()
    engine.generate_video()
